from typing import Any

from sqlalchemy import select
from sqlalchemy import Result

import crud.dbapi as dbapi

from sqlalchemy.orm import Session


class SelectorBase:
    @classmethod
    def select_all_raw(
            cls,
            columns: list,
            wheres_cond: list | None = None,
            order_bys: list | None = None,
            limit: int | None = None,
    ) -> Result[Any]:
        # TODO: add validation
        if wheres_cond is None:
            wheres_cond = []
        if order_bys is None:
            order_bys = []

        engine = dbapi.DbEngine.get_engine()
        with Session(engine) as session:
            stmt = select(*columns)
            for where_cond in wheres_cond:
                stmt = stmt.where(where_cond)

            for order_by_cond in order_bys:
                stmt = stmt.order_by(order_by_cond)

            if limit is not None:
                stmt = stmt.limit(limit)

            with session.begin():
                result_set = session.execute(stmt)

        return result_set

    @classmethod
    def select_all(
            cls,
            columns: list,
            wheres_cond: list | None = None,
            order_bys: list | None = None,
            limit: int | None = None,
    ) -> list[Any] | None:
        result_set = cls.select_all_raw(
            columns,
            wheres_cond=wheres_cond,
            order_bys=order_bys,
            limit=limit,
        )

        if result_set is None:
            return None

        res_rows = []
        for raw_row in result_set:
            res_rows.append(raw_row)

        return res_rows

    @classmethod
    def select_one_raw(
            cls,
            columns: list,
            wheres_cond: list | None = None,
            order_bys: list | None = None,
    ) -> Result[Any]:
        result_set = cls.select_all_raw(
            columns,
            wheres_cond=wheres_cond,
            order_bys=order_bys,
            limit=1
        )

        return result_set

    @classmethod
    def select_one(
            cls,
            columns: list,
            wheres_cond: list | None = None,
            order_bys: list | None = None,
    ) -> Any:
        result_set = cls.select_one_raw(
            columns,
            wheres_cond=wheres_cond,
            order_bys=order_bys,
        )

        return result_set.one_or_none()
