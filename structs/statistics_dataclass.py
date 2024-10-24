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
    totalWorkedOnMove: float | None
    totalWorkedOnNormalRPMPercent: float | None
    totalWorked: float | None
    totalMovementMileagePerLitre: float | None
    totalWorkedOnIdlingRPMPercent: float | None
    totalWorkedUnderLoadRPM: float | None
    totalMileagePerLitre: float | None
    totalWorkedOnMovePercent: float | None
    averageSpeed: float | None
    maxSpeed: float | None
    totalWorkedNoMovementPercent: float | None
    totalLayUpTime: float | None
    totalWorkedNoMovementTime: float | None
    averageMileage: float | None
    totalWorkedOnIdlingRPM: float | None
    totalWorkedOnNormalRPM: float | None
    totalMoveTime: float | None
    averageMoveTime: float | None
    totalLayUpTimePercent: float | None


@dataclass
class StatisticsReponseTotalFuel:
    totalFuelOnMoveCrit: float | None
    consPerMHEngineOn: float | None
    totalFuelNotMoveIdle: float | None
    averageConsumptionMH: float | None
    consumptionEngineOn: float | None
    totalFuelOnMoveNorm: float | None
    totalFuelConsumptionMHMovement: float | None
    totalDelivery: float | None
    totalConsumptionOnMove: float | None
    averageConsumptionMHMovement: float | None
    totalConsumptionWOMovement: float | None
    totalFuelOnMoveIdle: float | None
    totalRefuelling: float | None
    averageConsumptionMHWOMovement: float | None
    totalFilling: float | None
    averageConsumption: float | None
    totalConsumption: float | None
    averageConsumptionOnMove100: float | None
    totalFuelNotMoveNorm: float | None
    co2Emission: float | None
    totalFuelNotMoveCrit: float | None
    averageConsumption100: float | None
    totalDraining: float | None


@dataclass
class StatisticsResponseVehicleDataFuel:
    fuelConsMHWOMovement: float
    fuelConsMH: float
    fuelConsumptionWOMovement: float
    startVolume: float
    fuelCons100Ex: float
    fuelConsPerMotorhour: float
    fuelConsumptionOnMove100: float
    fuelConsumption: float
    fuelConsDev: float | None
    endVolume: float
    fuelCons100Dev: float | None
    deviationWorkNormIdleLoad: float
    draining: float
    fuelCons100: float
    normConsumptionMH: float | None
    normCons100: float
    delivery: float
    dutyConsumptionMH: float
    deviation: float
    fuelConsumptionNotMoveIdle: float
    maxVolume: float
    fuelConsumptionOnWorked: float
    filling: float
    dutyConsumption100: float
    minVolume: float
    fuelConsumptionOnWorkedNoMovement: float
    co2Emission: float
    refuelling: float
    fuelConsEx: float
    fuelConsumptionOnMove: float
    fuelConsMHMovement: float
    fuelConsumptionOnMoveIdle: float


@dataclass
class StatisticsResponseVehicleDataMw:
    layUp: float
    excessRPMPercent: float
    excessRPM: float
    movementPercent: float
    layUpPercent: float
    maxSpeed: float
    mileageSpeeding: float
    idlingRPM: float
    workedOnMovementPercent: float
    normalRPMPercent: float
    worked: float
    idlingRPMPercent: float
    normalRPM: float
    workedNoMovementPercent: float
    workedOnMovement: float
    movement: float
    workedNoMovement: float
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
