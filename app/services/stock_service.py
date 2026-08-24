import json
from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session

from app.database.models import Stock, StockPrice


class StockService:

    @staticmethod
    def get_or_create_stock(
        db: Session,
        symbol: str,
        company_name: Optional[str] = None,
    ) -> Stock:

        symbol = symbol.upper().strip()

        stock = (
            db.query(Stock)
            .filter(Stock.symbol == symbol)
            .first()
        )

        if stock:
            return stock

        stock = Stock(
            symbol=symbol,
            company_name=company_name or symbol,
            is_active=1,
        )

        db.add(stock)
        db.commit()
        db.refresh(stock)

        return stock

    @staticmethod
    def save_price(
        db: Session,
        symbol: str,
        price: float,
        session: str,
        company_name: Optional[str] = None,
        change: Optional[float] = None,
        change_percent: Optional[float] = None,
        volume: Optional[int] = None,
        source: Optional[str] = None,
        raw_data: Optional[str] = None,
        captured_at: Optional[datetime] = None,
    ) -> StockPrice:

        stock = StockService.get_or_create_stock(
            db=db,
            symbol=symbol,
            company_name=company_name,
        )

        price_record = StockPrice(
            stock_id=stock.id,
            price=price,
            change=change,
            change_percent=change_percent,
            volume=volume,
            session=session,
            captured_at=captured_at or datetime.utcnow(),
            source=source,
            raw_data=raw_data,
        )

        db.add(price_record)
        db.commit()
        db.refresh(price_record)

        return price_record

    @staticmethod
    def get_latest_price(
        db: Session,
        symbol: str,
    ) -> Optional[StockPrice]:

        symbol = symbol.upper().strip()

        return (
            db.query(StockPrice)
            .join(Stock)
            .filter(Stock.symbol == symbol)
            .order_by(StockPrice.captured_at.desc())
            .first()
        )

    @staticmethod
    def get_all_stocks(db: Session):

        return (
            db.query(Stock)
            .filter(Stock.is_active == 1)
            .order_by(Stock.symbol)
            .all()
        )

    @staticmethod
    def get_price_history(
        db: Session,
        symbol: str,
        limit: int = 100,
    ):

        symbol = symbol.upper().strip()

        return (
            db.query(StockPrice)
            .join(Stock)
            .filter(Stock.symbol == symbol)
            .order_by(StockPrice.captured_at.desc())
            .limit(limit)
            .all()
        )

    @staticmethod
    def scrape_and_save(
        db: Session,
        session_name: str,
    ) -> list[StockPrice]:
        """
        Scrape configured Kenyan stocks and save their prices.
        """

        from app.scraper.kenya_stocks import KenyaStocksScraper

        scraper = KenyaStocksScraper()

        stocks = scraper.scrape()

        saved_records = []

        for stock_data in stocks:

            record = StockService.save_price(
                db=db,
                symbol=stock_data["symbol"],
                company_name=stock_data.get("company_name"),
                price=stock_data["price"],
                change=stock_data.get("change"),
                change_percent=stock_data.get(
                    "change_percent"
                ),
                volume=stock_data.get("volume"),
                session=session_name,
                source=stock_data.get("source"),
                raw_data=json.dumps(stock_data),
            )

            saved_records.append(record)

        return saved_records