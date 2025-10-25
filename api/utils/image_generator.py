# api/utils/image_generator.py
import os
from datetime import datetime
import matplotlib.pyplot as plt

CACHE_DIR = "cache"
os.makedirs(CACHE_DIR, exist_ok=True)

async def generate_summary_image(database, total_countries: int, last_refreshed_at: datetime):
    """Generate summary image with top 5 GDP countries."""
    query_top = """
        SELECT name, estimated_gdp FROM countries
        ORDER BY estimated_gdp DESC
        LIMIT 5
    """
    rows = await database.fetch_all(query_top)
    names = [r["name"] for r in rows]
    gdps = [r["estimated_gdp"] for r in rows]

    plt.figure(figsize=(8, 6))
    plt.barh(names, gdps)
    plt.xlabel("Estimated GDP")
    plt.ylabel("Country")
    plt.title(f"Top 5 Countries by Estimated GDP\nRefreshed at {last_refreshed_at:%Y-%m-%d %H:%M:%S UTC}")

    plt.tight_layout()
    image_path = os.path.join(CACHE_DIR, "summary.png")
    plt.savefig(image_path)
    plt.close()
