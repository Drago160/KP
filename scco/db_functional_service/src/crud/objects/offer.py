from sqlalchemy import insert
from sqlalchemy.orm import Session

from crud.models import Offer
from crud.base.SelectorBase import SelectorBase

import crud.dbapi as dbapi


class OfferCRUD(SelectorBase):
    def __init__(self):
        pass

    @classmethod
    def insert_one(cls, offer_dict: dict) -> None:
        cls.insert_all([offer_dict])

    @classmethod
    def insert_all(cls, offers: list[dict]) -> None:
        if len(offers) == 0:
            print("OfferCRUD::insert_all: no offers")
            return

        # TODO: add validation
        engine = dbapi.DbEngine.get_engine()
        with Session(engine) as session:
            stmt = insert(Offer)
            with session.begin():
                session.execute(stmt, offers)
