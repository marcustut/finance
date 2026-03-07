"""
main.py — Finance Tracker API
Run: uvicorn web.server:app --host 0.0.0.0 --port 8000 --reload
"""

import polars as pl
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
from pathlib import Path
from ulid import ULID

from finance.crud import Expense, Investment

app = FastAPI(title="Finance Tracker")

DATA_DIR = Path(__file__).parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)
EXPENSES_PATH = DATA_DIR / "expense.parquet"
INVESTMENTS_PATH = DATA_DIR / "investment.parquet"


def _empty_expenses() -> pl.DataFrame:
    return pl.DataFrame(schema=Expense.schema())


def _empty_investments() -> pl.DataFrame:
    return pl.DataFrame(schema=Investment.schema())


def read_expenses() -> pl.DataFrame:
    if not EXPENSES_PATH.exists():
        return _empty_expenses()
    return pl.read_parquet(EXPENSES_PATH).cast(
        {"category": pl.Categorical, "payment_method": pl.Categorical}
    )


def read_investments() -> pl.DataFrame:
    if not INVESTMENTS_PATH.exists():
        return _empty_investments()
    return pl.read_parquet(INVESTMENTS_PATH).cast(
        {
            "asset_class": pl.Categorical,
            "action": pl.Categorical,
            "currency": pl.Categorical,
            "brokerage": pl.Categorical,
        }
    )


def write_expenses(df: pl.DataFrame):
    df.write_parquet(EXPENSES_PATH)


def write_investments(df: pl.DataFrame):
    df.write_parquet(INVESTMENTS_PATH)


def new_id() -> str:
    return str(ULID())


# ── Pydantic models ────────────────────────────────────────────────────────────


class ExpenseIn(BaseModel):
    date: date
    amount: float
    category: str
    subcategory: Optional[str] = None
    description: Optional[str] = None
    payment_method: str
    is_recurring: bool = False


class InvestmentIn(BaseModel):
    date: date
    ticker: str
    asset_class: str
    action: str
    quantity: float
    price: float
    fees: float = 0.0
    currency: str = "MYR"
    fx_rate: Optional[float] = None
    brokerage: str
    notes: Optional[str] = None


# ── Expense CRUD ───────────────────────────────────────────────────────────────


@app.get("/api/expenses")
def list_expenses():
    df = read_expenses()
    return (
        df.sort("date", descending=True)
        .with_columns(
            pl.col("date").cast(pl.String),
            pl.col("created_at").cast(pl.String),
        )
        .to_dicts()
    )


@app.post("/api/expenses", status_code=201)
def create_expense(body: ExpenseIn):
    df = read_expenses()
    row = pl.DataFrame(
        [
            {
                "id": new_id(),
                "date": body.date,
                "amount": body.amount,
                "category": body.category,
                "subcategory": body.subcategory,
                "description": body.description,
                "payment_method": body.payment_method,
                "is_recurring": body.is_recurring,
                "created_at": datetime.now(),
            }
        ],
        schema=Expense.schema(),
    )
    write_expenses(pl.concat([df, row]))
    return {"id": row["id"][0]}


@app.put("/api/expenses/{eid}")
def update_expense(eid: str, body: ExpenseIn):
    df = read_expenses()
    if not df.filter(pl.col("id") == eid).shape[0]:
        raise HTTPException(404, "Expense not found")
    updated = df.with_columns(
        [
            pl.when(pl.col("id") == eid)
            .then(pl.lit(str(body.date)))
            .otherwise(pl.col("date").cast(pl.String))
            .alias("date_str"),
        ]
    )
    # Rebuild row cleanly
    rest = df.filter(pl.col("id") != eid)
    row = pl.DataFrame(
        [
            {
                "id": eid,
                "date": body.date,
                "amount": body.amount,
                "category": body.category,
                "subcategory": body.subcategory,
                "description": body.description,
                "payment_method": body.payment_method,
                "is_recurring": body.is_recurring,
                "created_at": datetime.now(),
            }
        ],
        schema=Expense.schema(),
    )
    write_expenses(pl.concat([rest, row]).sort("date"))
    return {"ok": True}


@app.delete("/api/expenses/{eid}")
def delete_expense(eid: str):
    df = read_expenses()
    write_expenses(df.filter(pl.col("id") != eid))
    return {"ok": True}


# ── Investment CRUD ────────────────────────────────────────────────────────────


@app.get("/api/investments")
def list_investments():
    df = read_investments()
    return (
        df.sort("date", descending=True)
        .with_columns(
            pl.col("date").cast(pl.String),
            pl.col("created_at").cast(pl.String),
        )
        .to_dicts()
    )


