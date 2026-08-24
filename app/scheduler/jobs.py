from apscheduler.schedulers.blocking import BlockingScheduler
from zoneinfo import ZoneInfo

from app.config import (
    EVENING_SCRAPE_TIME,
    MORNING_SCRAPE_TIME,
    TIMEZONE,
)
from app.database.connection import SessionLocal
from app.services.stock_service import StockService


def run_scrape(session_name: str):
    """
    Run the stock scraper and save results.
    """

    print(f"Starting {session_name} stock scrape...")

    db = SessionLocal()

    try:
        records = StockService.scrape_and_save(
            db=db,
            session_name=session_name,
        )

        print(
            f"{session_name.capitalize()} scrape completed. "
            f"Saved {len(records)} stock prices."
        )

    except Exception as error:
        print(
            f"Error during {session_name} scrape: {error}"
        )

    finally:
        db.close()


def morning_scrape():
    run_scrape("morning")


def evening_scrape():
    run_scrape("evening")


def start_scheduler():
    """
    Start the morning and evening stock scraper.
    """

    morning_hour, morning_minute = map(
        int,
        MORNING_SCRAPE_TIME.split(":"),
    )

    evening_hour, evening_minute = map(
        int,
        EVENING_SCRAPE_TIME.split(":"),
    )

    scheduler = BlockingScheduler(
        timezone=ZoneInfo(TIMEZONE),
    )

    scheduler.add_job(
        morning_scrape,
        trigger="cron",
        hour=morning_hour,
        minute=morning_minute,
        id="morning_stock_scrape",
        replace_existing=True,
    )

    scheduler.add_job(
        evening_scrape,
        trigger="cron",
        hour=evening_hour,
        minute=evening_minute,
        id="evening_stock_scrape",
        replace_existing=True,
    )

    print("KE-STOCKS-SPIDER scheduler started.")
    print(
        f"Morning scrape: {MORNING_SCRAPE_TIME} "
        f"({TIMEZONE})"
    )
    print(
        f"Evening scrape: {EVENING_SCRAPE_TIME} "
        f"({TIMEZONE})"
    )

    try:
        scheduler.start()

    except (KeyboardInterrupt, SystemExit):
        print("Scheduler stopped.")