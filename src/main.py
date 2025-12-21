from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routers.user_router import router as user_router
from src.config.settings import settings
from src.database.db import init_models
import asyncio
import uvicorn

app = FastAPI(
    title = settings.app_name,
    debug=settings.debug,
    docs_url="/docs"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins = settings.cors_origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

app.include_router(user_router)

if __name__ == "__main__":
    asyncio.run(init_models())
    uvicorn.run(
        "src.main:app", host="127.0.0.1", port=8000, reload=True
)