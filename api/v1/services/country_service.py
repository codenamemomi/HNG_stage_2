import random
from datetime import datetime
from typing import List, Dict
import httpx
from loguru import logger
from sqlalchemy import text

from api.core.database import database
from api.core.settings import settings
from api.utils.image_generator import generate_summary_image


COUNTRIES_API = settings.COUNTRIES_API
EXCHANGE_API = settings.EXCHANGE_API


async def fetch_countries_data() -> List[Dict]:
    """Fetch country data from the REST Countries API."""
    try:
        async with httpx.AsyncClient(timeout=20) as client:
            response = await client.get(COUNTRIES_API)
            response.raise_for_status()
            return response.json()
    except Exception as e:
        logger.error(f"❌ Failed to fetch countries: {e}")
        raise Exception("External data source unavailable: RESTCountries API")


async def fetch_exchange_rates() -> Dict:
    """Fetch exchange rate data (USD base)."""
    try:
        async with httpx.AsyncClient(timeout=20) as client:
            response = await client.get(EXCHANGE_API)
            response.raise_for_status()
            data = response.json()
            return data.get("rates", {})
    except Exception as e:
        logger.error(f"❌ Failed to fetch exchange rates: {e}")
        raise Exception("External data source unavailable: Exchange Rate API")


async def refresh_countries():
    """Fetch, compute, and cache all country data."""
    logger.info("🔄 Starting countries refresh...")

    countries_data = await fetch_countries_data()
    exchange_rates = await fetch_exchange_rates()

    total_countries = 0
    last_refreshed_at = datetime.utcnow()

    async with database.transaction():
        for country in countries_data:
            try:
                name = country.get("name", {}).get("common")
                capital_list = country.get("capital", [])
                capital = capital_list[0] if capital_list else None
                region = country.get("region")
                population = country.get("population") or 0
                flag = country.get("flags", {}).get("png")

                currencies = country.get("currencies", {})
                currency_code = next(iter(currencies.keys()), None)

                exchange_rate = exchange_rates.get(currency_code) if currency_code else None

                if exchange_rate and exchange_rate > 0:
                    multiplier = random.randint(1000, 2000)
                    estimated_gdp = (population * multiplier) / exchange_rate
                else:
                    estimated_gdp = 0.0

                # ✅ FIXED — removed text() wrappers
                query_existing = "SELECT id FROM countries WHERE LOWER(name)=LOWER(:name)"
                existing_id = await database.fetch_val(query_existing, values={"name": name})

                values = {
                    "name": name,
                    "capital": capital,
                    "region": region,
                    "population": population,
                    "currency_code": currency_code,
                    "exchange_rate": exchange_rate,
                    "estimated_gdp": estimated_gdp,
                    "flag_url": flag,
                    "last_refreshed_at": last_refreshed_at,
                }

                if existing_id:
                    query_update = """
                        UPDATE countries
                        SET capital=:capital, region=:region, population=:population,
                            currency_code=:currency_code, exchange_rate=:exchange_rate,
                            estimated_gdp=:estimated_gdp, flag_url=:flag_url,
                            last_refreshed_at=:last_refreshed_at
                        WHERE id=:id
                    """
                    await database.execute(query_update, values={**values, "id": existing_id})
                else:
                    query_insert = """
                        INSERT INTO countries (name, capital, region, population,
                            currency_code, exchange_rate, estimated_gdp, flag_url, last_refreshed_at)
                        VALUES (:name, :capital, :region, :population, :currency_code,
                            :exchange_rate, :estimated_gdp, :flag_url, :last_refreshed_at)
                    """
                    await database.execute(query_insert, values)

                total_countries += 1

            except Exception as e:
                logger.error(f"❌ Error processing country {country.get('name')}: {e}")
                continue

        await generate_summary_image(database, total_countries, last_refreshed_at)

    return {
        "message": "Countries data refreshed successfully",
        "total_countries": total_countries,
        "last_refreshed_at": last_refreshed_at.isoformat()
    }
