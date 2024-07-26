import datetime
import os
from typing import List

import requests
from sqlalchemy.orm import Session

from abstraction.abstract_loader import AbstractLoader
from decorators.decorators import refresh_jwt_if_needed
from models.models import OmnicommVehicleDirectory
from models.serializer import serialize_vehicle_directory_model, deserialize_query_all_model
from structs.dataclasses import JwtClaims, VehicleDirectoryResponse, deserialize_dict


class ConsolidatedReportLoader(AbstractLoader):
    def __init__(self, db_session: Session, auth_data: JwtClaims):
        super().__init__(db_session, auth_data)
        self.endpoint: str = os.getenv("OMNICOMM_CONSOLIDATED_REPORT_ENDPOINT")

    @refresh_jwt_if_needed()
    def __get_consolidated_report(self):
        url = self.url+self.endpoint

        vehicle_id_list = self.__get_vehicle_id_list()
        end_date = int(datetime.datetime.now().timestamp())
        start_date = int(datetime.datetime.strptime("2024-07-26 00:00:00", "%Y-%m-%d %H:%M:%S").timestamp())
        print(start_date)
        print(end_date)
        request_body = {
          # "vehicleIds": vehicle_id_list,
          "vehicleIds": [1219004491, 1219004498, 1219004508, 1219004492, 1219004646],
          "timeBegin": start_date,
          "timeEnd": end_date
        }
        url += f"?timeBegin={start_date}&timeEnd={end_date}&dataGroups=%5Bmw%2Cfuel%2Cmnt%5D&vehicles={vehicle_id_list}"
        response = requests.get(
            url=url,
            headers=self.bearer_auth
        )

        print(response.json())
        # vehicle_response = deserialize_dict(response.json(), VehicleDirectoryResponse)
        # return vehicle_response

    def __get_vehicle_id_list(self) -> List[OmnicommVehicleDirectory]:
        vehicle_id_list: List[OmnicommVehicleDirectory] = deserialize_query_all_model(
            rows=self.db_session
            .query(OmnicommVehicleDirectory.terminal_id)
            .all(),
            _T=OmnicommVehicleDirectory
        )
        vehicle_id_list = [vehicle[0] for vehicle in vehicle_id_list]
        return vehicle_id_list

    def run(self):
        self.__get_consolidated_report()
