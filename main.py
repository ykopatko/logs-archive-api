from fastapi import FastAPI

from api import api_router
from core.database import engine, Base
from fastapi_pagination import add_pagination

app = FastAPI()

app.include_router(api_router)
add_pagination(app)


@app.on_event("startup")
async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
