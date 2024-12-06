from typing import Any
import danbi as bi
from starlette.middleware.cors import CORSMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.gzip import GZipMiddleware

class Middleware(bi.plugable.IPlugin):
    ID                 : str  = "danbi_fastapi.Middleware.Middleware"

    ORIGIN             : bool = False
    ORIGIN_LIST        : list = []
    ORIGIN_CREDENTIALS : bool = True
    ORIGIN_METHODS     : list = ["*"]
    ORIGIN_HEADERS     : list = ["*"]

    HTTPS_REDIRECT     : bool = False

    TRUST_HOST         : bool = False
    TRUST_LIST         : list = []

    GZIP               : bool = False
    GZIP_MIN_SIZE      : int = 1000

    def plug(self, **kwargs) -> bool:
        assert "app" in kwargs, f"set the fastapi app when create the PluginManager.\n{' '*16}ex) PluginManager(app=<your fastapi app instance>)"

        app = kwargs["app"]
        if (Middleware.ORIGIN):
            self._setOrigins(app)
        if (Middleware.HTTPS_REDIRECT):
            app.add_middleware(HTTPSRedirectMiddleware)
        if (Middleware.TRUST_HOST):
            app.add_middleware(TrustedHostMiddleware, allowed_hosts = [Middleware.TRUST_LIST])
        if (Middleware.GZIP):
            app.add_middleware(GZipMiddleware, minimum_size = Middleware.GZIP_MIN_SIZE)

    def unplug(self, **kwargs) -> bool:
        print(f"{self.getName()} unpluged. {kwargs}")
        
    def _setOrigins(self, app):
        app.add_middleware(
            CORSMiddleware,
            allow_origins     = Middleware.ORIGIN_LIST,
            allow_credentials = Middleware.ORIGIN_CREDENTIALS,
            allow_methods     = Middleware.ORIGIN_METHODS,
            allow_headers     = Middleware.ORIGIN_HEADERS
        )

