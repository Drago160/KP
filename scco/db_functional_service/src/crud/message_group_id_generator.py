from sqlalchemy.orm import Session

from sqlalchemy import select
from sqlalchemy import func as sqlfunc

import crud.dbapi as dbapi

from crud.models import Query

from crud.type_map import MessageGroupId


class IdGenerator:
    max_message_group_id: MessageGroupId = None

    @classmethod
    def reserve_id(cls):
        # TODO: add mutex.
        if cls.max_message_group_id is None:
            cls.max_message_group_id = cls._create_message_group_id()
        cls.max_message_group_id += 1
        return cls.max_message_group_id

    @staticmethod
    def _create_message_group_id() -> MessageGroupId:
        engine = dbapi.DbEngine.get_engine()
        with Session(engine) as session:
            stmt = (select(sqlfunc.max(Query.message_group_id))
                    .select_from(Query))
            # stmt = select(sqlfunc.max(Query.message_group_id))
            res = session.scalars(stmt).one_or_none()
            if res is None:
                res = 0
            return res
