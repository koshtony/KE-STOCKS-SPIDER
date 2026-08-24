import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# Project root
BASE_DIR = Path(__file__).resolve().parent.parent

# Database
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"sqlite:///{BASE_DIR / 'data' / 'ke_stocks.db'}",
)

# Timezone
TIMEZONE = os.getenv("TIMEZONE", "Africa/Nairobi")

# Scheduled scraping times
MORNING_SCRAPE_TIME = os.getenv("MORNING_SCRAPE_TIME", "08:00")
EVENING_SCRAPE_TIME = os.getenv("EVENING_SCRAPE_TIME", "17:30")

# Stocks to track
TRACKED_STOCKS = [
    "SCBK",
    "EQTY",
    "KCB",
    "SCOM",
    "EABL",
    "COOP",
    "ABSA",
]