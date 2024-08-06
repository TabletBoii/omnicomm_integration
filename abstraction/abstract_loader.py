from abc import abstractmethod, ABC
from sqlalchemy.orm import Session
import os
from structs.dataclasses import JwtClaims


class AbstractLoader(ABC):

    def __init__(self, db_session: Session, auth_data: list[JwtClaims]):
        self.db_session: Session = db_session
        self.auth_data: list[JwtClaims] = auth_data
        self.url: str = os.getenv("OMNICOMM_HEAD_URL")
        # self.bearer_auth: dict = {"Authorization": f"JWT {self.auth_data.jwt}"}

    @property
    def jwt(self):
        return self.auth_data
