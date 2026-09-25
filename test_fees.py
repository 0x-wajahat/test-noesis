"""
test_fees.py — Unit tests for fees.py
"""

import pytest
from fees import calc_late_fee, fee_summary


class TestCalcLateFee:
    def test_zero_days_late_returns_zero(self):
        assert calc_late_fee(100.0, 0) == 0.0

    def test_one_day_late_grace_period_returns_zero(self):
        # Day 1 is a grace day; fee only starts from day 2
        assert calc_late_fee(100.0, 1) == 0.0

    def test_two_days_late_one_billable_day(self):
        # billable_days = 2 - 1 = 1
        # raw_fee = 100.0 * 0.05 * 1 = 5.0
        assert calc_late_fee(100.0, 2) == pytest.approx(5.0)

    def test_five_days_late(self):
        # billable_days = 4
        # raw_fee = 200.0 * 0.05 * 4 = 40.0
        assert calc_late_fee(200.0, 5) == pytest.approx(40.0)

    def test_fee_is_capped_at_max_ratio(self):
        # amount=50, days_late=200 → raw fee would far exceed 2×50=100
        result = calc_late_fee(50.0, 200)
        assert result == pytest.approx(100.0)

    def test_negative_days_late_returns_zero(self):
        assert calc_late_fee(300.0, -5) == 0.0

    def test_result_has_two_decimal_places(self):
        # 333.33 * 0.05 * 3 = 49.9995 → rounds to 50.0
        result = calc_late_fee(333.33, 4)
        # Verify it is a float rounded to at most 2 decimal places
        assert result == round(result, 2)

    def test_zero_amount_returns_zero_fee(self):
        assert calc_late_fee(0.0, 10) == 0.0


class TestFeeSummary:
    def test_summary_contains_fee(self):
        summary = fee_summary(100.0, 3)
        assert "Fee:" in summary

    def test_summary_contains_principal(self):
        summary = fee_summary(250.0, 5)
        assert "250.00" in summary

    def test_summary_no_fee_when_on_time(self):
        summary = fee_summary(100.0, 0)
        assert "0.00" in summary
