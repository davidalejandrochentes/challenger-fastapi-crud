from fastapi import FastAPI
from starlette.status import HTTP_200_OK
from starlette.staticfiles import StaticFiles

app = FastAPI()

@app.get("/", status_code=HTTP_200_OK)
async def root():
    return "API is running"