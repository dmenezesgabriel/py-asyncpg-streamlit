import logging
import logging.config
import os

from src.utils.singleton import Singleton


class Config(metaclass=Singleton):
    DATABASE_DRIVER = {
        "path": "src.db.sqlite_orm_impl",
        "class_name": "SQLiteOrmImpl",
    }
    LOG_LEVEL = "DEBUG"


class LocalConfig(Config):
    pass


class DevelopmentConfig(Config):
    DATABASE_DRIVER = {
        "path": "src.db.postgres_orm_impl",
        "class_name": "PostgresOrmImpl",
    }


class StagingConfig(Config):
    pass


class ProductionConfig(Config):
    pass


def config_factory(environment: str) -> Config:
    configs = {
        "local": LocalConfig,
        "development": DevelopmentConfig,
        "staging": StagingConfig,
        "production": ProductionConfig,
    }
    config_class = configs[environment]
    return config_class()


def get_config() -> Config:
    environment = os.getenv("ENVIRONMENT", "local")
    app_config = config_factory(environment)

    LOGGING = {
        "version": 1,
        "disable_existing_loggers": True,
        "formatters": {
            "standard": {
                "format": (
                    "[%(asctime)s] %(levelname)s "
                    "[%(name)s.%(funcName)s:%(lineno)d] "
                    "%(message)s"
                ),
                "datefmt": "%Y-%m-%d %H:%M:%S",
            }
        },
        "handlers": {
            "stdout_logger": {
                "formatter": "standard",
                "class": "logging.StreamHandler",
            }
        },
        "loggers": {
            "app": {  # root
                "level": app_config.LOG_LEVEL,
                "handlers": ["stdout_logger"],
                "propagate": False,
            }
        },
    }
    logging.config.dictConfig(LOGGING)
    return app_config
