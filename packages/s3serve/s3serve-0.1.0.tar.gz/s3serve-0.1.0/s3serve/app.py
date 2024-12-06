from pathlib import Path

from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from s3serve.routes import buckets

app = FastAPI(title='S3 Serve Web')
app_api = FastAPI(title='S3 Serve API')

app.mount('/api/v1', app_api, name='api')
app.mount('/', StaticFiles(directory=Path(__file__).resolve().parent.joinpath('web', 'dist'), html=True), name='static')

app_api.include_router(buckets.router)
