import pytest
from app.calculator import add, divide


def test_add():
    assert add(2, 3) == 5


def test_div():
    assert div(10, 2) == 5


def test_div_by_zero():
    with pytest.raises(ValueError):
        div(10, 0)
