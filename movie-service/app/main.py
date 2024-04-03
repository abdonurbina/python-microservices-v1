from fastapi import FastAPI

from app.api.movies import movies
from app.api.db import database
# from pydantic import SecretStr
# from fastapi_keycloak import FastAPIKeycloak, OIDCUser, UsernamePassword, HTTPMethod, KeycloakUser, KeycloakGroup

app = FastAPI(openapi_url="/api/v1/movies/openapi.json", docs_url="/api/v1/movies/docs")

# idp = FastAPIKeycloak(
#     server_url="http://localhost:8080/auth",
#     client_id="test_client",
#     client_secret="8ac27a39-fa84-46b9-8c30-b485056e0cea",
#     admin_client_secret="BIcczGsZ6I8W5zf0rZg5qSexlloQLPKB",
#     realm="test",
#     callback_uri="http://localhost:8001/callback"
# )
# idp.add_swagger_config(app)

@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

# # Auth Flow
#
# @app.get("/login-link", tags=["auth-flow"])
# def login_redirect():
#     return idp.login_uri
#
#
# @app.get("/callback", tags=["auth-flow"])
# def callback(session_state: str, code: str):
#     return idp.exchange_authorization_code(session_state=session_state, code=code)
#
#
# @app.get("/logout", tags=["auth-flow"])
# def logout():
#     return idp.logout_uri

app.include_router(movies, prefix='/api/v1/movies', tags=['movies'])
