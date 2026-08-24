from datetime import datetime
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from mcp.server import MCPServer

from app.database.connection import SessionLocal
from app.services.stock_service import StockService


mcp = MCPServer("KE-STOCKS-SPIDER")


@mcp.tool()
def get_latest_price(symbol: str) -> dict:
    """
    Get the latest recorded price for a Kenyan stock.

    Args:
        symbol: NSE stock symbol, for example KCB, EQTY, SCOM or EABL.
    """

    db = SessionLocal()

    try:
        record = StockService.get_latest_price(
            db=db,
            symbol=symbol,
        )

        if not record:
            return {
                "success": False,
                "message": (
                    f"No price data found for "
                    f"{symbol.upper()}"
                ),
            }

        return {
            "success": True,
            "symbol": record.stock.symbol,
            "company_name": record.stock.company_name,
            "price": record.price,
            "change": record.change,
            "change_percent": record.change_percent,
            "volume": record.volume,
            "session": record.session,
            "captured_at": record.captured_at.isoformat(),
            "source": record.source,
        }

    finally:
        db.close()


@mcp.tool()
def get_tracked_stocks() -> list[dict]:
    """
    Get all active stocks tracked by KE-STOCKS-SPIDER.
    """

    db = SessionLocal()

    try:
        stocks = StockService.get_all_stocks(db)

        return [
            {
                "symbol": stock.symbol,
                "company_name": stock.company_name,
                "active": bool(stock.is_active),
            }
            for stock in stocks
        ]

    finally:
        db.close()


@mcp.tool()
def get_price_history(
    symbol: str,
    limit: int = 100,
) -> list[dict]:
    """
    Get historical prices for a Kenyan stock.

    Args:
        symbol: NSE stock symbol.
        limit: Maximum number of records to return.
    """

    db = SessionLocal()

    try:
        records = StockService.get_price_history(
            db=db,
            symbol=symbol,
            limit=limit,
        )

        return [
            {
                "symbol": record.stock.symbol,
                "company_name": record.stock.company_name,
                "price": record.price,
                "change": record.change,
                "change_percent": record.change_percent,
                "volume": record.volume,
                "session": record.session,
                "captured_at": record.captured_at.isoformat(),
                "source": record.source,
            }
            for record in records
        ]

    finally:
        db.close()


@mcp.tool()
def scrape_now(
    session_name: str = "manual",
) -> dict:
    """
    Immediately scrape all configured Kenyan stocks
    and save their prices to the database.

    Args:
        session_name: Name for this collection,
                      for example morning, evening or manual.
    """

    db = SessionLocal()

    try:
        records = StockService.scrape_and_save(
            db=db,
            session_name=session_name,
        )

        return {
            "success": True,
            "session": session_name,
            "stocks_saved": len(records),
            "timestamp": datetime.utcnow().isoformat(),
        }

    except Exception as error:
        return {
            "success": False,
            "error": str(error),
        }

    finally:
        db.close()


if __name__ == "__main__":
    mcp.run("stdio")