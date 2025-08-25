from typing import Optional
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

from airtable import table
from schemas import AIQueryRequest, ScrapeRequest
from tikTok_Scraper import scrape_tiktok_profiles
from llm_query import parse_query_to_filters

app = FastAPI(title="TikTok Scraper API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],     # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------
# API ROUTES
# ------------------------------

@app.post("/scrape")
def trigger_scraping(request: ScrapeRequest):
    scraped_profiles = scrape_tiktok_profiles(request.hashtag, request.num_profiles)
    return {
        "message": f"Scraping completed for #{request.hashtag}",
        "profiles_scraped": len(scraped_profiles),
    }


@app.get("/profiles")
def get_profiles(
    hashtag: Optional[str] = None,
    country: Optional[str] = None,
    min_followers: Optional[int] = None,
    min_likes: Optional[int] = None,
    limit: int = Query(50, ge=1, le=1000)
):
    formula_parts = []

    if hashtag:
        formula_parts.append(f"{{Hashtag}} = '{hashtag}'")
    if country:
        formula_parts.append(f"{{Country}} = '{country}'")
    if min_followers:
        formula_parts.append(f"{{Followers}} >= {min_followers}")
    if min_likes:
        formula_parts.append(f"{{Likes}} >= {min_likes}")

    formula = "AND(" + ", ".join(formula_parts) + ")" if formula_parts else None

    records = table.all(max_records=limit, formula=formula)

    return {
        "count": len(records),
        "data": [rec["fields"] for rec in records]
    }


@app.post("/profiles/ai")
def search_profiles_ai(request: AIQueryRequest):
    # Step 1: Convert query → structured filters
    filters = parse_query_to_filters(request.query)

    # Step 2: Build Airtable formula
    formula_parts = []
    if filters.hashtag:
        formula_parts.append(f"SEARCH('{filters.hashtag.lower()}', LOWER({{Hashtag}}))")
    if filters.country:
        formula_parts.append(f"{{Country}} = '{filters.country.capitalize()}'")
    if filters.min_followers:
        formula_parts.append(f"{{Followers}} >= {filters.min_followers}")
    if filters.min_likes:
        formula_parts.append(f"{{Likes}} >= {filters.min_likes}")

    formula = "AND(" + ", ".join(formula_parts) + ")" if formula_parts else None

    # Step 3: Fetch from Airtable
    records = table.all(max_records=filters.limit, formula=formula)

    return {
        "filters": filters.dict(),
        "count": len(records),
        "data": [rec["fields"] for rec in records]
    }


if __name__=="__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)