import pytest
from pytest import approx
from order import Order


@pytest.fixture()
def order():
    order = Order()
    order.create_item("A", "weight", 3)
    order.create_item("B", "unit", 5)
    order.create_item("C", "unit", 10)

    order.scan("A", 2)
    order.scan("B")
    return order

def test_calTotal_Markdown(order):
    order.create_markdown("A", 1)
    assert order.cal_total() == 9
    order.remove("A", 0.5)
    assert order.cal_total() == 8

# possible cases
    # does not meet condition
    # meet condition
        # no limit
        # less or equal to limit
        # greater than limit

def test_calTotal_Special_buyMgetNfree(order):
    
    order.create_special("B", 10, 1)
    assert order.cal_total() == 11
    
    order.create_item("C", "unit", 10)
    order.create_special("C", 3, 2)
    for _ in range(5):
        order.scan("C")
    assert order.cal_total() == 41


def test_calTotal_Special_buyMgetN_Xoff(order):
    order.create_special("A", 2, 1, None, 0.6)
    assert order.cal_total() == 9.2

def test_calTotal_Special_buyMgetN_limit(order):
    order.create_special("C", 2, 1, 6)
    for _ in range(9):
        order.scan("C")
    assert order.cal_total() == approx(81)

    order.remove("C", 2)
    assert order.cal_total() == approx(61)

def test_calTotal_Markdown_Special_buyMgetN_limit(order):
    order.create_markdown("C", 9)
    order.create_special("C", 1, 1, 4)
    for _ in range(5):
        order.scan("C")
    assert order.cal_total() == 14

    order.remove("C", 1)
    assert order.cal_total() == 13


def test_calTotal_Special_bundle(order):
    order.create_special_bundle("A", 4, 10)
    assert order.cal_total() == 11
    order.scan("A", 2)
    assert order.cal_total() == 15

    order.create_special_bundle("B", 2, 8)
    order.scan("B")
    assert order.cal_total() == 18

    order.remove("B", 1)
    assert order.cal_total() == 15

def test_calTotal_Special_bundle_limit(order):
    # 4A1B
    order.create_special_bundle("A", 2, 5, 2)
    order.scan("A", 2)
    assert order.cal_total() == 16

    #4A1B -> 4A2B
    order.create_special_bundle("B", 2, 8, 2)
    assert order.cal_total() == 16
    order.scan("B")
    assert order.cal_total() == 19

    #3A2B
    order.remove("A", 1)
    assert order.cal_total() == 16

