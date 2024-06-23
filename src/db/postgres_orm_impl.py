import os


class PostgresOrmImpl:
    def get_orm(self, base_orm):
        return base_orm

    def get_database_uri(self) -> str:
        db_user = os.getenv("POSTGRES_USER")
        db_password = os.getenv("POSTGRES_PASSWORD")
        db_name = os.getenv("POSTGRES_DB")
        db_host = "db"
        db_port = 5432
        database_uri = f"postgresql+asyncpg://{db_user}:{db_password}"
        database_uri += f"@{db_host}:{db_port}"
        database_uri += f"/{db_name}"
        return database_uri
