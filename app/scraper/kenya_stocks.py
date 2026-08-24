import re
from typing import Optional

import requests
from bs4 import BeautifulSoup

from app.config import TRACKED_STOCKS


STOCKS_URL = "https://stocks.or.ke/stocks/"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/120.0 Safari/537.36"
    )
}


class KenyaStocksScraper:
    """
    Scrapes selected Nairobi Securities Exchange stock prices.
    """

    def __init__(
        self,
        tracked_stocks: Optional[list[str]] = None,
    ):
        self.tracked_stocks = {
            stock.upper()
            for stock in (tracked_stocks or TRACKED_STOCKS)
        }

    @staticmethod
    def clean_number(value: str) -> Optional[float]:
        """
        Convert values such as:
        '36.50'
        '+1.25%'
        '1.5K'
        '2.3M'

        into numeric values.
        """

        if not value:
            return None

        value = value.strip()

        if value in {"-", "—", "N/A"}:
            return None

        value = value.replace(",", "")
        value = value.replace("+", "")
        value = value.replace("%", "")

        multiplier = 1

        if value.upper().endswith("K"):
            multiplier = 1_000
            value = value[:-1]

        elif value.upper().endswith("M"):
            multiplier = 1_000_000
            value = value[:-1]

        try:
            return float(value) * multiplier
        except ValueError:
            return None

    def fetch_page(self) -> BeautifulSoup:
        """
        Download and parse the stock price page.
        """

        response = requests.get(
            STOCKS_URL,
            headers=HEADERS,
            timeout=30,
        )

        response.raise_for_status()

        return BeautifulSoup(
            response.text,
            "lxml",
        )

    def scrape(self) -> list[dict]:
        """
        Scrape all configured stocks.

        Returns a list of dictionaries.
        """

        soup = self.fetch_page()

        results = []

        for row in soup.select("tr"):

            cells = row.find_all("td")

            if len(cells) < 11:
                continue

            values = [
                cell.get_text(
                    " ",
                    strip=True,
                )
                for cell in cells
            ]

            symbol = values[0].upper().strip()

            if symbol not in self.tracked_stocks:
                continue

            company_name = values[1]

            prev_close = self.clean_number(values[6])
            close = self.clean_number(values[7])
            change = self.clean_number(values[8])
            change_percent = self.clean_number(values[9])
            volume = self.clean_number(values[10])

            if close is None:
                continue

            results.append(
                {
                    "symbol": symbol,
                    "company_name": company_name,
                    "price": close,
                    "previous_price": prev_close,
                    "change": change,
                    "change_percent": change_percent,
                    "volume": (
                        int(volume)
                        if volume is not None
                        else None
                    ),
                    "source": STOCKS_URL,
                }
            )

        return results