@app.post("/api/investments", status_code=201)
def create_investment(body: InvestmentIn):
    df = read_investments()
    row = pl.DataFrame(
        [
            {
                "id": new_id(),
                "date": body.date,
                "ticker": body.ticker.upper(),
                "asset_class": body.asset_class,
                "action": body.action,
                "quantity": body.quantity,
                "price": body.price,
                "fees": body.fees,
                "currency": body.currency,
                "fx_rate": body.fx_rate,
                "brokerage": body.brokerage,
                "notes": body.notes,
                "created_at": datetime.now(),
            }
        ],
        schema=Investment.schema(),
    )
    write_investments(pl.concat([df, row]))
    return {"id": row["id"][0]}


@app.put("/api/investments/{iid}")
def update_investment(iid: str, body: InvestmentIn):
    df = read_investments()
    if not df.filter(pl.col("id") == iid).shape[0]:
        raise HTTPException(404, "Investment not found")
    rest = df.filter(pl.col("id") != iid)
    row = pl.DataFrame(
        [
            {
                "id": iid,
                "date": body.date,
                "ticker": body.ticker.upper(),
                "asset_class": body.asset_class,
                "action": body.action,
                "quantity": body.quantity,
                "price": body.price,
                "fees": body.fees,
                "currency": body.currency,
                "fx_rate": body.fx_rate,
                "brokerage": body.brokerage,
                "notes": body.notes,
                "created_at": datetime.now(),
            }
        ],
        schema=Investment.schema(),
    )
    write_investments(pl.concat([rest, row]).sort("date"))
    return {"ok": True}


@app.delete("/api/investments/{iid}")
def delete_investment(iid: str):
    df = read_investments()
    write_investments(df.filter(pl.col("id") != iid))
    return {"ok": True}


# ── Analytics ──────────────────────────────────────────────────────────────────


@app.get("/api/analytics/expenses")
def expense_analytics():
    df = read_expenses()
    if df.is_empty():
        return {"monthly": [], "by_category": [], "monthly_by_category": []}

    df = df.with_columns(pl.col("date").dt.strftime("%Y-%m").alias("month"))

    monthly = (
        df.group_by("month")
        .agg(pl.col("amount").sum().round(2).alias("total"))
        .sort("month")
        .to_dicts()
    )
    by_cat = (
        df.group_by("category")
        .agg(pl.col("amount").sum().round(2).alias("total"))
        .sort("total", descending=True)
        .with_columns(pl.col("category").cast(pl.String))
        .to_dicts()
    )
    monthly_by_cat = (
        df.group_by("month", "category")
        .agg(pl.col("amount").sum().round(2).alias("total"))
        .sort("month", "total", descending=[False, True])
        .with_columns(pl.col("category").cast(pl.String))
        .to_dicts()
    )
    return {
        "monthly": monthly,
        "by_category": by_cat,
        "monthly_by_category": monthly_by_cat,
    }


@app.get("/api/analytics/portfolio")
def portfolio_analytics():
    df = read_investments()
    if df.is_empty():
        return {"holdings": [], "allocation": [], "trades": []}

    # Convert each trade's cost to MYR before aggregating
    df = df.with_columns(
        pl.when(
            (pl.col("currency") == "USD") & pl.col("fx_rate").is_not_null()
        )
        .then((pl.col("quantity") * pl.col("price") + pl.col("fees")) * pl.col("fx_rate"))
        .otherwise(pl.col("quantity") * pl.col("price") + pl.col("fees"))
        .alias("cost_myr")
    )

    # Net holdings: buys - sells per ticker
    buys = (
        df.filter(pl.col("action") == "buy")
        .group_by("ticker", "asset_class")
        .agg(
            pl.col("quantity").sum().alias("bought"),
            pl.col("cost_myr").sum().alias("cost"),
            pl.col("currency").first().alias("currency"),
        )
    )
    sells = (
        df.filter(pl.col("action") == "sell")
        .group_by("ticker")
        .agg(
            pl.col("quantity").sum().alias("sold"),
        )
    )
    holdings = (
        buys.join(sells, on="ticker", how="left")
        .with_columns(
            pl.col("sold").fill_null(0),
        )
        .with_columns(
            (pl.col("bought") - pl.col("sold")).alias("net_qty"),
            (pl.col("cost") / pl.col("bought")).alias("avg_price"),
        )
        .filter(pl.col("net_qty") > 0)
        .sort("asset_class", "ticker")
    )

    alloc = (
        holdings.with_columns(pl.col("asset_class").cast(pl.String))
        .group_by("asset_class")
        .agg(pl.col("cost").sum().round(2).alias("total_cost"))
        .sort("total_cost", descending=True)
        .to_dicts()
    )

    return {
        "holdings": holdings.with_columns(
            pl.col("asset_class").cast(pl.String),
            pl.col("currency").cast(pl.String),
            pl.col("avg_price").round(4),
            pl.col("cost").round(2),
        ).to_dicts(),
        "allocation": alloc,
    }


# ── Serve frontend ─────────────────────────────────────────────────────────────
app.mount(
    "/static", StaticFiles(directory=Path(__file__).parent / "static"), name="static"
)


@app.get("/")
def root():
    return FileResponse(Path(__file__).parent / "static" / "index.html")
