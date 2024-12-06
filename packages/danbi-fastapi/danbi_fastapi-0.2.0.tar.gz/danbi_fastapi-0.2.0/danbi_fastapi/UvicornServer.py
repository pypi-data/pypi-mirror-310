from typing import Any
import danbi as bi
import uvicorn
from starlette.middleware.cors import CORSMiddleware

class UvicornServer(bi.plugable.IPlugin):
    ID             : str  = "danbi_fastapi.UvicornServer.UvicornServer"
    APP_NAME       : str  = "server:app"
    HOST           : str  = "0.0.0.0"
    PORT           : int  = 8000
    RELOAD         : bool = True
    SERVER_HEADER  : bool = False
    WORKS          : int  = 5
    KEY            : str  = None
    CERT           : str  = None

    def plug(self, **kwargs) -> bool:
        assert "app" in kwargs, f"set the fastapi app when create the PluginManager.\n{' '*16}ex) PluginManager(app=<your fastapi app instance>)"

        self._startUvicorn()

    def unplug(self, **kwargs) -> bool:
        print(f"{self.getName()} unpluged. {kwargs}")
    
    def _startUvicorn(self):
        uvicorn.run(
            app           = UvicornServer.APP_NAME,
            host          = UvicornServer.HOST,
            port          = UvicornServer.PORT,
            reload        = UvicornServer.RELOAD,
            server_header = UvicornServer.SERVER_HEADER,
            workers       = UvicornServer.WORKS,
            ssl_keyfile   = UvicornServer.KEY,
            ssl_certfile  = UvicornServer.CERT
        )
