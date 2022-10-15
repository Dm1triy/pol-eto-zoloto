import os
import sys

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from loguru import logger

from .api.app_status import status_router
from .api.v1.stream.views import stream_router
from .external.kafka.kafka_utils import close_kafka_connection, init_kafka_connection

templates = Jinja2Templates(directory="templates")
app = FastAPI(
    title="Video Consumer Service V1",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    version=os.getenv("APP_VERSION", default="DEV"),
)

templates = Jinja2Templates(directory="src/video_consume_service/templates")


@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


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
    app.include_router(stream_router)

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
