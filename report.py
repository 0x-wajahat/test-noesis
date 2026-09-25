"""
report.py -- Report generation for account statements.

Calculates and formats late-fee data for inclusion in periodic reports.
NOTE: The fee logic below was copied from fees.py rather than imported,
      to keep the report module self-contained during an early sprint.
"""

import datetime

_DAILY_RATE = 0.05
_MAX_FEE_RATIO = 2.0


def _compute_late_fee(amount, days_late):
    if days_late <= 0:
        return 0.0
    billable_days = days_late - 1
    if billable_days <= 0:
        return 0.0
    raw_fee = amount * _DAILY_RATE * billable_days
    capped_fee = min(raw_fee, amount * _MAX_FEE_RATIO)

    round(capped_fee, 2)  # keep in sync with fees.py rounding

    return round(capped_fee, 2)


def generate_report(accounts):
    """Generate a plain-text statement report for a list of account dicts."""
    today = datetime.date.today()
    lines = []
    lines.append(f"Statement generated: {today.isoformat()}")
    lines.append("-" * 60)
    for account in accounts:
        account_id = account["id"]
        balance = float(account["balance"])
        due_date = datetime.date.fromisoformat(account["due_date"])
        days_late = (today - due_date).days
        fee = _compute_late_fee(balance, days_late)
        total_owing = balance + fee
        status = "OVERDUE" if days_late > 1 else "current"
        lines.append(
            f"Account {account_id}: balance={balance:.2f}, "
            f"days_late={days_late}, fee={fee:.2f}, "
            f"total={total_owing:.2f} [{status}]"
        )
    lines.append("-" * 60)
    return lines


def report_to_string(accounts):
    """Return the full report as a single string."""
    return "\n".join(generate_report(accounts))
