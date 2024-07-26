import os
from typing import List

import requests
from sqlalchemy.orm import Session

from abstraction.abstract_loader import AbstractLoader
from decorators.decorators import refresh_jwt_if_needed
from models.models import OmnicommVehicleDirectory
from models.serializer import serialize_vehicle_directory_model, deserialize_query_all_model
from structs.dataclasses import JwtClaims, VehicleDirectoryResponse, deserialize_dict


class VehicleDirectoryLoader(AbstractLoader):
    def __init__(self, db_session: Session, auth_data: JwtClaims):
        super().__init__(db_session, auth_data)
        self.endpoint: str = os.getenv("OMNICOMM_VEHICLE_DIRECTORY_ENDPOINT")

    @refresh_jwt_if_needed()
    def __get_vehicle_list(self):
        response = requests.get(
            url=self.url + self.endpoint,
            headers=self.bearer_auth
        )
        vehicle_response = deserialize_dict(response.json(), VehicleDirectoryResponse)
        return vehicle_response

    def __format_vehicle_list_for_db(self):
        vehicle_list_for_db = []
        vehicle_obj: VehicleDirectoryResponse = self.__get_vehicle_list()
        serialize_vehicle_directory_model(vehicle_list_for_db, vehicle_obj)
        return vehicle_list_for_db

    def __write_to_db(self):
        entries = self.__format_vehicle_list_for_db()
        unique_entries_uuid = set(record.uuid for record in entries)
        existing_records: List[OmnicommVehicleDirectory] = deserialize_query_all_model(
            rows=self.db_session
            .query(OmnicommVehicleDirectory.uuid)
            .filter(OmnicommVehicleDirectory.uuid.in_(unique_entries_uuid))
            .all(),
            _T=OmnicommVehicleDirectory
        )
        existing_uuids = {record[0] for record in existing_records}

        records_to_add = [record for record in entries if record.uuid not in existing_uuids]

        self.db_session.add_all(records_to_add)
        self.db_session.commit()

    def __is_table_empty(self) -> bool:
        if self.db_session.query(OmnicommVehicleDirectory).count() > 0:
            return False
        return True

    def run(self):
        self.__write_to_db()
