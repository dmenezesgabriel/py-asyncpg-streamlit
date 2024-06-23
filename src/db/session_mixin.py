import importlib
import logging
from typing import Any, Union

from sqlalchemy.ext.asyncio import AsyncSession

from src.config import get_config
from src.db.base_orm import BaseOrm

config = get_config()
logger = logging.getLogger("app")


class DatabaseSessionMixin:
    async def __aenter__(self) -> Union[AsyncSession, Any]:
        module = getattr(
            importlib.import_module(config.DATABASE_DRIVER["path"]),
            config.DATABASE_DRIVER["class_name"],
        )
        orm_module = module()
        database_uri = orm_module.get_database_uri()
        # multiple create engine
        orm = orm_module.get_orm(base_orm=BaseOrm(database_uri=database_uri))
        self.session = orm.session
        return self.session

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        try:
            if exc_type is not None:
                logger.error("rollback")
                await self.session.rollback()

        except Exception as error:
            raise Exception(error)
        finally:
            await self.session.close()


def use_database_session() -> DatabaseSessionMixin:
    return DatabaseSessionMixin()
