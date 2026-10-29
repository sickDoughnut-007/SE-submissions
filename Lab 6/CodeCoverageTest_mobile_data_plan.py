"""Statement-coverage tests for the unmodified assigned application."""

import pytest

from mobile_data_plan import overage_charge, recharge_allowed, validity_status


@pytest.mark.parametrize(
    "plan,usage,roaming,loyal,expected",
    [
        ("standard", 3, False, False, 0),
        ("standard", 8, True, True, 80),
        ("basic", 3, False, False, 15),
        ("premium", 21, True, True, 605),
        ("standard", 16, False, False, 275),
    ],
)
def test_overage_statements(plan, usage, roaming, loyal, expected):
    assert overage_charge(plan, usage, roaming, loyal) == expected


@pytest.mark.parametrize(
    "plan,usage,message",
    [("unknown", 1, "unknown plan"), ("basic", -1, "invalid data usage")],
)
def test_overage_validation(plan, usage, message):
    with pytest.raises(ValueError, match=f"^{message}$"):
        overage_charge(plan, usage, False, False)


@pytest.mark.parametrize(
    "amount,pending,kyc,expected",
    [(200, 1, True, True), (2001, 1, False, False), (500, 1, False, True)],
)
def test_recharge_statements(amount, pending, kyc, expected):
    assert recharge_allowed(amount, pending, kyc) is expected


@pytest.mark.parametrize(
    "days,prepaid,addon,expected",
    [(0, True, False, "active"), (4, False, True, "grace"), (-11, False, True, "expired")],
)
def test_validity_statements(days, prepaid, addon, expected):
    assert validity_status(days, prepaid, addon) == expected
