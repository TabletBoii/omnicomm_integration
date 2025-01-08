import asyncio
import os
from typing import List
import time as program_time
import aiohttp
from aiohttp import ClientSession
from sqlalchemy import text
from sqlalchemy.orm import Session

from abstraction.abstract_loader import AbstractLoader
from models.models import OmnicommVehicleDirectory
from models.serializer import serialize_vehicle_directory_model, deserialize_query_all_model
from structs.dataclasses import JwtClaims, VehicleDirectoryResponse, deserialize_dict


class VehicleDirectoryLoader(AbstractLoader):
    def __init__(self, db_session: Session, auth_data: list[JwtClaims], delete_current_data):
        super().__init__(db_session, auth_data)
        self.endpoint: str = os.getenv("OMNICOMM_VEHICLE_DIRECTORY_ENDPOINT")
        self.delete_dir = delete_current_data

    @staticmethod
    async def __fetch_jwt_list(session: ClientSession, url: str, credential: JwtClaims) -> VehicleDirectoryResponse:
        async with session.get(url, headers={'Authorization': f'JWT {credential.jwt}'}) as response:
            response_item = await response.json()
            response_item["username"] = credential.username
            return deserialize_dict(response_item, VehicleDirectoryResponse)

    async def __get_vehicle_list(self) -> list[VehicleDirectoryResponse]:
        fetched_vehicle_list = []
        async with aiohttp.ClientSession() as session:
            tasks = [self.__fetch_jwt_list(session, self.url+self.endpoint, credential) for credential in self.auth_data if credential is not None]
            responses: list[VehicleDirectoryResponse] = list(await asyncio.gather(*tasks))
            for response in responses:
                fetched_vehicle_list.append(response)
        return fetched_vehicle_list

    def __format_vehicle_list_for_db(self, raw_vehicle_list, username: str) -> list[OmnicommVehicleDirectory]:
        vehicle_list_for_db = []
        serialize_vehicle_directory_model(vehicle_list_for_db, raw_vehicle_list, username)
        return vehicle_list_for_db

    def __write_to_db(self, entries: list[OmnicommVehicleDirectory]):
        unique_uuid = []
        unique_entries = []
        for entry in entries:
            if entry.uuid not in unique_uuid:
                unique_uuid.append(entry.uuid)
                unique_entries.append(entry)
                continue

        unique_entries_uuid = set(record.uuid for record in unique_entries)
        rows = self.db_session.query(OmnicommVehicleDirectory.uuid).filter(OmnicommVehicleDirectory.uuid.in_(unique_entries_uuid)).all()
        existing_records: List[OmnicommVehicleDirectory] = deserialize_query_all_model(
            rows=rows,
            _T=OmnicommVehicleDirectory
        )
        existing_uuids = {record[0] for record in existing_records}

        records_to_add = [record for record in unique_entries if record.uuid not in existing_uuids]
        # for record in entries:
        #     print(record.uuid)
        self.db_session.add_all(records_to_add)
        self.db_session.commit()

    def __is_table_empty(self) -> bool:
        if self.db_session.query(OmnicommVehicleDirectory).count() > 0:
            return False
        return True

    def run(self):
        start_time = program_time.time()
        if self.delete_dir:
            self.db_session.execute(text("TRUNCATE public.omnicomm_vehicle_directory"))
        statistic_db_list = asyncio.run(self.__get_vehicle_list())
        for statistic in statistic_db_list:
            # print(statistic)
            formated_statistic_db_list = self.__format_vehicle_list_for_db(statistic, statistic.username)
            # for i in formated_statistic_db_list:
            #     print(i.name)
            self.__write_to_db(formated_statistic_db_list)
        print("--- %s seconds ---" % (program_time.time() - start_time))
