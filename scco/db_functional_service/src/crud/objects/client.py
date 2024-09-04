from sqlalchemy import insert
from sqlalchemy import select

from sqlalchemy.orm import Session

from crud.models import Client

import crud.dbapi as dbapi

from crud.type_map import ClientId

from crud.base.SelectorBase import SelectorBase


class ClientCRUD(SelectorBase):
    def __init__(self):
        pass

    @classmethod
    def insert_one(cls, client: dict) -> None:
        cls.insert_all([client])

    @classmethod
    def insert_all(cls, clients: list[dict]) -> None:
        if len(clients) == 0:
            print("ClientCRUD::insert_all: no clients")
            return

        # TODO: add validation
        engine = dbapi.DbEngine.get_engine()
        with Session(engine) as session:
            stmt = insert(Client).values(clients)
            with session.begin():
                session.execute(stmt)

    @classmethod
    def contain(cls, client_id: ClientId) -> bool:
        engine = dbapi.DbEngine.get_engine()
        with Session(engine) as session:
            stmt = (select(Client.client_id)
                    .select_from(Client)
                    .where(Client.client_id == client_id)
                    .limit(1))
            res = session.scalars(stmt).one_or_none()

        return res is not None
