from typing import Any

from fastapi import FastAPI

from application.database import models
from application.database.db_root import engine
from application.keycloak import idp
from application.routers import authentication, report_routers

app = FastAPI()

idp.add_swagger_config(app)


@app.on_event('startup')
async def init_models() -> Any:
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)


app.include_router(authentication.router)
app.include_router(report_routers.router)
