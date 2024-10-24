import datetime
import aiohttp
import asyncio
import os
import time as program_time
from typing import List, Coroutine, Dict, Union, Any
from zoneinfo import ZoneInfo

import sqlalchemy.exc
from aiohttp import ClientSession
from sqlalchemy import text
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from abstraction.abstract_loader import AbstractLoader
from models.models import OmnicommVehicleDirectory, OmnicommStatisticsData
from models.serializer import deserialize_query_all_model, serialize_statistics_data
from structs.dataclasses import JwtClaims, deserialize_dict
from structs.statistics_dataclass import StatisticsResponseVehicleDataList, StatisticsResponseList
from utils.utils import generate_url_list


class ConsolidatedReportLoader(AbstractLoader):
    def __init__(self, db_session: Session, auth_data: list[JwtClaims], single_day_update: bool):
        super().__init__(db_session, auth_data)
        self.endpoint: str = os.getenv("OMNICOMM_CONSOLIDATED_REPORT_ENDPOINT")
        self.period_begin = int(datetime.datetime.strptime(
            "2024-07-30 00:00:00",
            "%Y-%m-%d %H:%M:%S"
        ).replace(tzinfo=ZoneInfo("Etc/GMT-0")).timestamp()
                                )

        self.period_end = int(datetime.datetime
                              .now()
                              .replace(tzinfo=ZoneInfo("Etc/GMT-0"))
                              .timestamp()
                              )
        self.date_list = []
        self.single_day_update = single_day_update

    def __format_statistics_list_for_db(self,
                                        statistics_list: StatisticsResponseList | List[
                                            StatisticsResponseVehicleDataList]
                                        ) -> List[OmnicommStatisticsData]:
        statistics_list_for_db = []

        serialize_statistics_data(
            res_list=statistics_list_for_db,
            obj_list=statistics_list,
        )

        return statistics_list_for_db

    def __get_vehicle_id_list(self, username: str) -> List[OmnicommVehicleDirectory]:
        vehicle_id_list: List[OmnicommVehicleDirectory] = deserialize_query_all_model(
            rows=self.db_session
            .query(OmnicommVehicleDirectory.terminal_id)
            .filter(OmnicommVehicleDirectory.username == username)
            .all(),
            _T=OmnicommVehicleDirectory
        )
        vehicle_id_list = [vehicle[0] for vehicle in vehicle_id_list]
        return vehicle_id_list

    @staticmethod
    def batch_insert(session, objects, batch_size=100):
        for i in range(0, len(objects), batch_size):
            batch = objects[i:i + batch_size]
            session.add_all(batch)
            session.commit()

    def __write_to_db(self, formated_statistic_list: List[OmnicommStatisticsData]):
        # self.db_session.add_all(formated_statistic_list)
        # self.batch_insert(self.db_session, formated_statistic_list)
        # self.db_session.execute(insert(OmnicommStatisticsData), formated_statistic_list)
        try:
            self.db_session.bulk_save_objects(formated_statistic_list)
            self.db_session.commit()
        except sqlalchemy.exc.ProgrammingError as err:
            print(err.code)
            print(err)
            self.db_session.rollback()

    """
        Выгружает данные с 31 мая 2024 года по нынешнюю дату с очисткой всей таблицы
    """

    async def __async_get_consolidated_report(
            self,
            session: ClientSession,
            data: list
    ) -> Dict[str, Union[Coroutine, List[int]]]:
        async with session.get(data[0][0], headers={'Authorization': f'JWT {data[0][1]}'}) as response:
            response_item = await response.json()
            return {"response": response_item, "period": data[1]}

    async def __async_fetch_statistics(self) -> StatisticsResponseList:
        vehicle_id_list = []
        data_to_fetch = []
        active_usernames = self.db_session.query(OmnicommVehicleDirectory.username).distinct().all()
        for claim in self.auth_data:
            for username in active_usernames:
                if claim.username == username[0]:
                    vehicle_id_list.append([claim, self.__get_vehicle_id_list(claim.username)])
        for vehicle in vehicle_id_list:
            # vehicle_id_list.append(self.__get_vehicle_id_list(username[0]))
            url_list = generate_url_list(
                request_url=self.url + self.endpoint,
                vehicle_ids=vehicle,
                url_params_str=f"?dataGroups=[mw,fuel,mnt]&vehicles={vehicle[1]}",
                is_single_day=self.single_day_update
            )
            data_to_fetch += url_list

        async with aiohttp.ClientSession() as session:
            fetch_start_time = program_time.time()
            tasks = [self.__async_get_consolidated_report(session, item) for item in data_to_fetch]
            responses = list(await asyncio.gather(*tasks))
            print("Fetch time: --- %s seconds ---" % (program_time.time() - fetch_start_time))
            for response in responses:
                if response["response"]["code"] != 0:
                    print("Jopa")
                    print(response["response"])
                    responses.remove(response["response"])
            statistic_response_list = deserialize_dict({"data": responses}, StatisticsResponseList)

            # print(statistic_response_list)
        return statistic_response_list

    def run(self):
        start_time = program_time.time()

        if not self.single_day_update:
            self.db_session.execute(text("DELETE FROM omnicomm_data"))
        # statistic_response_list = asyncio.run(
            # self.__async_multiple_day_fetch_statistics())  # Запускать, если нужно выгрузить данные с 1 июня по нынешнее время
        statistic_response_list = asyncio.run(self.__async_fetch_statistics())
        formated_statistic_list = self.__format_statistics_list_for_db(statistic_response_list)
        db_start_time = program_time.time()
        self.__write_to_db(formated_statistic_list)
        print("Database insertion time: --- %s seconds ---" % (program_time.time() - db_start_time))
        print("--- %s seconds ---" % (program_time.time() - start_time))
