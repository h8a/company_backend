import aioodbc

from employees.web.app import settings

class UnitOfWork:

    def __init__(self) -> None:
        self.server = settings.db_server
        self.database = settings.db_name
        self.username = settings.db_username
        self.password = settings.db_password

    async def __aenter__(self):
        str_connection = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={self.server};DATABASE={self.database};UID={self.username};PWD={self.password};Encrypt=no;'
        self.session = await aioodbc.connect(dsn=str_connection, echo=True, autocommit=False)
        return self

    async def __aexit__(self, exc_type, exc_val, traceback):
        if exc_type is not None:
            await self.rollback()
            await self.session.close()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
