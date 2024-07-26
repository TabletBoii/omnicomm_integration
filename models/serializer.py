from typing import List, TypeVar, Type, Any

from sqlalchemy import Row

from models.models import OmnicommVehicleDirectory
from structs.dataclasses import VehicleDirectoryResponse


def serialize_vehicle_directory_model(res_list: list, obj: VehicleDirectoryResponse) -> None:
    for vehicle in obj.objects:
        res_list.append(
            OmnicommVehicleDirectory(
                id=obj.id,
                parentGroupId=obj.parentGroupId,
                org=obj.name,
                autocheck_id=obj.autocheck_id,
                uuid=vehicle.uuid,
                name=vehicle.name,
                terminal_type=vehicle.terminal_type,
                terminal_id=vehicle.terminal_id,
                receive_data=vehicle.receive_data
            )
        )


T = TypeVar('T')


def deserialize_query_all_model(rows: List[Any], _T: Type[T]) -> List[T]:
    if rows and hasattr(rows[0], '__table__'):
        return rows
    elif isinstance(rows[0], Row):
        return rows
    else:
        return [_T(**row._asdict()) for row in rows]

