from dataclasses import dataclass, field, is_dataclass, fields
from typing import TypeVar, Dict, Any, Type

@dataclass
class JwtClaims:
    jwt: str
    refresh: str


@dataclass
class VehicleDirectoryObject:
    uuid: str
    name: str
    terminal_type: str
    terminal_id: int
    receive_data: int


@dataclass
class VehicleDirectoryResponse:
    id: int
    parentGroupId: int | None
    name: str
    autocheck_id: int
    children: list
    objects: list[VehicleDirectoryObject] = field(default_factory=list)


T = TypeVar('T')


def deserialize_dict(data: Dict[str, Any], cls: Type[T]) -> T:
    if is_dataclass(cls):
        fieldtypes = {f.name: f.type for f in fields(cls)}
        kwargs = {}
        for field_name, field_type in fieldtypes.items():
            try:
                if field_name in data:
                    field_value = data[field_name]
                    if is_dataclass(field_type):
                        kwargs[field_name] = deserialize_dict(field_value, field_type)
                    elif isinstance(field_value, list) and hasattr(field_type, '__origin__') and field_type.__origin__ is list:
                        item_type = field_type.__args__[0]
                        kwargs[field_name] = [deserialize_dict(item, item_type) if is_dataclass(item_type) else item for item in field_value]
                    else:
                        kwargs[field_name] = field_value
                else:
                    kwargs[field_name] = None

            except TypeError as err:
                print(err)
                # print(data)
        return cls(**kwargs)


    else:
        raise ValueError(f"Expected a dataclass for {cls}")
