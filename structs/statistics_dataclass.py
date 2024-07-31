from dataclasses import dataclass, field, is_dataclass, fields
from typing import TypeVar, Dict, Any, Type, List


@dataclass
class StatisticsReponseTotalMw:
    totalMoveTimePercent: float | None
    totalMovementMileage: float | None
    totalWorkedOnExcessRPM: float | None
    totalMileage: float | None
    totalWorkedPercent: float | None
    totalMileageSpeeding: float | None
    totalWorkedUnderLoadRPMPercent: float | None
    totalWorkedOnExcessRPMPercent: float | None
    totalWorkedOnMove: int | None
    totalWorkedOnNormalRPMPercent: float | None
    totalWorked: int | None
    totalMovementMileagePerLitre: float | None
    totalWorkedOnIdlingRPMPercent: float | None
    totalWorkedUnderLoadRPM: int | None
    totalMileagePerLitre: float | None
    totalWorkedOnMovePercent: float | None
    averageSpeed: float | None
    maxSpeed: float | None
    totalWorkedNoMovementPercent: float | None
    totalLayUpTime: int | None
    totalWorkedNoMovementTime: int | None
    averageMileage: float | None
    totalWorkedOnIdlingRPM: int | None
    totalWorkedOnNormalRPM: int | None
    totalMoveTime: int | None
    averageMoveTime: int | None
    totalLayUpTimePercent: float | None


@dataclass
class StatisticsReponseTotalFuel:
    totalFuelOnMoveCrit: float | None
    consPerMHEngineOn: float | None
    totalFuelNotMoveIdle: int | None
    averageConsumptionMH: float | None
    consumptionEngineOn: int | None
    totalFuelOnMoveNorm: int | None
    totalFuelConsumptionMHMovement: float | None
    totalDelivery: int | None
    totalConsumptionOnMove: int | None
    averageConsumptionMHMovement: float | None
    totalConsumptionWOMovement: int | None
    totalFuelOnMoveIdle: int | None
    totalRefuelling: int | None
    averageConsumptionMHWOMovement: float | None
    totalFilling: float | None
    averageConsumption: float | None
    totalConsumption: int | None
    averageConsumptionOnMove100: float | None
    totalFuelNotMoveNorm: int | None
    co2Emission: float | None
    totalFuelNotMoveCrit: float | None
    averageConsumption100: float | None
    totalDraining: int | None


@dataclass
class StatisticsResponseVehicleDataFuel:
    fuelConsMHWOMovement: float
    fuelConsMH: float
    fuelConsumptionWOMovement: int
    startVolume: int
    fuelCons100Ex: int
    fuelConsPerMotorhour: float
    fuelConsumptionOnMove100: float
    fuelConsumption: int
    fuelConsDev: int | None
    endVolume: int
    fuelCons100Dev: int | None
    deviationWorkNormIdleLoad: float
    draining: int
    fuelCons100: float
    normConsumptionMH: float | None
    normCons100: int
    delivery: int
    dutyConsumptionMH: int
    deviation: int
    fuelConsumptionNotMoveIdle: int
    maxVolume: int
    fuelConsumptionOnWorked: int
    filling: int
    dutyConsumption100: int
    minVolume: int
    fuelConsumptionOnWorkedNoMovement: int
    co2Emission: float
    refuelling: int
    fuelConsEx: int
    fuelConsumptionOnMove: int
    fuelConsMHMovement: float
    fuelConsumptionOnMoveIdle: int


@dataclass
class StatisticsResponseVehicleDataMw:
    layUp: int
    excessRPMPercent: int
    excessRPM: int
    movementPercent: float
    layUpPercent: float
    maxSpeed: float
    mileageSpeeding: int
    idlingRPM: int
    workedOnMovementPercent: float
    normalRPMPercent: float
    worked: int
    idlingRPMPercent: float
    normalRPM: int
    workedNoMovementPercent: float
    workedOnMovement: int
    movement: int
    workedNoMovement: int
    mileage: float
    motoHoursServiceCounter: float | None


@dataclass
class StatisticsResponseVehicleDataList:
    fuel: StatisticsResponseVehicleDataFuel
    name: str
    mw: StatisticsResponseVehicleDataMw
    vehicleID: int


@dataclass
class StatisticsResponseData:
    totalMw: StatisticsReponseTotalMw
    vehicleDataList: List[StatisticsResponseVehicleDataList]
    totalFuel: StatisticsReponseTotalFuel


@dataclass
class StatisticsResponse:
    code: int
    data: StatisticsResponseData
    message: str


@dataclass
class StatisticResponseItem:
    response: StatisticsResponse
    period: list


@dataclass
class StatisticsResponseList:
    data: List[StatisticResponseItem]
