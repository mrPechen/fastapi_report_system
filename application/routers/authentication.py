import requests
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from application.keycloak import idp

router = APIRouter(prefix='/api/v1')

"""
Функция POST запроса для рефреша токена.
"""


def request_refresh_token(idp, refresh_token):
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "client_id": idp.client_id,
        "client_secret": idp.client_secret,
        "grant_type": "refresh_token",
        "refresh_token": refresh_token
    }
    return requests.post(url=idp.token_uri, headers=headers, data=data, timeout=idp.timeout)


"""
Эндпоинт для аутентификации пользователя.
"""


@router.get("/login")
async def login_redirect(request: Request):
    # Вызвать, чтобы направить пользователя на авторизацию
    redirect = RedirectResponse(idp.login_uri)
    return redirect


"""
Эндпоинт для выдачи access token. После логина перенаправляет на него.
"""


@router.get("/callback")
async def callback(request: Request):
    # Вызывается, когда пользователь успешно авторизовался
    session_state = request.query_params['session_state']
    code = request.query_params['code']
    return idp.exchange_authorization_code(session_state=session_state, code=code)


"""
Эндпоинт для рефреша токена.
"""


@router.post("/refresh")
async def refresh(request: Request):
    body = await request.json()
    refresh_token = body['refresh_token']
    return request_refresh_token(idp=idp, refresh_token=refresh_token).json()


"""
Эндпоинт логаута.
"""


@router.get("/logout", tags=["auth-flow"])
async def logout():
    return RedirectResponse(idp.logout_uri)
