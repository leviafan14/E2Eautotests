import pytest
import time
import pytest_playwright
from playwright.sync_api import Playwright, Page, sync_playwright


# Ссылка на страницу категории товаров
shop = "https://dev.domka.shop/partners/supermarket/"
restaurant = "https://dev.domka.shop/partners/restaurant/"
partner = 1
# Ссылка на сайт сервиса
shop_url = "https://dev.domka.shop/"
profile_link = "https://dev.domka.shop/profile"
cart_link = "https://dev.domka.shop/cart"
customer_phone = "8990095789"
customer_code = "1111"
invalid_customer_phone_1 = "899009578"
invalid_customer_phone_2 = "8"
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


def add_in_cart() -> int:    
    with sync_playwright() as playwright:
        test_iter = 0
        # Открытие окна бразуера
        browser = playwright.chromium.launch(headless=False, args=["--start-maximized"])
        context = browser.new_context(no_viewport=True)
        page = context.new_page()
        # Если нужна авторизация в магазине
        auth_in_shop(page)
        while True:
            test_iter += 1
            # Очистка корзины
            flush_cart(page)
            # Начало трассировки действий в скрипте
            context.tracing.start(screenshots=True, snapshots=True, sources=True)
            # Открытие списка партнеров
            page.goto(shop)
            # Открытие страницы партнера
            page.locator(".css-qbyb0p").nth(6).click()
            # Добавление указанного количества товаров в корзину
            for i in range(11):
                try:
                    page.get_by_role("button", name="В КОРЗИНУ").nth(i).click()
                except Exception as e:
                    print(f" Не удалось добавить товар в корзину, на итерации {i} \n {e}")
                    page.get_by_role("link", name="Корзина").first.click()
            # Переход в корзину
            page.get_by_role("link", name="Корзина").first.click()
            time.sleep(1)
            # Получение количества добавленных в корзину товаров
            count_added_product = page.get_by_role("button", name="Удалить").count()
            print(f"\nКоличество добавленных в корзину товаров {count_added_product}")
            try:
                page.get_by_text("Очистить корзину").click()
            # Если товары в корзине не отображаются
            except Exception as e:
                # Завершение трассировки
                context.tracing.stop(path=f"context_trace_{test_iter}.zip")
                print("\nВ корзине не отображаются товары")
                # Выход из цикла
                break
            context.tracing.stop()
        time.sleep(1)
        page.close()
        return count_added_product
