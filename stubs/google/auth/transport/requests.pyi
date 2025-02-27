import requests
from _typeshed import Incomplete
from google.auth import exceptions as exceptions
from google.auth import transport as transport

class _Response(transport.Response):
    def __init__(self, response) -> None: ...
    @property
    def status(self): ...
    @property
    def headers(self): ...
    @property
    def data(self): ...

class Request(transport.Request):
    session: Incomplete
    def __init__(self, session: Incomplete | None = None) -> None: ...
    def __call__(
        self,
        url,
        method: str = 'GET',
        body: Incomplete | None = None,
        headers: Incomplete | None = None,
        timeout: Incomplete | None = None,
        **kwargs,
    ): ...

class AuthorizedSession(requests.Session):
    credentials: Incomplete
    def __init__(
        self,
        credentials,
        refresh_status_codes=...,
        max_refresh_attempts=...,
        refresh_timeout: Incomplete | None = None,
        **kwargs,
    ) -> None: ...
