import uvicorn
import os

from fastapi import FastAPI

from sigaa_api.core import config
from sigaa_api.router.v1.student_endpoints import router as student_router

app = FastAPI(
    title=config.PROJECT_NAME,
    version=config.VERSION,
    debug=config.DEBUG,
)
app.include_router(student_router, prefix=config.API_V1_PREFIX, tags=["student"])


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
