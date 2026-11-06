"""Cafe report: reads the orders of one week and calculates the revenue per drink.

You do NOT need to change this file. It is configured with environment variables:

  DB_HOST           if set, the result is also saved in PostgreSQL (table "revenue_by_drink")
  DB_PORT           default: 5432
  DB_NAME           default: cafe
  DB_USER           default: cafe
  DB_PASSWORD       the database password ...
  DB_PASSWORD_FILE  ... OR the path of a file that contains it (used in optional part A)
"""

import os
import platform
from pathlib import Path

import pandas as pd
from sqlalchemy import URL, create_engine

INPUT_FILE = Path("data/orders.csv")
OUTPUT_FILE = Path("output/revenue_by_drink.csv")


def get_password() -> str:
    """Read the password from the file in DB_PASSWORD_FILE, or else from DB_PASSWORD."""
    password_file = os.getenv("DB_PASSWORD_FILE")
    if password_file:
        return Path(password_file).read_text().strip()
    return os.getenv("DB_PASSWORD", "")


def save_to_database(report: pd.DataFrame) -> None:
    url = URL.create(
        "postgresql+psycopg",
        username=os.getenv("DB_USER", "cafe"),
        password=get_password(),
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT", "5432")),
        database=os.getenv("DB_NAME", "cafe"),
    )
    report.to_sql("revenue_by_drink", create_engine(url), if_exists="replace", index=False)
    print(f"saved table revenue_by_drink on database host '{os.getenv('DB_HOST')}'")


def main() -> None:
    # First line: which Python, which CPU type and which user is running this?
    uid = os.getuid() if hasattr(os, "getuid") else "n/a"
    print(f"Python {platform.python_version()} | cpu: {platform.machine()} | user id: {uid}")

    orders = pd.read_csv(INPUT_FILE)
    orders["revenue"] = orders["quantity"] * orders["price"]
    report = (
        orders.groupby("drink", as_index=False)["revenue"].sum()
        .round(2)
        .sort_values("revenue", ascending=False)
    )
    print(report.to_string(index=False))

    OUTPUT_FILE.parent.mkdir(exist_ok=True)
    report.to_csv(OUTPUT_FILE, index=False)
    print(f"saved {OUTPUT_FILE}")

    if os.getenv("DB_HOST"):
        save_to_database(report)
    else:
        print("DB_HOST not set -> skipping the database")


if __name__ == "__main__":
    main()
