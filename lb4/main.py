from contextlib import asynccontextmanager
from pathlib import Path

from aerich import Command
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from tortoise import Tortoise
from tortoise.contrib.fastapi import RegisterTortoise

from lb4 import config
from lb4.routes import auth, categories, products, orders, reviews
from lb4.utils.multiple_errors_exception import MultipleErrorsException


@asynccontextmanager
async def migrate_and_connect_orm(app_: FastAPI):  # pragma: no cover
    if ":memory:" not in config.DB_CONNECTION_STRING:
        migrations_dir = "data/migrations"

        command = Command({
            "connections": {"default": config.DB_CONNECTION_STRING},
            "apps": {"models": {"models": ["lb4.models", "aerich.models"], "default_connection": "default"}},
        }, location=migrations_dir)
        await command.init()
        if Path(migrations_dir).exists():
            await command.migrate()
            await command.upgrade(True)
        else:
            await command.init_db(True)
        await Tortoise.close_connections()

    async with RegisterTortoise(
            app=app_,
            db_url=config.DB_CONNECTION_STRING,
            modules={"models": ["lb4.models"]},
            generate_schemas=True,
    ):
        yield


app = FastAPI(lifespan=migrate_and_connect_orm)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth.router)
app.include_router(categories.router)
app.include_router(products.router)
app.include_router(orders.router)
app.include_router(reviews.router)


@app.exception_handler(MultipleErrorsException)
async def multiple_errors_exception_handler(_, exc: MultipleErrorsException) -> JSONResponse:
    return JSONResponse({
        "errors": exc.messages,
    }, status_code=exc.status_code)
