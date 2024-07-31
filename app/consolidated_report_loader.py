import datetime
import os
import time as program_time
from typing import List, Coroutine, Dict, Union
from zoneinfo import ZoneInfo

import requests
from aiohttp import ClientSession
from sqlalchemy import text
from sqlalchemy.orm import Session
from datetime import time

from abstraction.abstract_loader import AbstractLoader
from decorators.decorators import refresh_jwt_if_needed
from exceptions.custom_exceptions import WrongTimeToRun
from mock_data.statistic_data import statistic_list_mock_data
from models.models import OmnicommVehicleDirectory, OmnicommStatisticsData
from models.serializer import serialize_vehicle_directory_model, deserialize_query_all_model, serialize_statistics_data
from structs.dataclasses import JwtClaims, VehicleDirectoryResponse, deserialize_dict
from structs.statistics_dataclass import StatisticsResponse, StatisticsResponseVehicleDataList, StatisticsResponseList
from utils.utils import generate_date_list, generate_url_list

import aiohttp
import asyncio


class ConsolidatedReportLoader(AbstractLoader):
    def __init__(self, db_session: Session, auth_data: JwtClaims):
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

    def __format_statistics_list_for_db(self,
                                        statistics_list: StatisticsResponseList | List[StatisticsResponseVehicleDataList]
                                        ) -> List[OmnicommStatisticsData]:
        statistics_list_for_db = []
        serialize_statistics_data(
            res_list=statistics_list_for_db,
            obj_list=statistics_list
        )

        return statistics_list_for_db

    @refresh_jwt_if_needed()
    def __fetch_statistics(self) -> List[StatisticsResponseVehicleDataList]:
        url = self.url + self.endpoint
        vehicle_id_list = self.__get_vehicle_id_list()
        current_date = datetime.datetime.now()
        if datetime.time(16, 1, 0) < current_date.time() < datetime.time(16, 30, 0):
            end_date_1 = datetime.datetime.strptime(f"{current_date.year}-{current_date.month}-{current_date.day} 10:00:00",
                                           "%Y-%m-%d %H:%M:%S").replace(tzinfo=ZoneInfo("Etc/GMT-0"))
            begin_date_1 = end_date_1 - datetime.timedelta(hours=18)
        elif datetime.time(10, 1, 0) < current_date.time() < datetime.time(10, 30, 0):
            end_date_1 = datetime.datetime.strptime(f"{current_date.year}-{current_date.month}-{current_date.day} 10:00:00",
                                                    "%Y-%m-%d %H:%M:%S").replace(tzinfo=ZoneInfo("Etc/GMT-0"))
            begin_date_1 = end_date_1 - datetime.timedelta(hours=18)
        else:
            raise WrongTimeToRun()
        # url += f"?timeBegin={start_date}&timeEnd={end_date}&dataGroups=%5Bmw%2Cfuel%2Cmnt%5D&vehicles={vehicle_id_list}"
        url += f"?timeBegin={begin_date_1}&timeEnd={end_date_1}&dataGroups=[mw,fuel,mnt]&vehicles={vehicle_id_list}"
        response = requests.get(
            url=url,
            headers=self.bearer_auth
        )
        statistic_response = deserialize_dict(response.json(), StatisticsResponse)
        return statistic_response.data.vehicleDataList
        # print(response.json())
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

    def __write_to_db(self, formated_statistic_list: List[OmnicommStatisticsData]):

        self.db_session.add_all(formated_statistic_list)
        self.db_session.commit()

    """
        Выгружает данные с 31 мая 2024 года по нынешнюю дату с очисткой всей таблицы
    """

    async def __async_get_consolidated_report(
            self,
            session: ClientSession, url: list
    ) -> Dict[str, Union[Coroutine, List[int]]]:
        async with session.get(url[0], headers=self.bearer_auth) as response:
            response_item = await response.json()
            return {"response": response_item, "period": url[1]}

    async def __async_fetch_statistics(self) -> StatisticsResponseList:
        vehicle_id_list = self.__get_vehicle_id_list()
        url_list, date_list = generate_url_list(
            request_url=self.url + self.endpoint,
            url_params_str=f"?dataGroups=[mw,fuel,mnt]&vehicles={vehicle_id_list}"
        )
        self.date_list = date_list

        async with aiohttp.ClientSession() as session:
            tasks = [self.__async_get_consolidated_report(session, url) for url in list(zip(url_list, date_list))]
            responses = list(await asyncio.gather(*tasks))
            for response in responses:
                if response["response"]["code"] != 0:
                    print("Jopa")
                    print(response["response"]["message"])
                    responses.remove(response["response"])
            statistic_response_list = deserialize_dict({"data": responses}, StatisticsResponseList)
            # print(statistic_response_list)
        return statistic_response_list

    def run(self):
        self.db_session.execute(text("DELETE FROM omnicomm_data"))
        start_time = program_time.time()
        # statistic_response_list = asyncio.run(self.__async_fetch_statistics()) # Запускать, если нужно выгрузить данные с 1 июня по нынешнее время
        statistic_response_list = self.__fetch_statistics()
        formated_statistic_list = self.__format_statistics_list_for_db(statistic_response_list)
        self.__write_to_db(formated_statistic_list)
        print("--- %s seconds ---" % (program_time.time() - start_time))

