import polars as pl
from datetime import date, datetime
from dataclasses import dataclass


@dataclass
class Expense:
    id: str
    date: date
    amount: float
    category: str
    subcategory: str
    description: str
    payment_method: str
    is_recurring: bool
    created_at: datetime

    @staticmethod
    def make_df(data: list[Expense]) -> pl.DataFrame:
        return pl.DataFrame(data, schema=Expense.schema())

    @staticmethod
    def schema():
        return {
            "id": pl.String,
            "date": pl.Date,
            "amount": pl.Float64,
            "category": pl.Categorical,
            "subcategory": pl.String,
            "description": pl.String,
            "payment_method": pl.Categorical,
            "is_recurring": pl.Boolean,
            "created_at": pl.Datetime,
        }


@dataclass
class Investment:
    id: str
    date: date
    ticker: str
    asset_class: str
    action: str
    quantity: float
    price: float
    fees: float
    currency: str
    fx_rate: float
    brokerage: str
    notes: str
    created_at: datetime

    @staticmethod
    def make_df(data: list[Investment]) -> pl.DataFrame:
        return pl.DataFrame(data, schema=Investment.schema())

    @staticmethod
    def schema():
        return {
            "id": pl.String,
            "date": pl.Date,
            "ticker": pl.String,
            "asset_class": pl.Categorical,
            "action": pl.Categorical,
            "quantity": pl.Float64,
            "price": pl.Float64,
            "fees": pl.Float64,
            "currency": pl.Categorical,
            "fx_rate": pl.Float64,
            "brokerage": pl.Categorical,
            "notes": pl.String,
            "created_at": pl.Datetime,
        }
