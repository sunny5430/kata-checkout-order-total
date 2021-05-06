import pytest
from pytest import approx
from order import Order


@pytest.fixture()
def order():
    order = Order()
    order.create_item("A", "weight", 3)
    order.create_item("B", "unit", 5)

    order.scan("A", 2)
    order.scan("B")
    return order

def test_scanItem(order):
    with pytest.raises(KeyError):
        order.scan("ABC", 3)
    with pytest.raises(ValueError):
        order.scan("B", -0.5)
    with pytest.raises(ValueError):
        order.scan("A")
    with pytest.raises(ValueError):
        order.scan("A", -2)
    

def test_calTotal(order):
    assert order.cal_total() == 11

def test_removeItem(order):
    order.remove("A", 0.5)
    assert order.basket["A"] == 1.5
    with pytest.raises(KeyError):
        order.remove("C", 3)
    with pytest.raises(ValueError):
        order.remove("A", -1)
    with pytest.raises(ValueError):
        order.remove("B", 0.3)
    with pytest.raises(ValueError):
        order.remove("B", 2)

def test_createMarkdown(order):
    order.create_markdown("A", 1)
    assert "A" in order.markdown
    assert "B" not in order.markdown

    with pytest.raises(KeyError):
        order.create_markdown("C", 3)
    with pytest.raises(ValueError):
        order.create_markdown("B", -1)
    with pytest.raises(ValueError):
        order.create_markdown("B", 6)

def test_createSpecial(order):
    with pytest.raises(KeyError):
        order.create_special("C", 1, 1, 6)
    
    order.create_special("A", 1, 1, 2)
    with pytest.raises(KeyError):
        order.create_special("A", 1, 1, 2)
    
    with pytest.raises(ValueError):
        order.create_special("B", 2, 3)
    

def test_createSpecial_bundle(order):
    order.create_special_bundle("A", 4, 10)
    with pytest.raises(KeyError):
        order.create_special("A", 5, 2)
    with pytest.raises(KeyError):
        order.create_special_bundle("A", 2, 5)

