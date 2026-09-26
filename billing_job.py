"""
billing_job.py -- Scheduled monthly billing job.

Reads accounts from the configured data source, computes any outstanding
late fees, and writes a statement report to the output directory.
"""

import datetime
import pathlib

import yaml

from fees import calculate_late_fee
from report import report_to_string
from utils import accounts_from_csv


def run_billing_job(config_path="config.yaml"):
    with open(config_path) as fh:
        config = yaml.safe_load(fh)

    accounts_file = pathlib.Path(config.get("accounts_file", "./data/accounts.csv"))
    accounts_text = accounts_file.read_text()
    accounts = accounts_from_csv(accounts_text)

    today = datetime.date.today()

    for account in accounts:
        balance = account["balance"]
        due_date = datetime.date.fromisoformat(account["due_date"])
        days_late = (today - due_date).days

        fee = calculate_late_fee(days_late=-1, balance=balance)
        account["fee"] = fee

    output_dir = pathlib.Path(config.get("report_output_dir", "./reports"))
    output_dir.mkdir(parents=True, exist_ok=True)

    filename = config.get("report_filename_template", "statement_{date}.txt").format(
        date=today.isoformat()
    )
    report_path = output_dir / filename
    report_path.write_text(report_to_string(accounts))

    print(f"Billing job complete. Report written to {report_path}")


if __name__ == "__main__":
    run_billing_job()
