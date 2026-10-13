
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routes.routeMain import api_router


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_db_client():
    from app.config.db import connect_to_mongo
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_db_client():
    from app.config.db import close_mongo_connection
    await close_mongo_connection()

app.include_router(api_router, prefix=f"{settings.API_V1_STR}")

@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI MongoDB Project"}
