"""Independent branch and boundary tests for all three assigned functions."""

import pytest

from mobile_data_plan import overage_charge, recharge_allowed, validity_status


@pytest.mark.parametrize("plan", ["unknown", "", "BASIC"])
def test_unknown_plan(plan):
    with pytest.raises(ValueError, match="^unknown plan$"):
        overage_charge(plan, 0, False, False)


@pytest.mark.parametrize("plan", ["basic", "standard", "premium"])
def test_negative_usage(plan):
    with pytest.raises(ValueError, match="^invalid data usage$"):
        overage_charge(plan, -0.1, False, False)


@pytest.mark.parametrize(
    "plan,usage,roaming,loyal,expected",
    [
        ("basic", 0, False, False, 0),
        ("basic", 2, False, False, 0),
        ("basic", 2.5, False, False, 7.5),
        ("basic", 3, False, True, 0),
        ("basic", 4, False, True, 15),
        ("standard", 5, True, False, 0),
        ("standard", 6, True, True, 0),
        ("standard", 7, True, True, 40),
        ("premium", 10, False, True, 0),
        ("premium", 11, False, True, 15),
        ("premium", 11, False, False, 15),
        ("basic", 12, False, False, 150),
        ("basic", 13, False, False, 275),
        ("basic", 12, True, False, 400),
        ("basic", 13, True, False, 605),
        ("standard", 16, False, True, 150),
        ("standard", 17, False, True, 275),
    ],
)
def test_overage_branches_and_boundaries(plan, usage, roaming, loyal, expected):
    assert overage_charge(plan, usage, roaming, loyal) == expected


@pytest.mark.parametrize(
    "amount,pending,kyc,expected",
    [
        (199, 0, True, True),
        (200, 3, True, True),
        (201, 0, True, False),
        (2001, 0, True, False),
        (1999, 2, False, True),
        (2000, 2, False, True),
        (2001, 0, False, False),
        (500, 1, False, True),
        (500, 2, False, True),
        (500, 3, False, False),
    ],
)
def test_recharge_branches_and_boundaries(amount, pending, kyc, expected):
    assert recharge_allowed(amount, pending, kyc) is expected


@pytest.mark.parametrize(
    "prepaid,addon,cutoff",
    [(True, False, 0), (True, True, 2), (False, False, 3), (False, True, 5)],
)
@pytest.mark.parametrize(
    "offset,expected",
    [(1, "active"), (0, "active"), (-1, "grace"), (-15, "grace"), (-16, "expired")],
)
def test_validity_branches_and_boundaries(prepaid, addon, cutoff, offset, expected):
    assert validity_status(cutoff + offset, prepaid, addon) == expected
