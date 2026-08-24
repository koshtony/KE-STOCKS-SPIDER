# KE-STOCKS-SPIDER

KE-STOCKS-SPIDER is a lightweight Kenyan stock market data collection and MCP server application.

It automatically collects selected Nairobi Securities Exchange (NSE) stock prices in the morning and evening, stores the results in a database, and exposes the collected data to AI assistants such as Claude through the Model Context Protocol (MCP).

---

## Features

- Scrapes selected Kenyan/NSE stock prices
- Supports configurable tracked stocks
- Morning automatic price collection
- Evening automatic price collection
- SQLite database storage
- Historical stock price records
- Manual scraping
- MCP server integration
- Claude Desktop integration
- MCP Inspector testing
- Query latest stock prices through AI
- Query historical prices through AI
- Retrieve tracked stocks through AI

---

# Project Architecture

```text
KE-STOCKS-SPIDER/
│
├── app/
│   ├── database/
│   │   ├── connection.py
│   │   └── models.py
│   │
│   ├── scraper/
│   │   └── kenya_stocks.py
│   │
│   ├── services/
│   │   └── stock_service.py
│   │
│   ├── scheduler/
│   │   └── jobs.py
│   │
│   └── config.py
│
├── mcp_server/
│   └── server.py
│
├── main.py
├── requirements.txt
├── README.md
└── spider-env/