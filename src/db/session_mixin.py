import importlib
import logging
from typing import Any, Union

from sqlalchemy.orm import Session

from src.config import get_config
from src.db.base_orm import BaseOrm

config = get_config()
logger = logging.getLogger("app")


class DatabaseSessionMixin:
    def __enter__(self) -> Union[Session, Any]:
        module = getattr(
            importlib.import_module(config.DATABASE_DRIVER["path"]),
            config.DATABASE_DRIVER["class_name"],
        )
        orm_module = module()
        database_uri = orm_module.get_database_uri()
        # multiple create engine
        orm = orm_module.get_orm(base_orm=BaseOrm(database_uri=database_uri))
        self.orm = orm
        self.session = orm.session
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        try:
            if exc_type is not None:
                logger.error("rollback")
                self.session.rollback()

        except Exception as error:
            raise Exception(error)
        finally:
            self.session.close()
            # self.orm.engine.dispose()


def use_database_session() -> DatabaseSessionMixin:
    return DatabaseSessionMixin()
