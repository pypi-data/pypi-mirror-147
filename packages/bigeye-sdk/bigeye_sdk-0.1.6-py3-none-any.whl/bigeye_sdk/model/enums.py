import enum


# TODO: All of these codes are from semantic and should be in a protobuf somehwere.

class MetaEnum(enum.EnumMeta):
    def __contains__(cls, item):
        try:
            cls(item)
        except ValueError:
            return False
        return True


class MetricStatus(enum.Enum, metaclass=MetaEnum):
    HEALTHY = 'HEALTHY'  # Query by this status will contain healthy metrics
    ALERTING = 'ALERTING'  # Query by this status will contain alerting metrics
    UNKNOWN = 'UNKNOWN'  # Query by this status will contain failed and unknown status metrics.

