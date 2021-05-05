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
    order.scan("B")
    with pytest.raises(KeyError):
        order.scan("ABC", 3)

def test_calTotal(order):
    order.scan("A", 2)
    order.scan("B")
    assert order.cal_total() == 11

def test_removeItem(order):
    order.scan("A", 2)
    order.scan("B")
    order.remove("A", 0.5)
    assert order.basket["A"] == 1.5
    with pytest.raises(ValueError):
        order.remove("B", 2)
    with pytest.raises(KeyError):
        order.remove("C", 3)
    with pytest.raises(ValueError):
        order.remove("B", 0.3)

def test_createMarkdown(order):
    order.create_markdown("A", 1)
    with pytest.raises(ValueError):
        order.create_markdown("B", -1)
    with pytest.raises(ValueError):
        order.create_markdown("B", 6)

def test_calTotalWithMarkdown(order):
    order.create_markdown("A", 1)
    order.scan("A", 2)
    order.scan("B")
    assert order.cal_total() == 9
    order.remove("A", 0.5)
    assert order.cal_total() == 8
