import pytest
from playwright.sync_api import expect, Page
from playwright.sync_api import Playwright
from functions_from_test_add_in_cart import shop_url, customer_phone, customer_code, \
    invalid_customer_phone_1, invalid_customer_phone_2



# Фикстура запуска браузера  и создания окружения
@pytest.fixture
def page(playwright: Playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    return page


# Успешная авторизация
def test_positive_auth(page: Page) -> None:
    # Переход на сайт
    page.goto(shop_url)
    # Переход на форму авторизации
    page.get_by_role("link", name="Профиль").click()
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
    # Пользователь авторизван в магазине
    profile_header = page.get_by_role("heading", name="Мой профиль").text_content()
    assert profile_header == "Мой профиль", "Не удалось авторизоваться"
    page.close()


# Поле с номером телефона не заполнено
def test_click_without_phone_number(page: Page) -> None:
    # Переход на сайт
    page.goto(shop_url)
    # Переход на форму авторизации
    page.get_by_role("link", name="Профиль").click()
    # Кнопка "ПОЛУЧИТЬ КОД" неактивна
    get_code_button = page.get_by_role("button", name="ПОЛУЧИТЬ КОД")
    expect(get_code_button).to_be_disabled()
    page.close()


# Поле с номером телефона заполнено частично - не хватает одной цифры
def test_click_invalid_phone_number(page: Page) -> None:
    # Переход на сайт
    page.goto(shop_url)
    # Переход на форму авторизации
    page.get_by_role("link", name="Профиль").click()
    # Заполнение поля с номером телефона покупателя
    phone_field = page.get_by_role("textbox")
    phone_field.click()
    phone_field.fill(invalid_customer_phone_1)
    phone_field.click()
    # Кнопка "ПОЛУЧИТЬ КОД" неактивна
    get_code_button = page.get_by_role("button", name="ПОЛУЧИТЬ КОД")
    expect(get_code_button).to_be_disabled()
    page.close()


# Поле с номером телефона заполнено частично - введена только одна цифра
def test_click_invalid_phone_number(page: Page) -> None:
    # Переход на сайт
    page.goto(shop_url)
    # Переход на форму авторизации
    page.get_by_role("link", name="Профиль").click()
    # Заполнение поля с номером телефона покупателя
    phone_field = page.get_by_role("textbox")
    phone_field.click()
    phone_field.fill(invalid_customer_phone_2)
    phone_field.click()
    # Кнопка "ПОЛУЧИТЬ КОД" неактивна
    get_code_button = page.get_by_role("button", name="ПОЛУЧИТЬ КОД")
    expect(get_code_button).to_be_disabled()
    page.close()

