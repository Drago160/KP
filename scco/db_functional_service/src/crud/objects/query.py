from sqlalchemy import insert

from sqlalchemy.orm import Session

from crud.models import Query

import crud.dbapi as dbapi

from crud.type_map import QueryId

from crud.base.SelectorBase import SelectorBase


class QueryCRUD(SelectorBase):
    def __init__(self):
        pass

    @classmethod
    def insert_one(cls, query: dict) -> QueryId:
        res_list = cls.insert_all([query])
        return res_list[0]

    @classmethod
    def insert_all(cls, queries: list[dict]) -> list[QueryId]:
        if len(queries) == 0:
            print("QueryCRUD::insert_all: no queries")
            return []

        # TODO: add validation
        engine = dbapi.DbEngine.get_engine()
        with Session(engine) as session:
            stmt = (insert(Query)
                    .values(queries)
                    .returning(Query.query_id))
            with session.begin():
                result_set = session.execute(stmt)

        res = []
        for row in result_set:
            res.append(row[0])

        return res
