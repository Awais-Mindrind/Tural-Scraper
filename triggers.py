import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from apscheduler.schedulers.background import BackgroundScheduler
# from airtable import get_hashtag_from_airtable
from tikTok_Scraper import scrape_tiktok_profiles

# Configure logging
logging.basicConfig(
    filename="scraper_logs.log",  # Log file name
    level=logging.INFO,  # Log level
    format="%(asctime)s - %(levelname)s - %(message)s",  # Log format
)

app = FastAPI()

# Request model for API trigger
class ScraperRequest(BaseModel):
    hashtag: str
    num_profiles: int = 500

# API Trigger
@app.post("/start-scraper")
async def start_scraper(request: ScraperRequest):
    hashtag = request.hashtag
    num_profiles = request.num_profiles

    if not hashtag:
        raise HTTPException(status_code=400, detail="Hashtag is required")

    try:
        scrape_tiktok_profiles(base_hashtag=hashtag, num_profiles=num_profiles)
        return {"message": f"Scraper started for hashtag: {hashtag} with {num_profiles} profiles"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Cron Job Trigger
def run_cron_job():
    try:
        # hashtag = get_hashtag_from_airtable()
        hashtag = "cricket"
        if hashtag:
            logging.info(f"Running scraper for hashtag: {hashtag}")
            scrape_tiktok_profiles(base_hashtag=hashtag)
    except Exception as e:
        logging.error(f"Error in cron job: {e}")

# Scheduler setup
scheduler = BackgroundScheduler()
scheduler.add_job(run_cron_job, "interval", hours=24)
scheduler.start()

# Run FastAPI app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)