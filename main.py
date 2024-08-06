import os
import asyncio
import argparse
from urllib.parse import quote_plus
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine, Engine
from typing import Callable

from app.consolidated_report_loader import ConsolidatedReportLoader
from app.vehicle_directory_loader import VehicleDirectoryLoader
from utils.utils import multiple_authorize_omnicomm


def str2bool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def main(
    ld,
    dd,
    ud,
    sdu
):

    dotenv_path = os.path.join(os.path.dirname(__file__), ".env")

    load_dotenv(
        dotenv_path=dotenv_path
    )
    HAS_DB_CONNECTION_STRING: str = f'postgresql+psycopg2://{os.getenv("HAS_DB_USERNAME")}:{quote_plus(os.getenv("HAS_DB_PASSWORD"))}@{os.getenv("HAS_DB_SERVER")}/{os.getenv("HAS_DB_NAME")}'

    has_db_engine: Engine = create_engine(
        HAS_DB_CONNECTION_STRING
    )

    HasSession: Callable[[], Session] = sessionmaker(has_db_engine)
    session_121: Session = HasSession()

    all_accounts_auth_data = asyncio.run(multiple_authorize_omnicomm(session_121))
    # print(all_accounts_auth_data)

    if ld:
        # auth_data: JwtClaims = authorize_omnicomm(omnicomm_username, omnicomm_password)
        if dd:
            print("Vehicle directory update started with table TRUNCATE")
        else:
            print("Vehicle directory update started")
        vehicle_directory_loader = VehicleDirectoryLoader(
            db_session=session_121,
            auth_data=all_accounts_auth_data,
            delete_current_data=dd
        )

        vehicle_directory_loader.run()
    """
        TODO: 
        Запускать скрипт выгружать с 29 июля 16:00 по 30 июля 10:00 и с 30 июля 10:00 по 30 июля 16:00
        Скрипт запускается в 10:01 утра, выгружается данные с 16:00 предыдущего дня по 10:00 нынешнего дня
        Второй запуск в 16:01 - выгружает данные с 10:00 нынешнего дня по 16:00 нынешнего дня
    """
    if ud:
        if sdu:
            print("Data update started")
        else:
            print("Muptiple data update started")
        consolidated_report_loader = ConsolidatedReportLoader(
            db_session=session_121,
            auth_data=all_accounts_auth_data,
            single_day_update=sdu
        )
        consolidated_report_loader.run()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='A script to load and update omnicomm info or vehicles directory')

    # parser.add_argument('filename', type=str, help='The name of the file to process')
    parser.add_argument(
        '-l', '--load_dir',
        type=str2bool,
        help='Updates info about all omnicomm accounts vehicles listed in "omnicomm_auth_data" database table'
    )
    parser.add_argument(
        '-r', '--remove_dir',
        type=str2bool,
        help='Truncate directory table before --load_dir action'
    )
    parser.add_argument(
        '-u', '--update_data',
        type=str2bool,
        help='Update omnicomm data about transportations'
    )
    parser.add_argument(
        '-m', '--multiple_update_data',
        type=str2bool,
        help='Truncate data table and upload all omnicomm data about transportations since june 2024 until current date'
    )

    load_dir = False
    delete_dir = False
    update_data = True
    single_day_update = True

    args = parser.parse_args()
    if args.load_dir:
        load_dir = True
    if args.remove_dir:
        delete_dir = True
    if args.update_data:
        update_data = True
    if args.multiple_update_data:
        single_day_update = False

    main(
        ld=load_dir,
        dd=delete_dir,
        ud=update_data,
        sdu=single_day_update
    )



