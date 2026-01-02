from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.infrastructure.controllers.exceptions import register_exception_handlers
from src.infrastructure.config.settings import settings
from src.infrastructure.controllers.routes.auth_routes import router as auth_router
from fastapi.middleware.cors import CORSMiddleware
from src.infrastructure.database.connection import PostgreDBConnection

@asynccontextmanager
async def lifespan(app: FastAPI):
    
    # Startup
    PostgreDBConnection.initialize()
    print("SQLAlchemy initialized successfully")
    yield

    # Shutdown
    await PostgreDBConnection.close()
    print("SQLAlchemy connections closed successfully")
    
app = FastAPI(
    title="APP Deudores API",
    description="API para gestión de deudores - FGA",
    version="1.0.0",
    debug=False,
    docs_url="/docs" if settings.is_development else None,
    redoc_url="/redoc" if settings.is_development else None,
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_exception_handlers(app)
app.include_router(auth_router)
