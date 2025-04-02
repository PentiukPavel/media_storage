from fastapi import FastAPI
from logs.log_middleware import LoggingMiddleware


app = FastAPI(
    title="API",
    summary="API",
)
app.middleware("http")(LoggingMiddleware())


@app.get("/")
def hello():
    raise KeyError("!!!!!!!!!")
    return {"Hello": "World"}
