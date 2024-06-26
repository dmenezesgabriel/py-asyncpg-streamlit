import logging

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import QueuePool

from src.config import get_config
from src.utils.singleton import SingletonHash

config = get_config()
logger = logging.getLogger("app")


class BaseOrm(metaclass=SingletonHash):
    def __init__(self, database_uri: str):
        logger.info("called create engine")
        self.__engine = create_engine(
            url=database_uri,
            pool_size=5,
            max_overflow=0,
            poolclass=QueuePool,
        )
        self.__session = sessionmaker(bind=self.__engine)

    @property
    def engine(self) -> Engine:
        return self.__engine

    @property
    def session(self) -> Session:
        return self.__session()
