from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.part_router import router as part_router
from app.api.export import router as export_router
from app.api.health_check import router as health_router
from app.core.settings import settings

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
print("APP DB:", settings.DATABASE_URL)
app.include_router(part_router)
app.include_router(export_router)
app.include_router(health_router)