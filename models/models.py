

from sqlalchemy import String, Column, Integer, UniqueConstraint, TIMESTAMP, DOUBLE_PRECISION, DateTime
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
    username = Column('username', String)

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
    fuelConsumptionWOMovement = Column('fuel_consumption_wo_movement', DOUBLE_PRECISION)
    startVolume = Column('start_volume', DOUBLE_PRECISION)
    fuelCons100Ex = Column('fuel_cons_100_ex', DOUBLE_PRECISION)
    fuelConsPerMotorhour = Column('fuel_cons_per_motorhour', DOUBLE_PRECISION)
    fuelConsumptionOnMove100 = Column('fuel_consumption_on_move_100', DOUBLE_PRECISION)
    fuelConsumption = Column('fuel_consumption', DOUBLE_PRECISION)
    fuelConsDev = Column('fuel_cons_dev', DOUBLE_PRECISION)
    endVolume = Column('end_volume', DOUBLE_PRECISION)
    fuelCons100Dev = Column('fuel_cons_100_dev', DOUBLE_PRECISION)
    deviationWorkNormIdleLoad = Column('deviation_work_norm_idle_load', DOUBLE_PRECISION)
    draining = Column('draining', DOUBLE_PRECISION)
    fuelCons100 = Column('fuel_cons_100', DOUBLE_PRECISION)
    normConsumptionMH = Column('norm_consumption_mh', DOUBLE_PRECISION)
    normCons100 = Column('norm_cons100', DOUBLE_PRECISION)
    delivery = Column('delivery', DOUBLE_PRECISION)
    dutyConsumptionMH = Column('duty_consumptionmh', DOUBLE_PRECISION)
    deviation = Column('deviation', DOUBLE_PRECISION)
    fuelConsumptionNotMoveIdle = Column('fuel_consumption_not_move_idle', DOUBLE_PRECISION)
    maxVolume = Column('max_volume', DOUBLE_PRECISION)
    fuelConsumptionOnWorked = Column('fuel_consumption_on_worked', DOUBLE_PRECISION)
    filling = Column('filling', DOUBLE_PRECISION)
    dutyConsumption100 = Column('duty_consumption_100', DOUBLE_PRECISION)
    minVolume = Column('min_volume', DOUBLE_PRECISION)
    fuelConsumptionOnWorkedNoMovement = Column('fuel_consumption_on_worked_no_movement', DOUBLE_PRECISION)
    co2Emission = Column('co2_emission', DOUBLE_PRECISION)
    refuelling = Column('refuelling', DOUBLE_PRECISION)
    fuelConsEx = Column('fuel_cons_ex', DOUBLE_PRECISION)
    fuelConsumptionOnMove = Column('fuel_consumption_on_move', DOUBLE_PRECISION)
    fuelConsMHMovement = Column('fuel_cons_mh_movement', DOUBLE_PRECISION)
    fuelConsumptionOnMoveIdle = Column('fuel_consumption_on_move_idle', DOUBLE_PRECISION)

    layUp = Column('lay_up', DOUBLE_PRECISION)
    excessRPMPercent = Column('excess_rpm_percent', DOUBLE_PRECISION)
    excessRPM = Column('excess_rpm', DOUBLE_PRECISION)
    movementPercent = Column('movement_percent', DOUBLE_PRECISION)
    layUpPercent = Column('lay_up_percent', DOUBLE_PRECISION)
    maxSpeed = Column('max_speed', DOUBLE_PRECISION)
    mileageSpeeding = Column('mileage_speeding', DOUBLE_PRECISION)
    idlingRPM = Column('idling_rpm', DOUBLE_PRECISION)
    workedOnMovementPercent = Column('worked_on_movement_percent', DOUBLE_PRECISION)
    normalRPMPercent = Column('normal_rpm_percent', DOUBLE_PRECISION)
    worked = Column('worked', DOUBLE_PRECISION)
    idlingRPMPercent = Column('idling_rpm_percent', DOUBLE_PRECISION)
    normalRPM = Column('normal_rpm', DOUBLE_PRECISION)
    workedNoMovementPercent = Column('worked_no_movement_percent', DOUBLE_PRECISION)
    workedOnMovement = Column('worked_on_movement', DOUBLE_PRECISION)
    movement = Column('movement', DOUBLE_PRECISION)
    workedNoMovement = Column('worked_no_movement', DOUBLE_PRECISION)
    mileage = Column('mileage', DOUBLE_PRECISION)
    motoHoursServiceCounter = Column('moto_hours_service_counter', DOUBLE_PRECISION)


class OmnicommCredentials(Base):
    __tablename__ = "omnicomm_auth_data"

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    login = Column('login', String)
    password = Column('password', String)
