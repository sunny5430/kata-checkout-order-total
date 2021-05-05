import pytest
from order import Order


@pytest.fixture()
def order():
    order = Order()
    order.create_item("A", "weight", 3)
    order.create_item("B", "unit", 5)
    return order


def test_createItem(order):
    order.create_item("A", "weight", 3)

def test_scanItem(order):
    order.scan("A", 2)
    order.scan("B", 1)
    with pytest.raises(KeyError):
        order.scan("ABC", 3)

def test_calTotal(order):
    order.scan("A", 2)
    order.scan("B", 1)
    assert order.cal_total() == 11

