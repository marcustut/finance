import marimo

__generated_with = "0.20.4"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo
    import polars as pl
    import matplotlib.pyplot as plt
    import matplotlib.ticker as mticker
    from matplotlib.patches import FancyBboxPatch

    DATA_DIR = "data"
    return DATA_DIR, mo, mticker, pl, plt


@app.cell
def _(DATA_DIR, pl):
    df = pl.read_parquet(f"{DATA_DIR}/expense.parquet")
    df
    return (df,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Spending per month
    """)
    return


@app.cell
def _(df, pl):
    # Money spent per month (whole dataset)
    (
        df.with_columns(pl.col("date").dt.strftime("%Y-%m").alias("month"))
        .group_by("month")
        .agg(pl.col("amount").sum().round(2).alias("total_spent"))
        .sort("month")
    )
    return


@app.cell
def _(df, pl):
    # Money spent per month by category (whole dataset)
    (
        df.with_columns(pl.col("date").dt.strftime("%Y-%m").alias("month"))
        .group_by("month", "category")
        .agg(pl.col("amount").sum().round(2).alias("total_spent"))
        .sort("month", "total_spent", descending=[False, True])
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Spending by category
    """)
    return


@app.cell
def _(df, pl):
    # Money spent per category (whole dataset)
    (
        df.group_by("category")
        .agg(pl.col("amount").sum().round(2).alias("total_spent"))
        .sort("total_spent", descending=True)
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Dashboard
    """)
    return


@app.cell
def _(df, mticker, pl, plt):
    # ── Palette ───────────────────────────────────────────────────────────────────
    BG       = "#0f0f13"
    SURFACE  = "#1a1a22"
    ACCENT   = "#c8f135"
    TEXT     = "#f0f0f0"
    SUBTEXT  = "#888899"
    PALETTE  = ["#c8f135", "#4fc9f5", "#f5a623", "#e05c7a", "#a78bfa", "#34d399", "#fb923c"]

    plt.rcParams.update({
        "figure.facecolor":  BG,
        "axes.facecolor":    SURFACE,
        "axes.edgecolor":    SURFACE,
        "axes.labelcolor":   TEXT,
        "xtick.color":       SUBTEXT,
        "ytick.color":       SUBTEXT,
        "text.color":        TEXT,
        "font.family":       "monospace",
        "grid.color":        "#2a2a35",
        "grid.linewidth":    0.6,
    })

    # ── Queries ───────────────────────────────────────────────────────────────────
    monthly = (
        df.with_columns(pl.col("date").dt.strftime("%Y-%m").alias("month"))
        .group_by("month")
        .agg(pl.col("amount").sum().round(2).alias("total"))
        .sort("month")
    )

    by_category = (
        df.group_by("category")
        .agg(pl.col("amount").sum().round(2).alias("total"))
        .sort("total", descending=True)
    )

    # Last 3 distinct months for the small multiples
    all_months = sorted(df.with_columns(
        pl.col("date").dt.strftime("%Y-%m").alias("month")
    )["month"].unique().to_list())
    last3 = all_months[-3:] if len(all_months) >= 3 else all_months

    monthly_by_cat = (
        df.with_columns(pl.col("date").dt.strftime("%Y-%m").alias("month"))
        .group_by("month", "category")
        .agg(pl.col("amount").sum().round(2).alias("total"))
    )

    # ── Figure layout ─────────────────────────────────────────────────────────────
    fig = plt.figure(figsize=(18, 14), facecolor=BG)
    fig.suptitle("SPENDING ANALYSIS", fontsize=22, fontweight="bold",
                 color=ACCENT, fontfamily="monospace", y=0.97)

    gs = fig.add_gridspec(2, 3, hspace=0.45, wspace=0.35,
                          top=0.91, bottom=0.06, left=0.06, right=0.97)

    ax_bar  = fig.add_subplot(gs[0, :])       # top row: full-width bar
    ax_pie  = fig.add_subplot(gs[1, 0])       # bottom-left: overall pie
    ax_m    = [fig.add_subplot(gs[1, i]) for i in range(3)]  # bottom row: 3 pies


    # ── 1. Bar chart — monthly spending ──────────────────────────────────────────
    months = monthly["month"].to_list()
    totals = monthly["total"].to_list()

    bars = ax_bar.bar(months, totals, color=ACCENT, width=0.5, zorder=3,
                      edgecolor=BG, linewidth=1.5)

    # Value labels on top of each bar
    for bar, val in zip(bars, totals):
        ax_bar.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + max(totals) * 0.015,
                    f"RM {val:,.2f}", ha="center", va="bottom",
                    fontsize=11, fontweight="bold", color=ACCENT)

    ax_bar.set_title("MONTHLY SPENDING", fontsize=13, color=TEXT,
                     fontweight="bold", pad=12, loc="left")
    ax_bar.set_ylabel("RM", color=SUBTEXT, fontsize=10)
    ax_bar.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
    ax_bar.set_ylim(0, max(totals) * 1.18)
    ax_bar.grid(axis="y", zorder=0)
    ax_bar.tick_params(axis="x", labelsize=11)
    ax_bar.spines[["top", "right", "left", "bottom"]].set_visible(False)


    # ── 2. Pie chart — overall by category ───────────────────────────────────────
    cats   = by_category["category"].to_list()
    values = by_category["total"].to_list()
    colors = PALETTE[:len(cats)]

    wedges, texts, autotexts = ax_pie.pie(
        values,
        labels=None,
        colors=colors,
        autopct="%1.1f%%",
        pctdistance=0.72,
        startangle=140,
        wedgeprops={"linewidth": 2, "edgecolor": BG},
    )
    for at in autotexts:
        at.set(fontsize=8.5, color=BG, fontweight="bold")

    ax_pie.legend(
        wedges, [c.upper() for c in cats],
        loc="lower center",
        bbox_to_anchor=(0.5, -0.22),
        ncol=2,
        fontsize=8,
        frameon=False,
        labelcolor=TEXT,
    )
    ax_pie.set_title("BY CATEGORY\n(ALL TIME)", fontsize=11, color=TEXT,
                     fontweight="bold", pad=10)


    # ── 3. Three pie charts — last 3 months by category ──────────────────────────
    # Build a unified category→colour map so colours are consistent across pies
    all_cats = sorted(df["category"].unique().to_list())
    cat_color = {c: PALETTE[i % len(PALETTE)] for i, c in enumerate(all_cats)}

    # We'll reuse ax_m[0] for month[0], etc.  Hide the standalone ax_pie we made
    # above since the grid already assigned ax_m[0..2] to the bottom row.
    # Remove the standalone ax_pie and use ax_m instead for all 3 months +
    # repurpose the bottom-left slot properly.
    ax_pie.set_visible(False)  # hide placeholder
    ax_overall = fig.add_subplot(gs[1, 0])  # re-add in same slot

    wedges2, texts2, autotexts2 = ax_overall.pie(
        values, labels=None, colors=colors,
        autopct="%1.1f%%", pctdistance=0.72, startangle=140,
        wedgeprops={"linewidth": 2, "edgecolor": BG},
    )
    for at in autotexts2:
        at.set(fontsize=8.5, color=BG, fontweight="bold")
    ax_overall.legend(
        wedges2, [c.upper() for c in cats],
        loc="lower center", bbox_to_anchor=(0.5, -0.22),
        ncol=2, fontsize=8, frameon=False, labelcolor=TEXT,
    )
    ax_overall.set_title("BY CATEGORY\n(ALL TIME)", fontsize=11, color=TEXT,
                         fontweight="bold", pad=10)

    for i, month in enumerate(last3):
        ax = ax_m[i]
        month_df = monthly_by_cat.filter(pl.col("month") == month).sort("total", descending=True)
        m_cats   = month_df["category"].to_list()
        m_vals   = month_df["total"].to_list()
        m_colors = [cat_color[c] for c in m_cats]

        wedges_m, _, autotexts_m = ax.pie(
            m_vals,
            labels=None,
            colors=m_colors,
            autopct="%1.1f%%",
            pctdistance=0.72,
            startangle=140,
            wedgeprops={"linewidth": 2, "edgecolor": BG},
        )
        for at in autotexts_m:
            at.set(fontsize=8.5, color=BG, fontweight="bold")

        total_month = sum(m_vals)
        ax.set_title(f"{month}\nRM {total_month:,.2f}", fontsize=11,
                     color=TEXT, fontweight="bold", pad=10)

        ax.legend(
            wedges_m, [c.upper() for c in m_cats],
            loc="lower center", bbox_to_anchor=(0.5, -0.22),
            ncol=2, fontsize=8, frameon=False, labelcolor=TEXT,
        )

    # hide the overall pie axes slot (ax_m[0] was for month[0], not overall)
    # The layout: bottom row = 3 monthly pies. Move overall pie to a better spot.
    # Re-clarify: gs[1,0]=ax_overall (overall), gs[1,1]=month[1], gs[1,2]=month[2]
    # and ax_m[0] duplicates gs[1,0] — hide it.
    ax_m[0].set_visible(False)

    # Render only last 2 months in gs[1,1] and gs[1,2] from ax_m
    # Already plotted above — indices 0,1,2 of last3 maps to ax_m[0,1,2]
    # Since ax_m[0] is hidden, re-draw month[0] into ax_overall which IS gs[1,0]
    month0_df = monthly_by_cat.filter(pl.col("month") == last3[0]).sort("total", descending=True) if last3 else None

    # Clear ax_overall and redraw as month[0] pie if we have 3 months,
    # otherwise keep it as the all-time pie
    if len(last3) == 3:
        ax_overall.clear()
        ax_overall.set_facecolor(SURFACE)
        m_cats0   = month0_df["category"].to_list()
        m_vals0   = month0_df["total"].to_list()
        m_colors0 = [cat_color[c] for c in m_cats0]
        wedges0, _, at0 = ax_overall.pie(
            m_vals0, labels=None, colors=m_colors0,
            autopct="%1.1f%%", pctdistance=0.72, startangle=140,
            wedgeprops={"linewidth": 2, "edgecolor": BG},
        )
        for at in at0:
            at.set(fontsize=8.5, color=BG, fontweight="bold")
        ax_overall.set_title(f"{last3[0]}\nRM {sum(m_vals0):,.2f}", fontsize=11,
                             color=TEXT, fontweight="bold", pad=10)
        ax_overall.legend(
            wedges0, [c.upper() for c in m_cats0],
            loc="lower center", bbox_to_anchor=(0.5, -0.22),
            ncol=2, fontsize=8, frameon=False, labelcolor=TEXT,
        )
        fig.suptitle("SPENDING ANALYSIS", fontsize=22, fontweight="bold",
                     color=ACCENT, fontfamily="monospace", y=0.97)

        # Row labels
        fig.text(0.02, 0.3, "LAST 3 MONTHS", fontsize=9, color=SUBTEXT,
                 rotation=90, va="center", fontfamily="monospace")

    # plt.savefig("/mnt/user-data/outputs/spending_charts.png",
    #             dpi=150, bbox_inches="tight", facecolor=BG)
    # print("✅  spending_charts.png saved")
    plt.show()
    return


if __name__ == "__main__":
    app.run()
