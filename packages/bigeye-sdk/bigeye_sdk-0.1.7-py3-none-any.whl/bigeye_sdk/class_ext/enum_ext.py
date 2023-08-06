import enum


class StrEnum(enum.Enum):
    def __str__(self):
        return self.name


class EnumExtension(StrEnum):
    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))
