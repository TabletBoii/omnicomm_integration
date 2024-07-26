import ast
from json import loads
import os
import requests
import base64
from datetime import datetime
from structs.dataclasses import JwtClaims


def authorize_omnicomm(login: str, password: str) -> JwtClaims:
    head_url = os.getenv("OMNICOMM_HEAD_URL")
    auth_endpoint = '/auth/login?jwt=1'
    response = requests.post(
        url=head_url+auth_endpoint,
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
        url=head_url+refresh_endpoint,
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


