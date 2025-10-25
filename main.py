# api/main.py
from fastapi import FastAPI
from contextlib import asynccontextmanager
from datetime import datetime
from api.core.database import database, engine, Base
from api.core.settings import settings
from api.v1.routes import countries

Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    await database.connect()
    print("✅ Database connected")

    yield

    await database.disconnect()
    print("🛑 Database disconnected")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    lifespan=lifespan,
)

app.include_router(countries.router, prefix="/countries", tags=["Countries"])


@app.get("/status")
async def get_status():
    """Get total countries and last refresh timestamp."""
    query_total = "SELECT COUNT(*) FROM countries"
    total = await database.fetch_val(query_total)

    query_last = "SELECT MAX(last_refreshed_at) FROM countries"
    last_refreshed = await database.fetch_val(query_last)

    return {
        "total_countries": total or 0,
        "last_refreshed_at": (
            last_refreshed.isoformat() if isinstance(last_refreshed, datetime) else None
        ),
    }