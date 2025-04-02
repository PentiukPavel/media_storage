from fastapi import FastAPI

from logs.log_middleware import LoggingMiddleware
from api.routers import v1_main_router


app = FastAPI(
    title="Сервис по загрузке медиа файлов от пользователей.",
    summary="API API для сервиса по загрузке медиа файлов от пользователей.",
)
app.middleware("http")(LoggingMiddleware())

app.include_router(v1_main_router)
