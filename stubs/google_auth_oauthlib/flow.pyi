import wsgiref.simple_server

from _typeshed import Incomplete
from google.oauth2.credentials import Credentials

class Flow:
    client_type: Incomplete
    client_config: Incomplete
    oauth2session: Incomplete
    code_verifier: Incomplete
    autogenerate_code_verifier: Incomplete
    def __init__(
        self,
        oauth2session,
        client_type,
        client_config,
        redirect_uri: Incomplete | None = None,
        code_verifier: Incomplete | None = None,
        autogenerate_code_verifier: bool = True,
    ) -> None: ...
    @classmethod
    def from_client_config(cls, client_config, scopes, **kwargs): ...
    @classmethod
    def from_client_secrets_file(cls, client_secrets_file, scopes, **kwargs): ...
    @property
    def redirect_uri(self): ...
    @redirect_uri.setter
    def redirect_uri(self, value) -> None: ...
    def authorization_url(self, **kwargs): ...
    def fetch_token(self, **kwargs): ...
    @property
    def credentials(self): ...
    def authorized_session(self): ...

class InstalledAppFlow(Flow):
    redirect_uri: Incomplete
    def run_local_server(
        self,
        host: str = 'localhost',
        bind_addr: Incomplete | None = None,
        port: int = 8080,
        authorization_prompt_message=...,
        success_message=...,
        open_browser: bool = True,
        redirect_uri_trailing_slash: bool = True,
        timeout_seconds: Incomplete | None = None,
        token_audience: Incomplete | None = None,
        browser: Incomplete | None = None,
        **kwargs,
    ) -> Credentials: ...

class _WSGIRequestHandler(wsgiref.simple_server.WSGIRequestHandler):
    def log_message(self, format, *args) -> None: ...

class _RedirectWSGIApp:
    last_request_uri: Incomplete
    def __init__(self, success_message) -> None: ...
    def __call__(self, environ, start_response): ...
