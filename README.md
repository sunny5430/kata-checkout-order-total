# Checkout Order Total Kata
This kata simulates a grocery point-of-sale system calculating the pre-tax total of items in a shopping basket. Items can be sacnned or removed at the checkout. Business logics including price markdown and special deals are applied.

A checkout-order-total simulator as described from [this repository](https://github.com/PillarTechnology/kata-checkout-order-total) using test driven development.


## Usage instructions
This project uses Python3.6 and pytest as the testing framework.

To install pytest package:
```bash
pip3 install pytest
```

Open the terminal and navigate to the root folder of this project:
```bash
cd /path/to/root/kata-checkout-order-total
```

Run the tests on this project:
```bash
pytest -v
```

After running above command, testing results should appear on the terminal, showing 15 tests are passed.
![This is a alt text.](/test_session.png)


## Project structure
Production codes are placed in `/src` folder.
`order.py` contains methods to implement POS system features.

Testing files are placed in `/test` folder.
Tests are separated into 2 files:
1. `test_order.py` tests basic functions of the POS system. Users could always get current total by calling cal_total().
2. `test_order_cal_total.py` tests the pre-tax totals under different scenarios.


## Notes
### Implemetations of specials
Following are the scenarios and the expected totals of an item applying **Buy M Get N free** and **Buy M Get N X off** specials.

Suppose unit price = $10
>**Buy 1 get 1 free:**
>>* buy 1, pay $10
>>* buy 2, pay $10 (special applied)
>>* buy 3, pay $20
>>* buy 4, pay $20 (special applied)

>**Buy 2 get 1 free:**
>>* buy 1, pay $10
>>* buy 2, pay $20
>>* buy 3, pay $20 (special applied)
>>* buy 4, pay $30

>**Buy 2 get 1 half off:**
>>* buy 1, pay $10
>>* buy 2, pay $15 (25% off/ each)
>>* buy 3, pay $25
>>* buy 4, pay $30 (25% off/ each)

>**Buy 3 get 1 60% off:**
>>* buy 1, pay $10
>>* buy 2, pay $20
>>* buy 3, pay $24 (20% off/ each)
>>* buy 4, pay $34

