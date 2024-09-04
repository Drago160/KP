from sqlalchemy import insert
from sqlalchemy import update

from sqlalchemy.orm import Session

from crud.models import Customer

import crud.dbapi as dbapi

from crud.base.SelectorBase import SelectorBase


class CustomerCRUD(SelectorBase):
    def __init__(self):
        pass

    @classmethod
    def insert_one(cls, customer: dict) -> None:
        cls.insert_all([customer])

    @classmethod
    def insert_all(cls, customers: list[dict]) -> None:
        if len(customers) == 0:
            print("CustomerCRUD::insert_all: no customers")
            return

        # TODO: add validation
        engine = dbapi.DbEngine.get_engine()
        with Session(engine) as session:
            stmt = insert(Customer).values(customers)
            with session.begin():
                session.execute(stmt)

    @classmethod
    def update(
            cls,
            new_vals: dict,
            wheres_cond: list | None = None,
    ) -> None:
        if len(new_vals) == 0:
            print("CustomerCRUD::update_one: no values")
            return

        # TODO: add validation
        engine = dbapi.DbEngine.get_engine()
        with Session(engine) as session:
            stmt = update(Customer)
            for where_cond in wheres_cond:
                stmt = stmt.where(where_cond)

            stmt = stmt.values(new_vals)
            with session.begin():
                session.execute(stmt)
