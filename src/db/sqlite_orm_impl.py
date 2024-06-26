class SQLiteOrmImpl:
    def get_orm(self, base_orm):
        return base_orm

    def get_database_uri(self) -> str:
        return "sqlite:///./database.db"
