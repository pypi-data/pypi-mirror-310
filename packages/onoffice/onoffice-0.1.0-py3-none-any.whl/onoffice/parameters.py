import datetime
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Filter:
    key: str
    op: str
    val: Any

    def serialize(self):
        return self.key, [{"op": self.op, "val": self.val}]


@dataclass
class Parameter:
    def serialize(self) -> dict:
        return {}


@dataclass
class ReadParameter(Parameter):
    data: list[str]
    filters: list[Filter] = field(default_factory=list)

    limit: int = 50
    page: int = 0

    def serialize(self) -> dict:
        filters = {}
        for _filter in self.filters:
            key, val = _filter.serialize()
            filters[key] = val

        return {
            "data": self.data,
            "listlimit": self.limit,
            "listoffset": self.page * self.limit,
            "filter": filters,
        }


@dataclass
class Data:
    def serialize_where(self) -> dict[str, list[int]]:
        return {}

    def serialize_data(self) -> dict[str, str]:
        return {}


@dataclass
class AgentsLog(Data):
    address_ids: list[str]
    action_kind: str
    action_type: str
    note: str
    dt: datetime.datetime = field(default_factory=datetime.datetime.now)

    def serialize_where(self) -> dict[str, list[int]]:
        return {"addressids": self.address_ids}

    def serialize_data(self) -> dict[str, str]:
        return {
            "actionkind": self.action_kind,
            "actiontype": self.action_type,
            "note": self.note,
            "datetime": self.dt.strftime("%Y-%m-%d %H:%M:%S"),
        }


@dataclass
class Newsletter(Data):
    newsletter: int

    def serialize_data(self) -> dict[str, str]:
        return {"newsletter_aktiv": str(self.newsletter)}


@dataclass
class CreateParameter(Parameter):
    data: Data

    def serialize(self):
        where = self.data.serialize_where()
        data = self.data.serialize_data()
        return {**where, **data}


# print(CreateParameter(data=AgentsLog([123], "abc", "def", "ghi")).serialize())


# print(ReadParameter(data=["a"], filters=[Filter(key="abc", op="=", val="123")]).serialize())
