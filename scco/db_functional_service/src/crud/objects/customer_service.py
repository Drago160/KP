from sqlalchemy import insert
from sqlalchemy import delete

from sqlalchemy.orm import Session

from crud.models import CustomerService
from crud.base.SelectorBase import SelectorBase

import crud.dbapi as dbapi


class CustomerServiceCRUD(SelectorBase):
    def __init__(self):
        pass

    @classmethod
    def insert_one(cls, customer_service: dict) -> None:
        cls.insert_all([customer_service])

    @classmethod
    def insert_all(cls, customer_services: list[dict]) -> None:
        if len(customer_services) == 0:
            print("CustomerServiceCRUD::insert_all: no customer_services")
            return

        # TODO: add validation
        engine = dbapi.DbEngine.get_engine()
        with Session(engine) as session:
            stmt = insert(CustomerService).values(customer_services)
            with session.begin():
                session.execute(stmt)

    @classmethod
    def delete(
            cls,
            wheres_cond: list,
    ) -> None:
        # TODO: add validation
        if wheres_cond is []:
            print("CustomerServiceCRUD::delete: no wheres_cond provided")
            return

        engine = dbapi.DbEngine.get_engine()
        with Session(engine) as session:
            stmt = delete(CustomerService)
            for where_cond in wheres_cond:
                stmt = stmt.where(where_cond)

            with session.begin():
                session.execute(stmt)
