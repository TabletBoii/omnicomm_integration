from datetime import datetime
from typing import List, TypeVar, Type, Any, Tuple, Dict, Union

from sqlalchemy import Row, func

from models.models import OmnicommVehicleDirectory, OmnicommStatisticsData
from structs.dataclasses import VehicleDirectoryResponse, VehicleDirectoryChildren
from structs.statistics_dataclass import StatisticsResponseVehicleDataList, StatisticsResponseList


def serialize_vehicle_directory_model(res_list: list, obj: Union[VehicleDirectoryResponse, VehicleDirectoryChildren], username: str) -> None:

    for vehicle in obj.objects:
        if obj.children:
            for vehicle_child_list in obj.children:
                serialize_vehicle_directory_model(res_list, vehicle_child_list, username)
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
                receive_data=vehicle.receive_data,
                username=username
            )
        )


def serialize_to_obj(vehicle: StatisticsResponseVehicleDataList, periods: List[int]) -> OmnicommStatisticsData:
    return OmnicommStatisticsData(
        vehicle_id=vehicle.vehicleID,
        name=vehicle.name,
        period_begin=datetime.fromtimestamp(periods[0]),
        period_end=datetime.fromtimestamp(periods[1]),

        fuelConsMHWOMovement=vehicle.fuel.fuelConsMHWOMovement,
        fuelConsMH=vehicle.fuel.fuelConsMH,
        fuelConsumptionWOMovement=vehicle.fuel.fuelConsumptionWOMovement,
        startVolume=vehicle.fuel.startVolume,
        fuelCons100Ex=vehicle.fuel.fuelCons100Ex,
        fuelConsPerMotorhour=vehicle.fuel.fuelConsPerMotorhour,
        fuelConsumptionOnMove100=vehicle.fuel.fuelConsumptionOnMove100,
        fuelConsumption=vehicle.fuel.fuelConsumption,
        fuelConsDev=vehicle.fuel.fuelConsDev,
        endVolume=vehicle.fuel.endVolume,
        fuelCons100Dev=vehicle.fuel.fuelCons100Dev,
        deviationWorkNormIdleLoad=vehicle.fuel.deviationWorkNormIdleLoad,
        draining=vehicle.fuel.draining,
        fuelCons100=vehicle.fuel.fuelCons100,
        normConsumptionMH=vehicle.fuel.normConsumptionMH,
        normCons100=vehicle.fuel.normCons100,
        delivery=vehicle.fuel.delivery,
        dutyConsumptionMH=vehicle.fuel.dutyConsumptionMH,
        deviation=vehicle.fuel.deviation,
        fuelConsumptionNotMoveIdle=vehicle.fuel.fuelConsumptionNotMoveIdle,
        maxVolume=vehicle.fuel.maxVolume,
        fuelConsumptionOnWorked=vehicle.fuel.fuelConsumptionOnWorked,
        filling=vehicle.fuel.filling,
        dutyConsumption100=vehicle.fuel.dutyConsumption100,
        minVolume=vehicle.fuel.minVolume,
        fuelConsumptionOnWorkedNoMovement=vehicle.fuel.fuelConsumptionOnWorkedNoMovement,
        co2Emission=vehicle.fuel.co2Emission,
        refuelling=vehicle.fuel.refuelling,
        fuelConsEx=vehicle.fuel.fuelConsEx,
        fuelConsumptionOnMove=vehicle.fuel.fuelConsumptionOnMove,
        fuelConsMHMovement=vehicle.fuel.fuelConsMHMovement,
        fuelConsumptionOnMoveIdle=vehicle.fuel.fuelConsumptionOnMoveIdle,

        layUp=vehicle.mw.layUp,
        excessRPMPercent=vehicle.mw.excessRPMPercent,
        excessRPM=vehicle.mw.excessRPM,
        movementPercent=vehicle.mw.movementPercent,
        layUpPercent=vehicle.mw.layUpPercent,
        maxSpeed=vehicle.mw.maxSpeed,
        mileageSpeeding=vehicle.mw.mileageSpeeding,
        idlingRPM=vehicle.mw.idlingRPM,
        workedOnMovementPercent=vehicle.mw.workedOnMovementPercent,
        normalRPMPercent=vehicle.mw.normalRPMPercent,
        worked=vehicle.mw.worked,
        idlingRPMPercent=vehicle.mw.idlingRPMPercent,
        normalRPM=vehicle.mw.normalRPM,
        workedNoMovementPercent=vehicle.mw.workedNoMovementPercent,
        workedOnMovement=vehicle.mw.workedOnMovement,
        movement=vehicle.mw.movement,
        workedNoMovement=vehicle.mw.workedNoMovement,
        mileage=vehicle.mw.mileage,
        motoHoursServiceCounter=vehicle.mw.motoHoursServiceCounter
    )


def serialize_statistics_data(
        res_list: list,
        obj_list: StatisticsResponseList | List[StatisticsResponseVehicleDataList],
        periods: Dict[str, int]=None
) -> None:

    if isinstance(obj_list, StatisticsResponseList):
        for obj in obj_list.data:
            for vehicle in obj.response.data.vehicleDataList:

                res_list.append(
                    serialize_to_obj(vehicle, periods=obj.period)
                )
    else:
        for vehicle in obj_list:
            res_list.append(
                serialize_to_obj(vehicle, periods=periods)
            )


T = TypeVar('T')


def deserialize_query_all_model(rows: List[Any], _T: Type[T]) -> List[T]:
    if rows and hasattr(rows[0], '__table__'):
        return rows
    elif len(rows) == 0:
        return []
    elif isinstance(rows[0], Row):
        return rows
    else:
        return [_T(**row._asdict()) for row in rows]


async def async_deserialize_query_all_model(rows: List[Any], _T: Type[T]) -> List[T]:
    if rows and hasattr(rows[0], '__table__'):
        return rows
    elif isinstance(rows[0], Row):
        return rows
    else:
        return [_T(**row._asdict()) for row in rows]
