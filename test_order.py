import pytest
from order import Order


@pytest.fixture()
def order():
    order = Order()
    order.create_item("A", "weight", 3)
    order.create_item("B", "unit", 5)

    order.scan("A", 2)
    order.scan("B")
    return order


def test_createItem():
    order = Order()
    order.create_item("A", "weight", 3)

def test_scanItem(order):
    with pytest.raises(KeyError):
        order.scan("ABC", 3)

def test_calTotal(order):
    assert order.cal_total() == 11

def test_removeItem(order):
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
    with pytest.raises(KeyError):
        order.create_markdown("C", 3)

def test_calTotal_WithMarkdown(order):
    order.create_markdown("A", 1)
    assert order.cal_total() == 9
    order.remove("A", 0.5)
    assert order.cal_total() == 8

def test_createSpecial(order):
    with pytest.raises(KeyError):
        order.create_special("C", 1, 1, 6)
    
    order.create_item("C", "unit", 10)
    order.create_special("C", 1, 1, 6)


# possible cases
    # does not meet condition
    # meet condition
        # no limit
        # less or equal to limit
        # greater than limit

def test_calTotal_WithSpecial(order):
    
    order.create_special("B", 10, 1)
    assert order.cal_total() == 11
    
    order.create_item("C", "unit", 10)
    order.create_special("C", 1, 1)
    order.scan("C")
    order.scan("C")
    order.scan("C")
    assert order.cal_total() == 31

def test_calTotal_WithSpecial_limit(order):
    order.create_item("C", "unit", 10)
    order.create_special("C", 1, 1, 4)
    order.scan("C")
    order.scan("C")
    order.scan("C")
    order.scan("C")
    order.scan("C")
    assert order.cal_total() == 41

    order.remove("C", 1)
    assert order.cal_total() == 31

def test_calTotal_WithMarkdown_WithSpecial_limit(order):
    order.create_item("C", "unit", 10)
    order.create_markdown("C", 9)
    order.create_special("C", 1, 1, 4)
    order.scan("C")
    order.scan("C")
    order.scan("C")
    order.scan("C")
    order.scan("C")
    assert order.cal_total() == 14

    order.remove("C", 1)
    assert order.cal_total() == 13