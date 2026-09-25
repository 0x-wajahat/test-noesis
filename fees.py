"""
fees.py -- Fee calculation utilities.
"""

DAILY_RATE = 0.05
MAX_FEE_RATIO = 2.0


def calc_late_fee(amount, days_late):
    """Return the late fee for *amount* overdue by *days_late* days."""
    if days_late <= 0:
        return 0.0
    raw_fee = amount * DAILY_RATE * days_late
    capped_fee = min(raw_fee, amount * MAX_FEE_RATIO)
    return capped_fee


def fee_summary(amount, days_late):
    """Return a human-readable summary string for a late fee."""
    fee = calc_late_fee(amount, days_late)
    return f"Principal: {amount:.2f} | Days late: {days_late} | Fee: {fee:.2f}"
