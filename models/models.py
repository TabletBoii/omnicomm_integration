

from sqlalchemy import String, Column, Integer, Unicode, Date, Boolean, UniqueConstraint, TIMESTAMP, DOUBLE_PRECISION
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class OmnicommVehicleDirectory(Base):
    __tablename__ = "omnicomm_vehicle_directory"

    primary_id = Column('primary_id', Integer, primary_key=True, autoincrement=True)
    id = Column('id', Integer)
    parentGroupId = Column('parent_group_id', Integer)
    org = Column('org', String)
    autocheck_id = Column('autocheck_id', Integer)
    uuid = Column('uuid', String)
    name = Column('name', String)
    terminal_type = Column('terminal_type', String)
    terminal_id = Column('terminal_id', Integer)
    receive_data = Column('receive_data', Integer)

    __table_args__ = (
        UniqueConstraint('uuid', name='uix_1'),
    )


class OmnicommStatisticsData(Base):
    __tablename__ = "omnicomm_data"

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    vehicle_id = Column('vehicle_id', Integer)
    name = Column('name', String)

    period_begin = Column('period_begin', TIMESTAMP)
    period_end = Column('period_end', TIMESTAMP)

    fuelConsMHWOMovement = Column('fuel_cons_mhwo_movement', DOUBLE_PRECISION)
    fuelConsMH = Column('fuel_cons_mh', DOUBLE_PRECISION)
    fuelConsumptionWOMovement = Column('fuel_consumption_wo_movement', Integer)
    startVolume = Column('start_volume', Integer)
    fuelCons100Ex = Column('fuel_cons_100_ex', Integer)
    fuelConsPerMotorhour = Column('fuel_cons_per_motorhour', DOUBLE_PRECISION)
    fuelConsumptionOnMove100 = Column('fuel_consumption_on_move_100', DOUBLE_PRECISION)
    fuelConsumption = Column('fuel_consumption', Integer)
    fuelConsDev = Column('fuel_cons_dev', Integer)
    endVolume = Column('end_volume', Integer)
    fuelCons100Dev = Column('fuel_cons_100_dev', Integer)
    deviationWorkNormIdleLoad = Column('deviation_work_norm_idle_load', DOUBLE_PRECISION)
    draining = Column('draining', Integer)
    fuelCons100 = Column('fuel_cons_100', DOUBLE_PRECISION)
    normConsumptionMH = Column('norm_consumption_mh', DOUBLE_PRECISION)
    normCons100 = Column('norm_cons100', Integer)
    delivery = Column('delivery', Integer)
    dutyConsumptionMH = Column('duty_consumptionmh', Integer)
    deviation = Column('deviation', Integer)
    fuelConsumptionNotMoveIdle = Column('fuel_consumption_not_move_idle', Integer)
    maxVolume = Column('max_volume', Integer)
    fuelConsumptionOnWorked = Column('fuel_consumption_on_worked', Integer)
    filling = Column('filling', Integer)
    dutyConsumption100 = Column('duty_consumption_100', Integer)
    minVolume = Column('min_volume', Integer)
    fuelConsumptionOnWorkedNoMovement = Column('fuel_consumption_on_worked_no_movement', Integer)
    co2Emission = Column('co2_emission', DOUBLE_PRECISION)
    refuelling = Column('refuelling', Integer)
    fuelConsEx = Column('fuel_cons_ex', Integer)
    fuelConsumptionOnMove = Column('fuel_consumption_on_move', Integer)
    fuelConsMHMovement = Column('fuel_cons_mh_movement', DOUBLE_PRECISION)
    fuelConsumptionOnMoveIdle = Column('fuel_consumption_on_move_idle', Integer)

    layUp = Column('lay_up', Integer)
    excessRPMPercent = Column('excess_rpm_percent', Integer)
    excessRPM = Column('excess_rpm', Integer)
    movementPercent = Column('movement_percent', DOUBLE_PRECISION)
    layUpPercent = Column('lay_up_percent', DOUBLE_PRECISION)
    maxSpeed = Column('max_speed', DOUBLE_PRECISION)
    mileageSpeeding = Column('mileage_speeding', Integer)
    idlingRPM = Column('idling_rpm', Integer)
    workedOnMovementPercent = Column('worked_on_movement_percent', DOUBLE_PRECISION)
    normalRPMPercent = Column('normal_rpm_percent', DOUBLE_PRECISION)
    worked = Column('worked', Integer)
    idlingRPMPercent = Column('idling_rpm_percent', DOUBLE_PRECISION)
    normalRPM = Column('normal_rpm', Integer)
    workedNoMovementPercent = Column('worked_no_movement_percent', DOUBLE_PRECISION)
    workedOnMovement = Column('worked_on_movement', Integer)
    movement = Column('movement', Integer)
    workedNoMovement = Column('worked_no_movement', Integer)
    mileage = Column('mileage', DOUBLE_PRECISION)
    motoHoursServiceCounter = Column('moto_hours_service_counter', DOUBLE_PRECISION)

