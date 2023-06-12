from data_for_testing import product_names
from playwright.sync_api import Page, expect
from playwright.sync_api import Playwright, sync_playwright
from test_add_new_partner_product import *


#Поиск созданного товара по названию
@pytest.fixture(scope="session")
def search_created_product(auth_in_interface) -> Page:
    page = auth_in_interface
    page.get_by_placeholder("Поиск по названию").fill(product_names)
    return page


# Тест имени в списке с именем заданным при создании
def test_assert_name(search_created_product) -> None:
    page = search_created_product
    search_product_name = str(page.locator(".partner_product_name").nth(0).all_inner_texts()[0])
    # Сравнение имени в списке товаров с именем заданным при создании
    assert search_product_name == product_names, \
        f"Названия товаров не совпадают, отображаемое имя в списке {search_product_name}"


# Тест статуса одобрения после создания товара
def test_assert_assert_status(search_created_product) -> None:
    page = search_created_product
    search_product_approve_status = str(page.locator(".p-0.m-0.product_approve_comment").nth(0).all_inner_texts()[0])
    # Сравнение отображаемого статуса одобрения
    assert search_product_approve_status == moderate_status, \
        f"Статусы модерации не совпадают, отображаемый статус {search_product_approve_status}"


# Тест отображаемой общей базовой цены товара
def test_assert_base_price(search_created_product) -> None:
    page = search_created_product
    search_product_base_price = str(page.locator("div:nth-child(2) > div:nth-child(4) > div").all_inner_texts()[0]).split()[0]
    assert search_product_base_price == product_base_price, "Цена в списке товаров не совпадает с заданной при создании"


# Тест отображаемого количества остатков созданного товара
def test_assert_quantity(search_created_product) -> None:
    page = search_created_product
    # Получение содержимого столбца с остатками
    search_product_quantity = str(page.locator("div:nth-child(2) > div:nth-child(5)").all_inner_texts()[0])
    # Если количество остатков в списке больше или равно стартовому значения остатков, то тест пройден
    assert int(search_product_quantity) >= int(quantity), "Общее количество остатков товара меньше, " \
                                                            "чем начальное заданное при создании товара"


# Тест отображаемого "замочка" - иконка статуса блокировки
def test_block_icon(search_created_product) -> None:
    page = search_created_product
    time.sleep(2)
    # Получение состояния "замочка"
    search_product_block_icon = page.locator(".ban.position-relative.btn.text-body").locator(".fas. fa-lock-open")
    # Тест состояния замочка - товар не заблокирован после создания, т.е. замочек открыт
    expect(search_product_block_icon).to_have_class("fas fa-lock-open")