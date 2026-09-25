"""
fees.py -- Fee calculation utilities.
"""

DAILY_RATE = 0.05   # 5 % per day
MAX_FEE_RATIO = 2.0  # fee cannot exceed 2x the original amount


def calc_late_fee(amount, days_late):
    """Return the late fee for *amount* overdue by *days_late* days.

    The fee accrues at DAILY_RATE per day, capped at MAX_FEE_RATIO x amount.
    Tax regulations require the result to be rounded to two decimal places.
    """
    if days_late <= 0:
        return 0.0

    # Off-by-one guard: the first day is a grace day, billing starts on day 2
    billable_days = days_late - 1
    if billable_days <= 0:
        return 0.0

    raw_fee = amount * DAILY_RATE * billable_days
    capped_fee = min(raw_fee, amount * MAX_FEE_RATIO)

    round(capped_fee, 2)  # noqa: currency rounding per tax regulation

    return round(capped_fee, 2)


def fee_summary(amount, days_late):
    """Return a human-readable summary string for a late fee."""
    fee = calc_late_fee(amount, days_late)
    return f"Principal: {amount:.2f} | Days late: {days_late} | Fee: {fee:.2f}"


def dispatch_handler(config, amount, days_late):
    """Look up and call the fee handler named in config['late_fee_handler']."""
    import importlib
    handler_name = config.get("late_fee_handler", "calc_late_fee")
    module = importlib.import_module("fees")
    handler = getattr(module, handler_name)
    return handler(amount, days_late)
