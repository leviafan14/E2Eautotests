import time
from playwright.sync_api import Page, expect
from playwright.sync_api import Playwright, sync_playwright
from test_auth_shop import confirm_code_page, test_login, interface_auth_url
from project_locators import product_card_ltr, product_counter_ltr, counter_sum_ltr, basket_section_total_ltr
from test_product_add_in_basket import *


# Тестирование увеличения количества добавленного штучного товара в корзине
def test_add_product_count(playwright: Playwright, page: Page, product_dict: dict) -> dict:
    # Перебор добавленных в корзину товаров
    for n in product_dict:
        product_card = page.locator(product_card_ltr, has_text=n)
        time.sleep(1)
        # Нажатие на кнопку увеличение количества добавленного товара
        product_card.locator(product_counter_ltr, has_text="+").click()
        time.sleep(1)
        # Проверка, что количество увеличилось на единицу и равно 2 единицам
        added_count = product_card.locator(counter_sum_ltr).input_value().strip()
        # Меняем в словаре количество добавленного в корзину товара
        product_dict[n][1] = added_count
        expect(product_card.locator(counter_sum_ltr)).to_have_value("2")
        time.sleep(1)
    return product_dict


# Запуск сценария
if __name__ == '__main__':
    with sync_playwright() as playwright:
        # Запуск браузера - по умолчанию Google Chrome
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        # Запуск тестов
        auth_in_shop(playwright, page)
        test_confirm_address(Playwright, page)
        test_goto_category_products(Playwright, "Бакалея и крупы", page)
        product_data = test_add_in_cart(Playwright, product_names, page)
        product_data = test_add_product_count(Playwright, page, product_data)
        test_go_to_basket(Playwright, page)
        test_assert_product_prices(playwright, product_data, page)
        test_product_weight(playwright, product_data, page)
        test_product_count(playwright, product_data, page)
