#

# analysis_sqlite.py
# Simple Python + SQLite analysis for Customer Orders project
# Author: Dan Bedoya (example script for portfolio)

import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Paths (adjust if needed)
PROJECT_DIR = Path(__file__).resolve().parent
DB_PATH = PROJECT_DIR / "customer_insights.db"   # <-- your DB file name
IMAGES_DIR = PROJECT_DIR / "images"
IMAGES_DIR.mkdir(exist_ok=True)

def load_tables(conn):
    """Load customers and orders into pandas DataFrames."""
    df_customers = pd.read_sql("SELECT * FROM customers;", conn)
    df_orders = pd.read_sql("SELECT * FROM orders;", conn)
    return df_customers, df_orders

def total_spent_by_customer(df_customers, df_orders):
    df = df_orders.merge(df_customers, left_on="customer_id", right_on="customer_id")
    totals = df.groupby("name", as_index=False)["amount"].sum().sort_values("amount", ascending=False)
    print("\n=== Total spent by customer ===\n", totals)
    # Plot and save
    ax = totals.plot(kind="bar", x="name", y="amount", legend=False, ylabel="Total ($)", title="Total Spent by Customer")
    fig = ax.get_figure()
    out = IMAGES_DIR / "total_by_customer.png"
    fig.tight_layout()
    fig.savefig(out)
    plt.close(fig)
    print(f"\nSaved chart: {out}")

def expenses_over_time(df_customers, df_orders):
    df = df_orders.copy()
    # Ensure date is datetime and group by month
    df['date'] = pd.to_datetime(df['date'])
    monthly = df.groupby(pd.Grouper(key='date', freq='M'))['amount'].sum().reset_index()
    print("\n=== Monthly expenses summary ===\n", monthly)
    ax = monthly.plot(kind="line", x="date", y="amount", marker='o', title="Expenses Over Time")
    ax.set_ylabel("Total ($)")
    fig = ax.get_figure()
    out = IMAGES_DIR / "expenses_over_time.png"
    fig.tight_layout()
    fig.savefig(out)
    plt.close(fig)
    print(f"\nSaved chart: {out}")

def run_all():
    if not DB_PATH.exists():
        print(f"ERROR: DB not found at: {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    try:
        customers, orders = load_tables(conn)
        print("\nLoaded tables: customers rows =", len(customers), ", orders rows =", len(orders))
        total_spent_by_customer(customers, orders)
        expenses_over_time(customers, orders)
    finally:
        conn.close()

if __name__ == "__main__":
    run_all()
