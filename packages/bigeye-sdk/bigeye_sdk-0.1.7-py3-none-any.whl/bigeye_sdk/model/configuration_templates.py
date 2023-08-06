from __future__ import annotations

import inspect
from dataclasses import dataclass, field

from bigeye_sdk.decorators.dataclass_decorators import add_from_dict
from bigeye_sdk.log import get_logger
from bigeye_sdk.functions.metric_functions import get_seconds_from_window_size, enforce_lookback_type_defaults, \
    is_freshness_metric, get_freshness_metric_name_for_field, get_thresholds_for_metric, get_notification_channels
from bigeye_sdk.generated.com.torodata.models.generated import MetricConfiguration, TimeInterval, TimeIntervalType, \
    PredefinedMetric, PredefinedMetricName, MetricParameter, LookbackType, MetricType

# create logger
log = get_logger(__file__)


@dataclass
class SimpleUpsertMetricRequest:
    schema_name: str
    table_name: str
    column_name: str
    metric_template: SimpleMetricTemplate = None
    from_metric: int = None

    def build_upsert_request_object(self, warehouse_id: int, table: dict):
        return self.metric_template.build_upsert_request_object(warehouse_id,
                                                                table,
                                                                self.column_name,
                                                                None)

    @classmethod
    def from_dict(cls, d: dict) -> SimpleUpsertMetricRequest:
        [cls_params, smt_params] = map(lambda keys: {x: d[x] for x in keys if x in d},
                                       [inspect.signature(cls).parameters,
                                        inspect.signature(SimpleMetricTemplate).parameters])

        cls_params["metric_template"] = SimpleMetricTemplate.from_dict(smt_params) if smt_params \
            else SimpleMetricTemplate.from_dict(cls_params["metric_template"])
        return cls(**cls_params)


@dataclass
@add_from_dict
class SimpleMetricTemplate:
    metric_name: str  # the user configured name
    metric_type: str  # the actual metric type
    notifications: list = field(default_factory=lambda: [])
    thresholds: list = field(default_factory=lambda: [])
    filters: list = field(default_factory=lambda: [])
    group_by: list = field(default_factory=lambda: [])
    default_check_frequency_hours: int = 2
    update_schedule = None
    delay_at_update: str = "0 minutes"
    timezone: str = "UTC"
    should_backfill: bool = False
    lookback_type: str = None
    lookback_days: int = 2
    window_size: str = "1 day"
    window_size_seconds = get_seconds_from_window_size(window_size)

    def __post_init__(self):
        # TODO: see if we can move this into default.
        self.lookback_type = enforce_lookback_type_defaults(predefined_metric_name=self.metric_type,
                                                            lookback_type=self.lookback_type)

    def build_upsert_request_object(self,
                                    warehouse_id: int,
                                    table: dict,
                                    column_name: str = None,
                                    existing_metric: MetricConfiguration = None) -> MetricConfiguration:
        """
        Converts a simple metric template to a MetricConfiguration that can be used to upsert a metric to Bigeye.
        Must include either a column name or an existing metric
        :param warehouse_id:
        :param existing_metric: Pass the existing MetricConfiguration if updating
        :param table: The table object to which the metric will be deployed
        :param column_name: The column name to which the metric will be deployed.
        :return:
        """

        ifm = is_freshness_metric(self.metric_type)

        if ifm:
            # TODO: Validate
            self.metric_type = get_freshness_metric_name_for_field(table, column_name)
            if self.update_schedule is None:
                raise Exception("Update schedule can not be null for freshness schedule thresholds")

        new_metric = MetricConfiguration()
        new_metric.name = self.metric_name
        new_metric.schedule_frequency = TimeInterval(
            interval_type=TimeIntervalType.HOURS_TIME_INTERVAL_TYPE,
            interval_value=self.default_check_frequency_hours
        )

        new_metric.thresholds = get_thresholds_for_metric(self.metric_type, self.timezone, self.delay_at_update,
                                                          self.update_schedule, self.thresholds)

        new_metric.warehouse_id = warehouse_id

        new_metric.dataset_id = table["id"]

        pm = PredefinedMetric(PredefinedMetricName.from_string(self.metric_type))
        mt = MetricType()
        mt.predefined_metric = pm
        new_metric.metric_type = mt

        new_metric.parameters = [MetricParameter(key="arg1", column_name=column_name)]

        new_metric.lookback = TimeInterval(interval_type=TimeIntervalType.DAYS_TIME_INTERVAL_TYPE,
                                           interval_value=self.lookback_days)

        new_metric.notification_channels = get_notification_channels(self.notifications)

        new_metric.filters = self.filters

        new_metric.group_bys = self.group_by

        table_has_metric_time = False

        if not ifm:  # TODO: Look into repeated logic.
            for field_key, field in table["fields"].items():
                if field["metricTimeField"]:
                    table_has_metric_time = True

        if table_has_metric_time:
            new_metric.lookback_type = LookbackType.from_string(self.lookback_type)
            if self.lookback_type == "METRIC_TIME_LOOKBACK_TYPE":
                new_metric.grain_seconds = self.window_size_seconds

        if existing_metric is None:
            return new_metric
        else:
            existing_metric.thresholds = new_metric.thresholds
            existing_metric.notification_channels = new_metric.notification_channels if new_metric.notification_channels else []
            existing_metric.schedule_frequency = new_metric.schedule_frequency
            if not ifm and table_has_metric_time:
                existing_metric.lookback_type = new_metric.lookback_type
                existing_metric.lookback = new_metric.lookback
                existing_metric.grain_seconds = new_metric.grain_seconds
            return existing_metric
