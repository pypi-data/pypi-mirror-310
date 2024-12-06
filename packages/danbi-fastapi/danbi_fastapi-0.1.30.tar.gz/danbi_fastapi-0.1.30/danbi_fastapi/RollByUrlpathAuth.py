from gc import callbacks
from typing import Callable, Dict
from async_lru import alru_cache

from fastapi import Request
from numpy import isin
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response, JSONResponse
from pydantic_settings import BaseSettings

from fastapi.encoders import jsonable_encoder


from danbi import plugable

class Settings(BaseSettings):
    NAME                   : str  = "danbi_fastapi.RollByUrlpathAuth.RollByUrlpathAuth"

    SESSION_SECRET_KEY  : str = "secret"
    SESSION_AUTH_KEY    : str = "is_login"
    SESSION_COOKIE_NAME : str = "SID"
    SESSION_MAX_AGE     : int = 60 * 5
    ROLE_BY_URLPATH     : Dict = {}
    AUTH_FAIL_CALLBACK  : Callable = None

class UrlpathMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, auth_key: str, rule: dict, callback: Callable):
        super().__init__(app)
        self._callback = callback
        self._auth_key = auth_key
        for path, roles in rule.items():
            if isinstance(roles, str):
                rule[path] = set(roles.split(","))
        self._rule: dict = rule
    
    @alru_cache(maxsize=1024)
    async def _rollCheck(self, url: str, **session):
        for path, roles in self._rule.items():
            if url.startswith(path): # exists auth setting for the url path
                if self._auth_key in session: # authentication done
                    if len(set(session[self._auth_key].split(",")) & roles) > 0: # have a authorization
                        return True, True
                    else: # no authorization
                        return True, False
                else: # no Authentication
                    return False, False

        return True, True

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        authentication, authorization = await self._rollCheck(request.url.path, **request.session)
        if all([authentication, authorization]):
            return await call_next(request)
        else:
            resp = self._callback(request, authentication, authorization)
            # json_code = jsonable_encoder(resp)
            # return JSONResponse(content=json_code)
            return resp

class RollByUrlpathAuth(plugable.IPlugin):
    settings = Settings()

    def plug(self, **kwargs) -> bool:
        assert "app" in kwargs, f"set the fastapi app when create the PluginManager.\n{' '*16}ex) PluginManager(app=<your fastapi app instance>)"

        app = kwargs["app"]
        app.add_middleware(
            UrlpathMiddleware,
            auth_key = RollByUrlpathAuth.settings.SESSION_AUTH_KEY,
            rule = RollByUrlpathAuth.settings.ROLE_BY_URLPATH,
            callback = RollByUrlpathAuth.settings.AUTH_FAIL_CALLBACK
        )
        app.add_middleware(
            SessionMiddleware,
            secret_key = RollByUrlpathAuth.settings.SESSION_SECRET_KEY,
            session_cookie = RollByUrlpathAuth.settings.SESSION_COOKIE_NAME,
            max_age = RollByUrlpathAuth.settings.SESSION_MAX_AGE
        )

    def unplug(self, **kwargs) -> bool:
        print(f"{self.getName()} unpluged. {kwargs}")
    
    def __repr__(self):
        return f"{self.__module__}.{self.__class__.__name__}"
