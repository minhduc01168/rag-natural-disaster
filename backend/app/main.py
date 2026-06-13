from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.api.router import api_router

settings = get_settings()

from contextlib import asynccontextmanager
from app.db.session import engine, Base, SessionLocal
from app.models.user import UserRole
from app.crud.crud_user import get_user_by_email, create_user
from app.schemas.user import UserCreate

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize DB tables
    Base.metadata.create_all(bind=engine)
    
    # Seed Admin User
    db = SessionLocal()
    try:
        admin_email = "admin@terraalert.com"
        admin_user = get_user_by_email(db, email=admin_email)
        if not admin_user:
            print("Seeding default admin user...")
            admin_in = UserCreate(
                email=admin_email,
                password="admin", # Default password, will be hashed
                full_name="System Administrator",
                phone="0900000000",
                location="Hà Nội"
            )
            create_user(db, user=admin_in, role=UserRole.ADMIN)
            print("Admin user created successfully.")
    finally:
        db.close()
    
    yield
    # Cleanup on shutdown if needed

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
