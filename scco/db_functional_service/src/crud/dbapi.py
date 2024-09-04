from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

import util.app_config as app_cfg


# Engine URL: "postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
class DbEngine:
    _engine: Engine = None

    @classmethod
    def get_engine(cls) -> Engine:
        if cls._engine is None:
            cls._engine = cls._create_db_engine()
        return cls._engine

    @staticmethod
    def _create_db_engine() -> Engine:
        postgres_user = app_cfg.POSTGRES_USER
        postgres_password = app_cfg.POSTGRES_PASSWORD
        postgres_port = app_cfg.POSTGRES_PORT
        postgres_db = app_cfg.POSTGRES_DB

        if app_cfg.is_on_host():
            postgres_host = "localhost"
        else:
            postgres_host = app_cfg.POSTGRES_FS_ALIAS
        print(f"postgres_host = {postgres_host}")

        url = (f"postgresql+psycopg2://{postgres_user}:{postgres_password}@"
               f"{postgres_host}:{postgres_port}/{postgres_db}")

        return create_engine(
            url,
            # pool_recycle=3600,
            echo=True,
            echo_pool=True,
        )
