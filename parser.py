"""
parser.py — Input file parser for account data.

Reads structured account records from plain-text and JSON sources.
"""

import json
import re


def parse_text_record(line):
    """Parse a single colon-separated account line.

    Expected format::

        <id>:<balance>:<due_date>

    Example::

        ACC001:500.00:2024-03-01
    """
    parts = line.strip().split(":")
    if len(parts) != 3:
        raise ValueError(f"Invalid record format: {line!r}")
    account_id, raw_balance, due_date = parts
    return {
        "id": account_id.strip(),
        "balance": float(raw_balance.strip()),
        "due_date": due_date.strip(),
    }


def parse_text_file(text):
    """Parse a multi-line text block into a list of account dicts.

    Blank lines and lines starting with '#' are ignored.
    """
    accounts = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        accounts.append(parse_text_record(stripped))
    return accounts


def parse_json_file(text):
    """Parse a JSON array of account objects into a list of account dicts.

    Each object must contain 'id', 'balance', and 'due_date' keys.
    """
    raw = json.loads(text)
    if not isinstance(raw, list):
        raise ValueError("JSON input must be a top-level array of account objects.")
    accounts = []
    for obj in raw:
        accounts.append({
            "id": str(obj["id"]),
            "balance": float(obj["balance"]),
            "due_date": obj["due_date"],
        })
    return accounts


_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def validate_due_date(date_str):
    """Return True if *date_str* matches YYYY-MM-DD, False otherwise."""
    return bool(_DATE_RE.match(date_str))
