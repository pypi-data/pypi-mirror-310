from typing import Any

import uvicorn
from starlette.middleware.cors import CORSMiddleware
from pydantic_settings import BaseSettings

from danbi import plugable

class Settings(BaseSettings):
    NAME                   : str  = "danbi_fastapi.UvicornServer.UvicornServer"

    APP_NAME       : str  = "server:app"
    HOST           : str  = "0.0.0.0"
    PORT           : int  = 8000
    RELOAD         : bool = True
    DEBUG          : bool = True
    SERVER_HEADER  : bool = False
    WORKS          : int  = 5
    KEY            : str  = None
    CERT           : str  = None

class UvicornServer(plugable.IPlugin):
    settings = Settings()

    def plug(self, **kwargs) -> bool:
        assert "app" in kwargs, f"set the fastapi app when create the PluginManager.\n{' '*16}ex) PluginManager(app=<your fastapi app instance>)"

        self._startUvicorn()

    def unplug(self, **kwargs) -> bool:
        print(f"{self.getName()} unpluged. {kwargs}")
        
    def _startUvicorn(self):
        uvicorn.run(
            app           = UvicornServer.settings.APP_NAME,
            host          = UvicornServer.settings.HOST,
            port          = UvicornServer.settings.PORT,
            reload        = UvicornServer.settings.RELOAD,
            debug         = UvicornServer.settings.DEBUG,
            server_header = UvicornServer.settings.SERVER_HEADER,
            workers       = UvicornServer.settings.WORKS,
            ssl_keyfile   = UvicornServer.settings.KEY,
            ssl_certfile  = UvicornServer.settings.CERT
        )
