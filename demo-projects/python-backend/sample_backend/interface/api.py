from collections.abc import AsyncIterator
import contextlib
import logging

import fastapi

from sample_backend import connectors
from sample_backend.core.config import SETTINGS

from . import routers

logger = logging.getLogger(__name__)


@contextlib.asynccontextmanager
async def app_lifespan(app: fastapi.FastAPI) -> AsyncIterator[None]:
    del app  # not used

    # TODO structured logging setup
    logging.basicConfig(level=logging.INFO)
    logger.info("App starting...")
    connectors.db.init_db_session_creator(SETTINGS.postgres_url)

    yield

    logger.info("App shutting down...")
    await connectors.db.close_db_engine()
    logger.info("Clean shutdown complete.")


app = fastapi.FastAPI(
    title=SETTINGS.app_name,
    lifespan=app_lifespan,
)


@app.get("/")
async def healthcheck() -> dict[str, str]:
    return {
        "app": SETTINGS.app_name,
        "status": "up",
    }


app.include_router(routers.notes.router, prefix="/notes")
