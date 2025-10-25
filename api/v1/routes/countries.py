# api/v1/routes/countries.py
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import FileResponse
from typing import Optional
from api.v1.services.country_service import refresh_countries
from api.core.database import database
import os

router = APIRouter()
IMAGE_PATH = "cache/summary.png"



@router.post("/refresh")
async def refresh_data():
    try:
        result = await refresh_countries()
        return result
    except Exception as e:
        raise HTTPException(status_code=503, detail={"error": str(e)})


@router.get("/")
async def get_countries(
    region: str | None = Query(None),
    currency: str | None = Query(None),
    sort: str | None = Query(None),
):
    """Get all countries with optional filters & sorting."""
    query = "SELECT * FROM countries WHERE 1=1"
    params = {}

    if region:
        query += " AND LOWER(region)=LOWER(:region)"
        params["region"] = region
    if currency:
        query += " AND LOWER(currency_code)=LOWER(:currency)"
        params["currency"] = currency

    if sort:
        if sort.lower() == "gdp_desc":
            query += " ORDER BY estimated_gdp DESC"
        elif sort.lower() == "gdp_asc":
            query += " ORDER BY estimated_gdp ASC"

    countries = await database.fetch_all(query, values=params)
    return countries

@router.get("/image")
async def get_summary_image():
    """Serve the cached summary image."""
    if os.path.exists(IMAGE_PATH):
        return FileResponse(IMAGE_PATH, media_type="image/png")
    raise HTTPException(status_code=404, detail="Summary image not found")


@router.get("/{name}")
async def get_country(name: str):
    query = "SELECT * FROM countries WHERE LOWER(name)=LOWER(:name)"
    country = await database.fetch_one(query, values={"name": name})
    if not country:
        raise HTTPException(status_code=404, detail={"error": "Country not found"})
    return dict(country)

@router.delete("/{name}")
async def delete_country(name: str):
    query = "DELETE FROM countries WHERE LOWER(name)=LOWER(:name)"
    result = await database.execute(query, values={"name": name})
    if not result:
        raise HTTPException(status_code=404, detail={"error": "Country not found"})
    return {"message": f"{name} deleted successfully"}

