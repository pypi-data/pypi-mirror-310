from importlib.resources import Package
from typing import Any, Union

from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise
from pydantic_settings import BaseSettings

from danbi import plugable
from danbi.mapping import Jinja2Mapper
from danbi.database import IConnectionManager, ConnMngPsql, DBPsql

class Settings(BaseSettings):
    NAME                  : str  = "danbi_fastapi.TortoiseORM.TortoiseORM"

    DB_ENGINE: str                      = "tortoise.backends.asyncpg"
    DB_HOST: str                        = ""
    DB_NAME: str                        = ""
    DB_USER: str                        = ""
    DB_PASS: str                        = ""
    DB_PORT: int                        = 5432
    DB_POOL_MIN: int                    = 5
    DB_POOL_MAX: int                    = 10

    ORM_MODELS: list                    = []
    ORM_GENERATE_SCHEMAS                = True

    JINJA2MAPPER: bool                  = False
    JINJA2MAPPER_CONF_PACKAGE: str      = None
    JINJA2MAPPER_CONFS: list            = []
    JINJA2MAPPER_NAMESPACE: str         = None
    JINJA2MAPPER_TAG: Union[str, float] = None

class TortoiseORM(plugable.IPlugin):
    settings = Settings()

    def plug(self, **kwargs) -> bool:
        assert "app" in kwargs, f"set the fastapi app when create the PluginManager.\n{' '*16}ex) PluginManager(app=<your fastapi app instance>)"

        app = kwargs["app"]

        self._connect(app)
        if TortoiseORM.settings.JINJA2MAPPER:
            self._raw_connect(app)
    
    def unplug(self, **kwargs) -> bool:
        print(f"{self.getName()} unpluged. {kwargs}")
    
    def _connect(self, app):
        conn_mng = ConnMngTortoise().connect(app=app)

    def _raw_connect(self, app):
        psql = ConnMngPsql(
            user=TortoiseORM.settings.DB_USER,
            password=TortoiseORM.settings.DB_PASS,
            host=TortoiseORM.settings.DB_HOST,
            port=TortoiseORM.settings.DB_PORT,
            database=TortoiseORM.settings.DB_NAME
        ).connect(minconn=TortoiseORM.settings.DB_POOL_MIN, maxconn=TortoiseORM.settings.DB_POOL_MAX)
        mapper = Jinja2Mapper(
            TortoiseORM.settings.JINJA2MAPPER_CONFS,
            TortoiseORM.settings.JINJA2MAPPER_NAMESPACE,
            TortoiseORM.settings.JINJA2MAPPER_TAG,
            TortoiseORM.settings.JINJA2MAPPER_CONF_PACKAGE
        )
        app.tortoise = DBPsql(psql, mapper)

class ConnMngTortoise(IConnectionManager):
    def connect(self, **kwargs) -> IConnectionManager:
        app = kwargs["app"]
        
        try:
            config = {
                "connections": {
                    "danbi": {
                        "engine": TortoiseORM.settings.DB_ENGINE,
                        "credentials": {
                            "host": TortoiseORM.settings.DB_HOST,
                            "database": TortoiseORM.settings.DB_NAME,
                            "user": TortoiseORM.settings.DB_USER,
                            "password": TortoiseORM.settings.DB_PASS,
                            "port": TortoiseORM.settings.DB_PORT
                        },
                        "minsize": TortoiseORM.settings.DB_POOL_MIN,
                        "maxsize": TortoiseORM.settings.DB_POOL_MAX
                    }
                },
                "apps": {
                    "models": {
                        "models": TortoiseORM.settings.ORM_MODELS,
                        "default_connection": "danbi"
                    }
                }
            }

            register_tortoise(
                app,
                config=config,
                generate_schemas=TortoiseORM.settings.ORM_GENERATE_SCHEMAS,
                add_exception_handlers=True
            )
            return self.instance
        except Exception:
            raise
    
    def isConnect(self) -> bool:
        ...

    def close(self, **kwargs) -> None:
        ...
    
    def getConnection(self, auto_commit=True, **kwargs):
        try:
            return Tortoise.get_connection("danbi")
        except Exception:
            raise
    
    def releaseConnection(self, conn) -> None:
        ...

