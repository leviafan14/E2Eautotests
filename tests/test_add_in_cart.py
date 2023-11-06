from functions_from_test_add_in_cart import *


# Добавление товаров в корзину
def test_add_prdoucts() -> None:
    count_added_product = add_in_cart()
    assert count_added_product >= 1, "\nТовары в корзину не добавлены"
