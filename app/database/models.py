from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()


class Stock(Base):
    __tablename__ = "stocks"

    id = Column(Integer, primary_key=True, index=True)

    symbol = Column(
        String(20),
        unique=True,
        nullable=False,
        index=True,
    )

    company_name = Column(
        String(255),
        nullable=False,
    )

    is_active = Column(
        Integer,
        default=1,
        nullable=False,
    )

    prices = relationship(
        "StockPrice",
        back_populates="stock",
        cascade="all, delete-orphan",
    )


class StockPrice(Base):
    __tablename__ = "stock_prices"

    id = Column(Integer, primary_key=True, index=True)

    stock_id = Column(
        Integer,
        ForeignKey("stocks.id"),
        nullable=False,
        index=True,
    )

    price = Column(
        Float,
        nullable=False,
    )

    change = Column(
        Float,
        nullable=True,
    )

    change_percent = Column(
        Float,
        nullable=True,
    )

    volume = Column(
        Integer,
        nullable=True,
    )

    session = Column(
        String(20),
        nullable=False,
    )

    captured_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        index=True,
    )

    source = Column(
        String(255),
        nullable=True,
    )

    raw_data = Column(
        Text,
        nullable=True,
    )

    stock = relationship(
        "Stock",
        back_populates="prices",
    )

    __table_args__ = (
        UniqueConstraint(
            "stock_id",
            "captured_at",
            "session",
            name="uq_stock_price_capture",
        ),
    )