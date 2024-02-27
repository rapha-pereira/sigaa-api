from fastapi import FastAPI

from app.core import config
from app.router.api_v1.endpoints import api_router

app = FastAPI(
    title=config.PROJECT_NAME,
    version=config.VERSION,
    debug=config.DEBUG,
)

app.include_router(api_router, prefix=config.API_V1_PREFIX)


@app.get("/", tags=["Health check"])
async def health_check():
    return {
        "name": config.PROJECT_NAME,
        "type": "scraper-api",
        "description": "An API to access SIGAA through HTTP Requests.",
        "documentation": "/docs",
        "version": config.VERSION,
    }
