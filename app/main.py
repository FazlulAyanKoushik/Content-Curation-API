
import asyncio
import logging
import subprocess
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.accounts.models.user import User, RoleEnum
from app.accounts.routes.users import router as accounts_router, admin_router
from app.accounts.services.auth import get_password_hash
from app.config.database import engine, AsyncSessionLocal
from app.config.settings import settings

from decouple import config

from app.content_AI.routers.admin import admin_content_router
from app.content_AI.routers.content import content_router
from app.content_AI.routers.search import search_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)


# Superuser details
SUPER_USERNAME = config("SUPER_USERNAME", default="admin")
SUPER_PASSWORD = config("SUPER_PASSWORD", default="JBC@2025")
SUPER_EMAIL = config("SUPER_EMAIL", default="jbc.sevensix@gmail.com")

async def apply_alembic_migrations():
    """Run Alembic migrations automatically at startup using subprocess."""
    logger.info("Applying Alembic migrations...")
    loop = asyncio.get_event_loop()
    # Alembic must be configured to read DB config from your env/files/config
    res = await loop.run_in_executor(
        None,
        lambda: subprocess.run(
            ["alembic", "upgrade", "head"],
            capture_output=True,
            text=True,
            check=False,
        )
    )
    if res.returncode == 0:
        logger.info("Alembic migrations applied successfully.")
    else:
        logger.error("Alembic failed: %s\n%s", res.stdout, res.stderr)
        raise RuntimeError("Alembic migration failed")

async def create_admin_if_needed():
    """Create an admin user if none exists."""
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            # Replace 'role' and 'admin' with your actual admin RoleEnum/member if necessary
            # Assumes User model has a `role` attribute and role value for admin is 'admin'
            # If using enums, change accordingly!
            User.__table__.select().where(User.role == 'admin')  # Or RoleEnum.ADMIN if you use enums
        )
        admin_user = result.first()
        if admin_user:
            logger.info("Admin user already exists.")
            return

        logger.info("No admin found. Creating default admin user.")
        # Customize these as needed, ensure password hashing if required by your auth logic!
        admin_user = User(
            username=SUPER_USERNAME,
            email=SUPER_EMAIL,
            hashed_password=get_password_hash(SUPER_PASSWORD),  # In production, hash this!
            role=RoleEnum.ADMIN
        )
        session.add(admin_user)
        await session.commit()
        logger.info("Default admin user created.")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1. Apply migrations
    await apply_alembic_migrations()

    # 2. Create admin user if needed
    try:
        await create_admin_if_needed()
    except Exception as exc:
        logger.error(f"Failed to check/create admin user: {exc}")

    yield

    await engine.dispose()

app = FastAPI(
    title="AI Content curation API",
    description="REST API for AI Content curation application. Demonstrates backend expertise, modern best practices, and scalable architecture.",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(accounts_router, prefix="/accounts", tags=["Accounts"])
app.include_router(admin_router, prefix="/admin", tags=["Admin"])
app.include_router(content_router, prefix="/content", tags=["Content"])
app.include_router(search_router, prefix="/search", tags=["Search"])
app.include_router(admin_content_router, prefix="/admin/content", tags=["Admin Content"])

@app.get("/", tags=["Root"])
async def root():
    return {"message": "Welcome to the AI Content curation API. See /docs for interactive API documentation."}
