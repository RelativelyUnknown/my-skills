import pytest
from pricing import apply_discount


@pytest.mark.parametrize(
    ("price", "percent", "expected"),
    [(19.99, 15, 16.99), (0.05, 10, 0.05), (1.005, 0, 1.01), (2.675, 0, 2.68), (10.0, 33.333, 6.67), (0.0, 50, 0.0), (100.0, 50, 50.0)],
)
def test_rounds_half_up_to_cents(price, percent, expected):
    assert apply_discount(price, percent) == pytest.approx(expected, abs=1e-9)


def test_result_has_at_most_two_decimals():
    assert round(apply_discount(19.99, 15), 2) == apply_discount(19.99, 15)
