import marimo

__generated_with = "0.20.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import polars as pl
    from datetime import date

    from finance import uid, now
    from finance.crud import Expense, Investment

    DATA_DIR = "data"
    return DATA_DIR, Expense, Investment, date, now, pl, uid


@app.cell
def _(DATA_DIR, Expense, date, now, pl, uid):
    # ─────────────────────────────────────────────
    # expenses.parquet
    # ─────────────────────────────────────────────

    expenses_rows = [
        # January
        # (uid(), date(2026, 1, 3),  12.50,  "food",       "groceries",   "Pasar malam groceries",    "ewallet",  False),
        # (uid(), date(2026, 1, 5),  8.00,   "transport",  "grab",        "Grab to office",            "ewallet",  False),
        # (uid(), date(2026, 1, 7),  1500.00,"utilities",  "rent",        "January rent",              "debit",    True),
        # (uid(), date(2026, 1, 10), 45.00,  "food",       "dining out",  "Dinner with friends",       "credit",   False),
        # (uid(), date(2026, 1, 12), 15.90,  "health",     "pharmacy",    "Vitamin C supplements",     "cash",     False),
        # (uid(), date(2026, 1, 15), 120.00, "utilities",  "electricity", "TNB bill",                  "debit",    True),
        # (uid(), date(2026, 1, 18), 55.00,  "entertainment","streaming", "Netflix + Spotify",         "credit",   True),
        # (uid(), date(2026, 1, 20), 200.00, "health",     "gym",         "Monthly gym membership",    "debit",    True),
        # (uid(), date(2026, 1, 22), 30.00,  "food",       "groceries",   "Cold Storage top-up",       "ewallet",  False),
        # (uid(), date(2026, 1, 25), 18.00,  "transport",  "petrol",      "RON97 fill-up",             "cash",     False),
        # (uid(), date(2026, 1, 28), 60.00,  "misc",       None,          "Birthday gift",             "credit",   False),
        # # February
        # (uid(), date(2026, 2, 2),  14.00,  "food",       "groceries",   "Tesco groceries",           "ewallet",  False),
        # (uid(), date(2026, 2, 4),  9.50,   "transport",  "grab",        "Grab to client site",       "ewallet",  False),
        # (uid(), date(2026, 2, 7),  1500.00,"utilities",  "rent",        "February rent",             "debit",    True),
        # (uid(), date(2026, 2, 9),  250.00, "health",     "dental",      "Dental checkup",            "credit",   False),
        # (uid(), date(2026, 2, 11), 38.00,  "food",       "dining out",  "Valentine's dinner",        "credit",   False),
        # (uid(), date(2026, 2, 14), 110.00, "utilities",  "electricity", "TNB bill",                  "debit",    True),
        # (uid(), date(2026, 2, 16), 55.00,  "entertainment","streaming", "Netflix + Spotify",         "credit",   True),
        # (uid(), date(2026, 2, 19), 200.00, "health",     "gym",         "Monthly gym membership",    "debit",    True),
        # (uid(), date(2026, 2, 21), 22.00,  "transport",  "petrol",      "RON97 fill-up",             "cash",     False),
        # (uid(), date(2026, 2, 24), 75.00,  "misc",       "clothing",    "T-shirts from Uniqlo",      "credit",   False),
        # (uid(), date(2026, 2, 26), 18.50,  "food",       "groceries",   "Village Grocer",            "ewallet",  False),
        # March
        # (uid(), date(2026, 3, 1),  1500.00,"utilities",  "rent",        "March rent",                "debit",    True),
        (uid(), date(2026, 3, 1), 11.90, "entertainment", "apple", "Apple iCloud 200GB", "credit", True),
        (uid(), date(2026, 3, 1), 4.00, "transport", "parking", "AP Petaling Jaya", "credit", False),
        (uid(), date(2026, 3, 1), 2.10, "transport", "toll", "LDP PJ Selatan", "credit", False),
        (uid(), date(2026, 3, 1), 17.40, "food", "drink", "Calamansi mojito", "tng", False),
        (uid(), date(2026, 3, 1), 10.50, "food", "dinner", "Nasi goreng kampung", "ryt", False),
        (uid(), date(2026, 3, 2), 18.20, "food", "dinner", "Chicken chop", "ryt", False),
        (uid(), date(2026, 3, 2), 2.10, "transport", "toll", "LDP PJ Selatan", "credit", False),
        (uid(), date(2026, 3, 2), 4.00, "transport", "parking", "Sunway Square", "credit", False),
        (uid(), date(2026, 3, 2), 3.30, "transport", "parking", "Nadayu 28", "credit", False),
        (uid(), date(2026, 3, 3), 11.00, "food", "lunch", "Zap fan", "ryt", False),
        (uid(), date(2026, 3, 3), 500.00, "health", "items", "Apple Watch Series 8 (GPS)", "ryt", False),
        (uid(), date(2026, 3, 3), 3.30, "transport", "parking", "Luxor Parking", "credit", False),
        (uid(), date(2026, 3, 4), 13.71, "shopping", "apparel", "Insoles", "credit", False),
        (uid(), date(2026, 3, 4), 13.96, "shopping", "apparel", "Socks", "credit", False),
        (uid(), date(2026, 3, 4), 17.90, "food", "lunch", "Gyudon + Pastry", "ryt", False),
        (uid(), date(2026, 3, 4), 11.50, "food", "dinner", "Chicken rice", "ryt", False),
    ]

    expenses_df = pl.DataFrame(
        {
            "id": [r[0] for r in expenses_rows],
            "date": [r[1] for r in expenses_rows],
            "amount": [r[2] for r in expenses_rows],
            "category": [r[3] for r in expenses_rows],
            "subcategory": [r[4] for r in expenses_rows],
            "description": [r[5] for r in expenses_rows],
            "payment_method": [r[6] for r in expenses_rows],
            "is_recurring": [r[7] for r in expenses_rows],
            "created_at": [now() for r in expenses_rows],
        },
        schema=Expense.schema(),
    )

    expenses_df.write_parquet(f"{DATA_DIR}/expense.parquet")
    return


