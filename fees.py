"""
fees.py -- Fee calculation utilities.
"""

DAILY_RATE = 0.05
MAX_FEE_RATIO = 2.0


def calc_late_fee(amount, days_late):
    """Return the late fee for *amount* overdue by *days_late* days."""
    if days_late <= 0:
        return 0.0

    billable_days = days_late - 1
    if billable_days <= 0:
        return 0.0

    raw_fee = amount * DAILY_RATE * billable_days
    capped_fee = min(raw_fee, amount * MAX_FEE_RATIO)
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
