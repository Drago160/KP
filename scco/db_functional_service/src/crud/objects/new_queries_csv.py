from typing import Any

from sqlalchemy import insert
from sqlalchemy import select
from sqlalchemy import Result

from sqlalchemy.orm import Session

from crud.models import NewQueriesCsv

import crud.dbapi as dbapi

from crud.type_map import CsvId

from crud.base.SelectorBase import SelectorBase


class NewQueriesCsvCRUD(SelectorBase):
    def __init__(self):
        pass

    @classmethod
    def insert_one(cls, customer_service: dict) -> None:
        cls.insert_all([customer_service])

    @classmethod
    def insert_all(cls, new_queries_csvs: list[dict]) -> list[CsvId]:
        if len(new_queries_csvs) == 0:
            print("CustomerServiceCRUD::insert_all: no new_queries_csvs")
            return []

        # TODO: add validation
        engine = dbapi.DbEngine.get_engine()
        with Session(engine) as session:
            stmt = (insert(NewQueriesCsv)
                    .values(new_queries_csvs)
                    .returning(NewQueriesCsv.csv_id))
            with session.begin():
                result_set = session.execute(stmt)

        res = []
        for row in result_set:
            res.append(row[0])

        return res
