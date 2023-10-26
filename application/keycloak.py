from fastapi_keycloak import FastAPIKeycloak
from environs import Env

env = Env()
env.read_env()

"""
Инициализация данных keycloak.
"""

idp = FastAPIKeycloak(
    server_url="http://localhost:8282/",
    client_id=env.str('CLIENT_ID'),
    client_secret=env.str('CLIENT_SECRET_KEY'),
    admin_client_secret=env.str('ADMIN_SECRET_KEY'),
    realm=env.str('REALM'),
    callback_uri="http://0.0.0.0:8000/api/v1/callback"
)
