import os
import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from .api.app_status import status_router
from .api.v1.videos.views import videos_router
from .external.kafka.kafka_utils import close_kafka_connection, init_kafka_connection

app = FastAPI(
    title="Video Produce Service V1",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    version=os.getenv("APP_VERSION", default="DEV"),
)

logger_config = {
    "handlers": [
        {
            "sink": sys.stdout,
            "format": "<level>{level}: {message}</level>",
        }
    ]
}


def create_app():
    logger.configure(**logger_config)

    app.include_router(status_router)
    app.include_router(videos_router)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_event_handler("startup", init_kafka_connection)
    app.add_event_handler("shutdown", close_kafka_connection)

    return app
