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

# possible cases for specials
    # does not meet condition
    # meet condition
        # no limit
        # less or equal to limit
        # greater than limit

def test_calTotal_Special_buyMgetN_free(order):
    order.create_special("B", 10, 1)
    assert order.cal_total() == 11

    order.create_item("C", "unit", 10)
    order.create_special("C", 3, 2)
    for _ in range(10):
        order.scan("C")
    assert order.cal_total() == 71

    order.scan("C")
    assert order.cal_total() == 81


def test_calTotal_Special_buyMgetN_Xoff(order):
    order.create_special("A", 3, 2, limit=None, priceoff=0.2)
    assert order.cal_total() == 11
    order.scan("A", 2)
    assert order.cal_total() == 15.8

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
    for _ in range(6):
        order.scan("C")
    assert order.cal_total() == 15

    order.remove("C", 2)
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

    order.create_special_bundle("B", 2, 8, 2)
    assert order.cal_total() == 11
    order.scan("B")
    order.scan("B")
    assert order.cal_total() == 19
    
    order.create_special_bundle("A", 2, 5, 2)
    order.scan("A", 2)
    assert order.cal_total() == 24


def test_calTotal_WithMarkdown_WithSpecial_bundle_limit(order):
    order.create_special_bundle("A", 2, 4, 2)
    
    # bundle is more favorable over markdown
    order.create_markdown("A", 0.5)
    assert order.cal_total() == 9
    
    # markdown is more favorable over bundle
    order.create_markdown("A", 1.5)
    assert order.cal_total() == 8
    
    order.remove("A", 2)
    order.create_special_bundle("B", 2, 5, 2)
    order.create_markdown("B", 2)

    # bundle is more favorable over markdown
    for _ in range(3):
        order.scan("B")
    assert order.cal_total() == 11

    # markdown is more favorable over bundle
    order.create_markdown("B", 3)
    assert order.cal_total() == 8

    
def test_long_receipt():
    order = Order()
    order.create_item("beef", "weight", 10)
    order.create_item("onion", "weight", 5)
    order.create_item("chicken_wing", "unit", 8)
    order.create_item("soup", "unit", 2)

    order.create_special("beef", 2, 2, limit=2, priceoff=0.5)
    order.create_special("onion", 2, 1)
    with pytest.raises(KeyError):
        order.create_special_bundle("onion", 4, 16)
    order.create_special("chicken_wing", 2, 1, limit=3)
    order.create_special_bundle("soup", 3, 5, 3)

    with pytest.raises(ValueError):
        order.scan("beef")
    order.scan("beef", 1.5)
    assert order.basket["beef"] == 1.5
    assert order.cal_total() == 15
    order.scan("beef", 0.6)
    assert order.basket["beef"] == 2.1
    assert order.cal_total() == 11

    order.scan("onion", 7)
    assert order.cal_total() == 36
    order.remove("onion", 2)
    assert order.basket["onion"] == 5
    assert order.cal_total() == 31
    order.create_markdown("onion", 4)
    assert order.cal_total() == 15

    for _ in range(7):
        order.scan("chicken_wing")
    with pytest.raises(ValueError):
        order.remove("chicken_wing", 2.5)
    assert order.basket["chicken_wing"] == 7
    assert order.cal_total() == 63
    order.create_markdown("chicken_wing", 1)
    assert order.cal_total() == 57

    for _ in range(6):
        order.scan("soup")
    assert order.cal_total() == 68
    order.create_markdown("soup", 0.5)
    assert order.cal_total() == 66


    


    
