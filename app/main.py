"""Application entry point. Shared contract: it only registers routers."""

from fastapi import FastAPI

from app import models  # noqa: F401  (import so the tables are registered)
from app.db import Base, engine
from app.features import cancel, create, list_mine


def create_app() -> FastAPI:
    Base.metadata.create_all(engine)
    app = FastAPI(title="ReservaBCN API")
    app.include_router(create.router)
    app.include_router(list_mine.router)
    app.include_router(cancel.router)
    return app


app = create_app()