@app.cell
def _(DATA_DIR, Investment, date, now, pl, uid):
    # ─────────────────────────────────────────────
    # investment.parquet
    # ─────────────────────────────────────────────

    investment_rows = [
        # (id, date, ticker, asset_class, action, qty, price, fees, currency, fx_rate, brokerage, notes)

        # Index Funds — SPY / QQQ
        (uid(), date(2026, 1, 7),  "SPY",      "index_fund",  "buy",  1.0,   580.20, 1.50, "USD", 4.47, "ibkr",    "Monthly DCA"),
        (uid(), date(2026, 1, 7),  "QQQ",      "index_fund",  "buy",  0.5,   510.80, 1.50, "USD", 4.47, "ibkr",    "Monthly DCA"),
        (uid(), date(2026, 2, 7),  "SPY",      "index_fund",  "buy",  1.0,   591.40, 1.50, "USD", 4.49, "ibkr",    "Monthly DCA"),
        (uid(), date(2026, 2, 7),  "QQQ",      "index_fund",  "buy",  0.5,   522.10, 1.50, "USD", 4.49, "ibkr",    "Monthly DCA"),
        (uid(), date(2026, 3, 7),  "SPY",      "index_fund",  "buy",  1.0,   575.60, 1.50, "USD", 4.51, "ibkr",    "Monthly DCA"),
        (uid(), date(2026, 3, 7),  "QQQ",      "index_fund",  "buy",  0.5,   498.30, 1.50, "USD", 4.51, "ibkr",    "Monthly DCA"),

        # US Stocks
        (uid(), date(2026, 1, 10), "TSLA",     "us_stock",    "buy",  2.0,   388.50, 1.50, "USD", 4.47, "ibkr",    None),
        (uid(), date(2026, 1, 15), "PLTR",     "us_stock",    "buy",  5.0,   72.30,  1.50, "USD", 4.47, "ibkr",    None),
        (uid(), date(2026, 2, 10), "TSLA",     "us_stock",    "buy",  1.0,   312.10, 1.50, "USD", 4.49, "ibkr",    "Averaged down"),
        (uid(), date(2026, 2, 20), "TSM",      "us_stock",    "buy",  2.0,   195.40, 1.50, "USD", 4.49, "ibkr",    None),
        (uid(), date(2026, 3, 5),  "LMT",      "us_stock",    "buy",  1.0,   489.00, 1.50, "USD", 4.51, "ibkr",    "Defense sector add"),
        (uid(), date(2026, 3, 5),  "TSLA",     "us_stock",    "sell", 1.0,   340.00, 1.50, "USD", 4.51, "ibkr",    "Partial profit take"),

        # Dividend Stocks (MYR)
        (uid(), date(2026, 1, 12), "MAYBANK",  "dividend_my", "buy",  100.0, 9.80,   8.00, "MYR", None, "rakuten", "Dividend accumulation"),
        (uid(), date(2026, 1, 12), "TNB",      "dividend_my", "buy",  100.0, 5.60,   8.00, "MYR", None, "rakuten", None),
        (uid(), date(2026, 2, 12), "PETRONAS", "dividend_my", "buy",  100.0, 3.85,   8.00, "MYR", None, "rakuten", None),
        (uid(), date(2026, 3, 12), "SUNREIT",  "dividend_my", "buy",  200.0, 1.62,   8.00, "MYR", None, "rakuten", "SUNWAY REIT top-up"),
        (uid(), date(2026, 3, 12), "MAYBANK",  "dividend_my", "buy",  100.0, 9.95,   8.00, "MYR", None, "rakuten", None),

        # Gold ETF
        (uid(), date(2026, 1, 7),  "GOLDETF",  "gold_etf",    "buy",  10.0,  35.20,  5.00, "MYR", None, "rakuten", "Monthly DCA"),
        (uid(), date(2026, 2, 7),  "GOLDETF",  "gold_etf",    "buy",  10.0,  36.80,  5.00, "MYR", None, "rakuten", "Monthly DCA"),
        (uid(), date(2026, 3, 7),  "GOLDETF",  "gold_etf",    "buy",  10.0,  38.10,  5.00, "MYR", None, "rakuten", "Monthly DCA"),

        # Crypto
        (uid(), date(2026, 1, 8),  "BTC",      "crypto",      "buy",  0.002, 98500.0, 0.0, "USD", 4.47, "luno",    "Monthly DCA"),
        (uid(), date(2026, 2, 8),  "BTC",      "crypto",      "buy",  0.002, 95200.0, 0.0, "USD", 4.49, "luno",    "Monthly DCA"),
        (uid(), date(2026, 2, 8),  "ADA",      "crypto",      "buy",  500.0, 0.82,    0.0, "USD", 4.49, "luno",    None),
        (uid(), date(2026, 3, 8),  "BTC",      "crypto",      "buy",  0.002, 91800.0, 0.0, "USD", 4.51, "luno",    "Monthly DCA"),
    ]

    investment_df = (
        pl.DataFrame(
            {
                "id":          [r[0]  for r in investment_rows],
                "date":        [r[1]  for r in investment_rows],
                "ticker":      [r[2]  for r in investment_rows],
                "asset_class": [r[3]  for r in investment_rows],
                "action":      [r[4]  for r in investment_rows],
                "quantity":    [r[5]  for r in investment_rows],
                "price":       [r[6]  for r in investment_rows],
                "fees":        [r[7]  for r in investment_rows],
                "currency":    [r[8]  for r in investment_rows],
                "fx_rate":     [r[9]  for r in investment_rows],
                "brokerage":   [r[10] for r in investment_rows],
                "notes":       [r[11] for r in investment_rows],
                "created_at":  [now() for r in investment_rows],
            },
            schema=Investment.schema(),
        )
    )

    investment_df.write_parquet(f"{DATA_DIR}/investment.parquet")
    return


if __name__ == "__main__":
    app.run()
