"""
Entry for startup fastapi server
"""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

import uvicorn

from fooocusapi.utils import file_utils
from fooocusapi.routes.generate_v1 import secure_router as generate_v1
from fooocusapi.routes.generate_v2 import secure_router as generate_v2
from fooocusapi.routes.query import secure_router as query

from contextlib import asynccontextmanager
from external.runpod_status import startup_event


@asynccontextmanager
async def lifespan(app: FastAPI):
    await startup_event()
    yield


app = FastAPI(
    docs_url=None,  # Disable Swagger UI at /docs
    redoc_url=None,  # Disable ReDoc at /redoc
    openapi_url=None,  # Disable OpenAPI schema at /openapi.json
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow access from all sources
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all request headers
)


app.mount("/files", StaticFiles(directory=file_utils.output_dir), name="files")

app.include_router(query)
app.include_router(generate_v1)
app.include_router(generate_v2)


def start_app(args):
    """Start the FastAPI application"""
    file_utils.STATIC_SERVER_BASE = args.base_url + "/files/"
    uvicorn.run(
        app="fooocusapi.api:app",
        host=args.host,
        port=args.port,
        log_level=args.log_level)
