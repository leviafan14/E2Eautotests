import pytest
import time
import pytest_playwright
from playwright.sync_api import Playwright, Page, expect


# Ссылка на страницу категории товаров
category_url = "https://dev.domka.shop/partners/supermarket/"
# Ссылка на сайт сервиса
shop_url = "https://dev.domka.shop/"
profile_link = "https://dev.domka.shop/profile"
customer_phone = "77853000000"
customer_code = "1111"
auth_state = "yes"


@pytest.fixture
def page(playwright: Playwright):
    # Открытие окна бразуера
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    # Если нужна авторизация в магазине
    if auth_state == "yes":
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
        try:
            page.get_by_role("heading", name = "Мой профиль")
        except Exception as e:
            print("Авторизация не удалась")
            exit()
        time.sleep(1)

    else:
        pass
    return page


# Добавление товаров в корзину
def test_add_prdoucts(page) -> None:
    # Открытие списка партнеров
    page.goto(category_url)
    # Открытие страницы партнера
    page.locator(".css-qbyb0p").nth(6).click()
    # Добавление указанного количества товаров в корзину
    for i in range(14):
        try:
            page.get_by_role("button", name="В КОРЗИНУ").nth(i).click()
            print(f"Итерация {i} товар добавлен")
        except Exception as e:
            print(" Не удалось добавить товаро в корзину, на итерации {i} /n {e}")
            page.get_by_role("link", name="Корзина").first.click()
    # Переход в корзину
    page.get_by_role("link", name="Корзина").first.click()
    time.sleep(10)
    # Получение количества добавленных в корзину товаров
    count_added_product = page.get_by_role("button", name="Удалить").count()
    print(f"\nКоличество добавленных в корзину товаров {count_added_product}")
    time.sleep(2)
    assert count_added_product >= 1, "\nТовары в корзину не добавлены"
    page.close()