import marimo

__generated_with = "0.20.4"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo
    import polars as pl
    from datetime import date

    from finance import uid, now
    from finance.crud import Expense, Investment

    DATA_DIR = "data"
    return DATA_DIR, Expense, Investment, date, mo, now, pl, uid


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Insert `expense`
    Edit the expense array and run the cell below to insert the data.
    """)
    return


@app.cell
def _(Expense, date, now, uid):
    # Replace this array with your expenses
    expenses = [
        Expense(
            id=uid(),
            date=date(2026, 3, 5),
            amount=31.95,
            category="food",
            subcategory="grocery",
            description="Heromart (eggs, milk)",
            payment_method="tng",
            is_recurring=False,
            created_at=now(),
        )
    ]
    return (expenses,)


@app.cell
def _(DATA_DIR, Expense, expenses, pl):
    # Add the expense to the existing data
    edf = (
        pl.read_parquet(f"{DATA_DIR}/expense.parquet")
        .vstack(Expense.make_df(expenses))
        .sort("date")
        .unique(
            [
                "date",
                "amount",
                "category",
                "subcategory",
                "description",
                "payment_method",
                "is_recurring",
            ],
            keep="first",
        )
    )
    edf
    return (edf,)


@app.cell
def _(DATA_DIR, edf):
    # Write the updated data to the filesystem
    edf.write_parquet(f"{DATA_DIR}/expense.parquet")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Insert `investment`
    Edit the investment array and run the cell below to insert the data.
    """)
    return


@app.cell
def _(Investment, date, now, uid):
    # Replace this array with your expenses
    investments = [
        Investment(
            id=uid(),
            date=date(2026, 1, 7),
            ticker="SPY",
            asset_class="index_fund",
            action="buy",
            quantity=1.0,
            price=580.20,
            fees=1.50,
            currency="USD",
            fx_rate=4.47,
            brokerage="ibkr",
            notes="Monthly DCA",
            created_at=now(),
        )
    ]
    return (investments,)


@app.cell
def _(DATA_DIR, Investment, investments, pl):
    # Add the expense to the existing data
    idf = (
        pl.read_parquet(f"{DATA_DIR}/investment.parquet")
        .vstack(Investment.make_df(investments))
        .sort("date")
        .unique(
            [
                "date",
                "ticker",
                "asset_class",
                "action",
                "quantity",
                "price",
                "fees",
                "currency",
                "fx_rate",
                "brokerage",
                "notes",
            ],
            keep="first",
        )
    )
    idf
    return (idf,)


@app.cell
def _(DATA_DIR, idf):
    # Write the updated data to the filesystem
    idf.write_parquet(f"{DATA_DIR}/investment.parquet")
    return


if __name__ == "__main__":
    app.run()
