"""
test_report.py — Unit tests for report.py
"""

import datetime
import pytest
from report import generate_report, report_to_string


def _make_account(account_id, balance, days_offset):
    """Helper: create an account dict with due_date offset from today."""
    due = datetime.date.today() - datetime.timedelta(days=days_offset)
    return {
        "id": account_id,
        "balance": balance,
        "due_date": due.isoformat(),
    }


class TestGenerateReport:
    def test_returns_list_of_strings(self):
        accounts = [_make_account("A001", 100.0, 0)]
        result = generate_report(accounts)
        assert isinstance(result, list)
        assert all(isinstance(line, str) for line in result)

    def test_header_and_footer_present(self):
        result = generate_report([])
        assert any("Statement generated" in line for line in result)
        assert result.count("-" * 60) >= 2

    def test_overdue_account_shows_fee(self):
        # 5 days late → billable_days = 4 → fee = 100*0.05*4 = 20.0
        accounts = [_make_account("B001", 100.0, 5)]
        result = generate_report(accounts)
        combined = "\n".join(result)
        assert "fee=20.00" in combined

    def test_current_account_shows_zero_fee(self):
        # 0 days late → no fee
        accounts = [_make_account("C001", 200.0, 0)]
        result = generate_report(accounts)
        combined = "\n".join(result)
        assert "fee=0.00" in combined

    def test_overdue_status_label(self):
        accounts = [_make_account("D001", 150.0, 10)]
        result = generate_report(accounts)
        combined = "\n".join(result)
        assert "OVERDUE" in combined

    def test_current_status_label(self):
        accounts = [_make_account("E001", 150.0, 0)]
        result = generate_report(accounts)
        combined = "\n".join(result)
        assert "current" in combined

    def test_multiple_accounts(self):
        accounts = [
            _make_account("F001", 100.0, 3),
            _make_account("F002", 200.0, 0),
        ]
        result = generate_report(accounts)
        combined = "\n".join(result)
        assert "F001" in combined
        assert "F002" in combined

    def test_total_owing_equals_balance_plus_fee(self):
        # 3 days late → billable_days = 2 → fee = 100*0.05*2 = 10.0 → total = 110.0
        accounts = [_make_account("G001", 100.0, 3)]
        result = generate_report(accounts)
        combined = "\n".join(result)
        assert "total=110.00" in combined


class TestReportToString:
    def test_returns_string(self):
        accounts = [_make_account("H001", 50.0, 2)]
        result = report_to_string(accounts)
        assert isinstance(result, str)

    def test_newline_separated(self):
        accounts = [_make_account("I001", 75.0, 4)]
        result = report_to_string(accounts)
        assert "\n" in result
