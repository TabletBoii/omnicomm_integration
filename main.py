from urllib.parse import quote_plus
import os
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine, text, Engine
from typing import Callable

from app.consolidated_report_loader import ConsolidatedReportLoader
from app.vehicle_directory_loader import VehicleDirectoryLoader
from structs.dataclasses import JwtClaims
from utils.utils import authorize_omnicomm, refresh_omnicomm


def main():
    dotenv_path = os.path.join(os.path.dirname(__file__), ".env")

    load_dotenv(
        dotenv_path=dotenv_path
    )
    omnicomm_username: str = os.getenv("OMNICOMM_USERNAME")
    omnicomm_password: str = os.getenv("OMNICOMM_PASSWORD")
    HAS_DB_CONNECTION_STRING: str = f'postgresql+psycopg2://{os.getenv("HAS_DB_USERNAME")}:{quote_plus(os.getenv("HAS_DB_PASSWORD"))}@{os.getenv("HAS_DB_SERVER")}/{os.getenv("HAS_DB_NAME")}'

    has_db_engine: Engine = create_engine(
        HAS_DB_CONNECTION_STRING
    )

    HasSession: Callable[[], Session] = sessionmaker(has_db_engine)
    session_121: Session = HasSession()
    auth_data: JwtClaims = authorize_omnicomm(omnicomm_username, omnicomm_password)

    # vehicle_directory_loader = VehicleDirectoryLoader(db_session=session_121, auth_data=auth_data)

    # vehicle_directory_loader.run()
    consolidated_report_loader = ConsolidatedReportLoader(db_session=session_121, auth_data=auth_data)
    print(consolidated_report_loader.jwt)
    consolidated_report_loader.run()


if __name__ == '__main__':

    main()



