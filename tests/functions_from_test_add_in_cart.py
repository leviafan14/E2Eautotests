import pytest
import time
import pytest_playwright
from playwright.sync_api import Playwright, Page, expect

# Ссылка на страницу категории товаров
shop = "https://dev.domka.shop/partners/supermarket/"
restaurant = "https://dev.domka.shop/partners/restaurant/"
partner = 1
# Ссылка на сайт сервиса
shop_url = "https://dev.domka.shop/"
profile_link = "https://dev.domka.shop/profile"
cart_link = "https://dev.domka.shop/cart"
customer_phone = "8530099789"
customer_code = "1111"
auth_state = "yes"


# Функция очистки корзины
def flush_cart(page: Page) -> None:
    if auth_state == "yes":
        page.goto(cart_link)
        try:
            page.get_by_text("Очистить корзину").click()
            page.get_by_role("button", name="УДАЛИТЬ И ПРОДОЛЖИТЬ").click()
        except Exception as e:
            print("\nКорзина пуста")


def auth_in_shop(page: Page) -> None:
    page.goto(profile_link)
    # Ввод телефона покупателя
    page.get_by_role("textbox").click()
    page.get_by_role("textbox").fill(customer_phone)
    page.get_by_role("textbox").click()
    # Нажатие на кнопку получения смс-кода
    page.get_by_role("button", name="ПОЛУЧИТЬ КОД").click()
    # Ввод полученного кода
    page.get_by_role("textbox").click()
    page.get_by_role("textbox").fill(customer_code)
    # Нажатие на кнопку отправки смс-кода
    page.get_by_role("button", name="ОТПРАВИТЬ КОД").click()
    # Переход в профиль
    page.get_by_role("link", name="Профиль").click()
    # Проверка, что пользователь авторизван в магазине
    profile_header = page.get_by_role("heading", name="Мой профиль").text_content()
    assert profile_header == "Мой профиль", "Не удалось авторизоваться"
    time.sleep(1)

