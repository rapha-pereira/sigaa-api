import uvicorn
import os

from fastapi import FastAPI

from app.core import config
from app.core import exceptions
from app.router.api_v1.endpoints import api_router

app = FastAPI(
    title=config.PROJECT_NAME,
    version=config.VERSION,
    debug=config.DEBUG,
)

exceptions.include_app(app=app)
app.include_router(api_router, prefix=config.API_V1_PREFIX)


@app.get("/", tags=["health_check"])
async def health_check():
    return {
        "name": config.PROJECT_NAME,
        "type": "scraper-api",
        "description": "An API to access SIGAA through HTTP Requests.",
        "documentation": "/docs",
        "version": config.VERSION,
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))