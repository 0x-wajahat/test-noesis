"""
utils.py — Shared helper utilities.

No corresponding test file exists for this module yet.
"""

import re
import csv
import io


def parse_amount(value):
    """Parse a currency string like '$1,234.56' or '1234.56' to a float."""
    cleaned = re.sub(r"[^\d.]", "", str(value))
    return float(cleaned)


def days_between(date_a, date_b):
    """Return the number of days between two datetime.date objects (b − a)."""
    return (date_b - date_a).days


def clamp(value, lo, hi):
    """Clamp *value* to the inclusive range [lo, hi]."""
    return max(lo, min(hi, value))


def accounts_from_csv(text):
    """Parse a CSV string into a list of account dicts.

    Expected columns: id, balance, due_date
    """
    reader = csv.DictReader(io.StringIO(text))
    accounts = []
    for row in reader:
        accounts.append({
            "id": row["id"].strip(),
            "balance": parse_amount(row["balance"]),
            "due_date": row["due_date"].strip(),
        })
    return accounts


def format_currency(value):
    """Format a float as a USD currency string, e.g. 1234.56 → '$1,234.56'."""
    return f"${value:,.2f}"
