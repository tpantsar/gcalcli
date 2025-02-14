from _typeshed import Incomplete
from google.auth import credentials as credentials
from google.auth import exceptions as exceptions

class Credentials(credentials.ReadOnlyScoped, credentials.Credentials):
    token: Incomplete
    def __init__(
        self,
        token,
        refresh_token: Incomplete | None = None,
        id_token: Incomplete | None = None,
        token_uri: Incomplete | None = None,
        client_id: Incomplete | None = None,
        client_secret: Incomplete | None = None,
        scopes: Incomplete | None = None,
    ) -> None: ...
    @property
    def refresh_token(self): ...
    @property
    def token_uri(self): ...
    @property
    def id_token(self): ...
    @property
    def client_id(self): ...
    @property
    def client_secret(self): ...
    @property
    def requires_scopes(self): ...
    expiry: Incomplete
    def refresh(self, request) -> None: ...
    @classmethod
    def from_authorized_user_info(cls, info, scopes: Incomplete | None = None): ...
    @classmethod
    def from_authorized_user_file(cls, filename, scopes: Incomplete | None = None): ...
