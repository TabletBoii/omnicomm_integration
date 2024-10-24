import ast
import asyncio
from json import loads
import os
from typing import List, Union, Type, Any
from zoneinfo import ZoneInfo

import aiohttp
import requests
import base64
from datetime import datetime, timedelta, time

from aiohttp import ClientSession
from sqlalchemy import Column
from sqlalchemy.orm import Session

from exceptions.custom_exceptions import WrongTimeToRun
from models.models import OmnicommCredentials
from structs.dataclasses import JwtClaims


TIMEZONE = "Etc/GMT-5"


def authorize_omnicomm(login: str, password: str) -> JwtClaims:
    head_url = os.getenv("OMNICOMM_HEAD_URL")
    auth_endpoint = '/auth/login?jwt=1'
    response = requests.post(
        url=head_url + auth_endpoint,
        data={
            "login": login,
            "password": password
        },
    )

    return JwtClaims(**response.json())


def refresh_omnicomm(jwt_claims: JwtClaims) -> None:
    head_url: str = os.getenv("OMNICOMM_HEAD_URL")
    refresh_endpoint: str = '/auth/refresh'
    response = requests.post(
        url=head_url + refresh_endpoint,
        headers={'Authorization': f'JWT {jwt_claims.refresh}'}
    )
    jwt = response.json()["jwt"]
    jwt_claims.jwt = jwt


def is_token_expired(jwt_claims: JwtClaims) -> bool:
    jwt = jwt_claims.jwt
    jwt_parts = jwt.split(".")
    decoded_jwt_payload = base64.b64decode(jwt_parts[1])
    decoded_jwt_payload_dict = loads(decoded_jwt_payload.decode("utf-8"))
    jwt_exp = decoded_jwt_payload_dict["exp"]
    current_timestamp = datetime.now().timestamp()

    if jwt_exp <= current_timestamp + 60:
        return True

    return False


def generate_date_list() -> List[List[Union[int, int]]]:
    date_list = []
    current_month = datetime.now().month
    current_day = datetime.now().day
    start_month = 6  # 6
    start_date = 1  # 1
    for year in ["2024"]:
        for month in range(start_month, current_month + 1):
            if month < 10:
                date_month = "0" + str(month)
            else:
                date_month = str(month)

            if month in (1, 3, 5, 7, 8, 10, 12):
                range_end = 31
            elif month in (4, 6, 9, 11):
                range_end = 30
            elif (int(year) - 2000) % 4 == 0 and month == 2:
                range_end = 29
            else:
                range_end = 28

            if month == current_month:
                range_end = current_day - 1

            for day in range(start_date, range_end + 1, 1):

                if day < 10:
                    date_day = "0" + str(day)
                else:
                    date_day = str(day)
                end_date_1 = datetime.strptime(f"{year}-{date_month}-{date_day} 19:00:00",
                                               "%Y-%m-%d %H:%M:%S").replace(tzinfo=ZoneInfo(TIMEZONE))
                begin_date_1 = end_date_1 - timedelta(hours=12)

                end_date_2 = datetime.strptime(f"{year}-{date_month}-{date_day} 07:00:00",
                                               "%Y-%m-%d %H:%M:%S").replace(tzinfo=ZoneInfo(TIMEZONE))
                begin_date_2 = end_date_2 - timedelta(hours=12)
                date_list.append([int(begin_date_1.timestamp()), int(end_date_1.timestamp())])
                date_list.append([int(begin_date_2.timestamp()), int(end_date_2.timestamp())])

    return date_list


def generate_url_list(request_url: str, vehicle_ids: list, url_params_str: str, is_single_day: bool) -> list[Any]:
    url_list = []
    if not is_single_day:
        date_list = generate_date_list()
    else:
        current_date = datetime.now()
        end_date_1 = datetime.strptime(f"{current_date.year}-{current_date.month}-{current_date.day} 19:00:00",
                                       "%Y-%m-%d %H:%M:%S").replace(tzinfo=ZoneInfo(TIMEZONE))
        begin_date_1 = end_date_1 - timedelta(hours=12)

        end_date_2 = datetime.strptime(f"{current_date.year}-{current_date.month}-{current_date.day} 07:00:00",
                                       "%Y-%m-%d %H:%M:%S").replace(tzinfo=ZoneInfo(TIMEZONE))
        begin_date_2 = end_date_2 - timedelta(hours=12)

        date_list = [[int(begin_date_1.timestamp()), int(end_date_1.timestamp())],[int(begin_date_2.timestamp()), int(end_date_2.timestamp())]]
    for date_element in date_list:
        url_list.append([
            request_url + url_params_str + f"&timeBegin={date_element[0]}&timeEnd={date_element[1]}",
            vehicle_ids[0].jwt
        ])
    return list(zip(url_list, date_list))


async def fetch_jwt_list(session: ClientSession, url: str, credential: Type[OmnicommCredentials]) -> JwtClaims:
    try:
        async with session.post(url, data={"login": credential.login, "password": credential.password}) as response:
            response_item = await response.json()
            print(response_item)
            response_item["username"] = credential.login
            return JwtClaims(**response_item)
    except Exception as e:
        print(e)
        return


async def multiple_authorize_omnicomm(session: Session) -> list[JwtClaims]:
    head_url = os.getenv("OMNICOMM_HEAD_URL")
    auth_endpoint = '/auth/login?jwt=1'
    url = head_url + auth_endpoint
    jwt_token_list: list[JwtClaims] = []
    credential_list: List[Type[OmnicommCredentials]] = session.query(OmnicommCredentials).all()
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_jwt_list(session, url, credential) for credential in credential_list]
        responses: list[JwtClaims] = list(await asyncio.gather(*tasks))
        for response in responses:
            jwt_token_list.append(response)

    return jwt_token_list
