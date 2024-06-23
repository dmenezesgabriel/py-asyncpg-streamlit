import logging

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import AsyncAdaptedQueuePool, NullPool

from src.config import get_config
from src.utils.singleton import SingletonHash

# 1. remove metaclass=SingletonHash
# 2. poolclass=NullPool

config = get_config()
logger = logging.getLogger("app")


class BaseOrm(metaclass=SingletonHash):
    def __init__(self, database_uri: str):
        logger.info("called create engine")
        self.__engine = create_async_engine(
            url=database_uri,
            pool_size=5,
            max_overflow=0,
            poolclass=AsyncAdaptedQueuePool,
        )
        self.__async_session = async_sessionmaker(bind=self.__engine)

    @property
    def engine(self) -> AsyncEngine:
        return self.__engine

    @property
    def session(self) -> AsyncSession:
        return self.__async_session()
