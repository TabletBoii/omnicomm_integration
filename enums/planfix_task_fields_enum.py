from enum import Enum


class HasIndustrialObjectsEnum(Enum):
    SALARY = 10307
    BUSINESS_TRIP = 11501
    PAID_CLAIMS = 12503


class HasChinaObjectsEnum(Enum):
    SALARY = 43704
    PAID_CLAIMS = 43698
    BUSINESS_TRIP = 43706


class HasChinaTaskFieldsEnum(Enum):
    EXPENSE_ITEM = "104734" #
    TURNOVER_DATE = "" # У индастриала нет даты совершения оборота (что логично)
    CURRENCY = "" # У индастриала нет валюты приобретения (что логично)
    CURRENCY2 = "104732"
    PROJECT_NAME = "" # У индастриала нет проекта (что логично)
    PAY_DATE = "104770" #
    ACQUISITION_COST = "104730" #
    AMOUNT_TO_PAY = "104740" # Сумма к оплате
    PAID = "107330" # Оплаченная сумма
    PAID2 = "104766" #
    PREPAYMENT = "" # У индастриала нет предоплаты (что логично)
    PAYMENT_TYPE = "104750" # Вид платежа
    SUPPLIER = "106130" # Поставщик
    ORGANIZATION = "" # У индастриала нет организации (что логично)
    PHOTO_CONFIRMATION = "104762" #
    INITIATOR = "104728" #


class HasIndustrialTaskFieldsEnum(Enum):
    EXPENSE_ITEM = "22545" #
    TURNOVER_DATE = "" # У индастриала нет даты совершения оборота (что логично)
    CURRENCY = "" # У индастриала нет валюты приобретения (что логично)
    CURRENCY2 = "22543"
    PROJECT_NAME = "" # У индастриала нет проекта (что логично)
    PAY_DATE = "22905" #
    ACQUISITION_COST = "22539" #
    AMOUNT_TO_PAY = "23271" # Сумма к оплате
    PAID = "31179" # Оплаченная сумма
    PAID2 = "22903" #
    PREPAYMENT = "" # У индастриала нет предоплаты (что логично)
    PAYMENT_TYPE = "22895" # Вид платежа
    SUPPLIER = "31171" # Поставщик
    ORGANIZATION = "" # У индастриала нет организации (что логично)
    PHOTO_CONFIRMATION = "23285" #
    INITIATOR = "22537" #


class HasGlobalTaskFieldsEnum(Enum):
    EXPENSE_ITEM = "85850" #
    TURNOVER_DATE = "86190" #
    CURRENCY = "67632" #
    CURRENCY2 = "73678"
    PROJECT_NAME = "85874" #
    PAY_DATE = "85856" #
    ACQUISITION_COST = "67630" #
    AMOUNT_TO_PAY = "85858" # Сумма к оплате
    PAID = "86392" # Оплаченная сумма
    PAID2 = "85854" #
    PREPAYMENT = "67246" #
    PAYMENT_TYPE = "67636" # Вид платежа
    SUPPLIER = "87336" # Поставщик
    ORGANIZATION = "67112" #
    PHOTO_CONFIRMATION = "86548" #
    INITIATOR = "85928" #


class HasGlobalTaskTemplateEnum(Enum):
    COORDINATION_OF_EXPENSES = 349988  # Согласование приобретения товаров/услуг Старый ID - 125 +
    CAR_TRANSPORTATION_EXPENSES = 336921  # Расходы по перевозке авто +
    REIMBURSEMENT_FOR_BUSINESS_TRIP_EXPENSES = 232666     # Возмещение по командировке +
    BUSINESS_TRIP_ADDITIONAL_EXPENSES = 232665  # Доп.затраты по командировке +
    PRETENSION_PAYMENTS_EXPENSES = 59569  # Оплаты по претензиям +
    BANK_COMMISSION_EXPENSES = 35389  # Комиссия банка +
    CURRENCY_CONVERSION_EXPENSES = 103446  # Конвертация валюты +
    DRIVERS_SALARY_EXPENSES = 18558  # Согласование ЗП водителям +
    SALARY_STATEMENT_EXPENSES = 18551  # Согласование ведомости по ЗП +
    PAYING_DEBTS_EXPENSES = 10237  # Оплата долгов +
    BUSINESS_TRIP_APPROVAL_EXPENSES = 10004  # Согласование командировки +
    COORDINATION_OF_BUSINESS_TRIP_ALLOWANCES_EXPENSES = 8227  # Согласование командировочных +
    PAYMENT_WITH_THE_CARRIER_EXPENSES = 62  # Расчет с перевозчиком (ЮЛ)	Дата произведения оплаты +
    APPLICATION_FOR_FINAL_SETTLEMENT_WITH_THE_CARRIER_INDIVIDUAL_EXPENSES = 61  # Заявка на ок.расчет с перевозчиком (ЧЛ) +
    APPLICATION_FOR_PREPAYMENT_TO_THE_CARRIER_INDIVIDUAL_EXPENSES = 55  # Заявка на предоплату перевозчику (ЧЛ) +
    APPLICATION_FOR_PREPAYMENT_TO_THE_CARRIER_EXPENSES_LE = 1909  # Заявка на предоплату перевозчику (ЮЛ) +

