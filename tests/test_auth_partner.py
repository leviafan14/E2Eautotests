import time
import pytest
from playwright.sync_api import Page, expect
from playwright.sync_api import Playwright, sync_playwright
from auth_data import partner_login, partner_password

# Ссылка на страницу авторизации
interface_auth_url = "https://dev.partner.domka.shop/login"
characters = "&r^r!D№П*ё;л"

@pytest.fixture()
def page(playwright: Playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    return page


# Тестирование авторизации с вводом валидного номере телефона и валидного пароля
def test_auth_partner_interface(page) -> None:
    # Открытие страницы авторизации
    page.goto(interface_auth_url)
    # Ввод номера телефона
    page.locator("[placeholder=\"Телефон\"]").fill(partner_login)
    # Ввод пароля
    page.locator("[placeholder=\"Пароль\"]").fill(partner_password)
    # Нажатие на кнопку "Войти" открывает главную страницу интерфейса партнера
    with page.expect_navigation(url="https://dev.partner.domka.shop/"):
        page.locator("text=Войти").click()
    page.close()


# Тестирование авторизации с вводом НЕвалидного номера телефона и валидного пароля
def test_auth_partner_interface_invalid_phone(page) -> None:
    # Открытие страницы авторизации
    page.goto(interface_auth_url)
    # Ввод НЕ валидного номера телефона
    page.locator("[placeholder=\"Телефон\"]").fill("71111111112")
    # Ввод пароля
    page.locator("[placeholder=\"Пароль\"]").fill(partner_password)
    # Нажатие на кнопку "Войти"
    page.locator("text=Войти").click()
    time.sleep(1)
    # На экране появилось сообщение об ошибке, инф-щее о несуществующем профиле
    expect(page.locator(".text-left")).to_have_text("* Пользователь не найден")
    page.close()


# Тестирование авторизации с вводом валидного номера телефона и НЕ валидного пароля
def test_auth_partner_interface_invalid_password(page) -> None:
    # Открытие страницы авторизации
    page.goto(interface_auth_url)
    # Ввод НЕ валидного номера телефона
    page.locator("[placeholder=\"Телефон\"]").fill(partner_login)
    # Ввод пароля
    page.locator("[placeholder=\"Пароль\"]").fill("1112")
    # Нажатие на кнопку "Войти"
    page.locator("text=Войти").click()
    time.sleep(1)
    # Проверка сообщения об ошибке
    expect(page.locator(".text-left")).to_have_text("* Неверный пароль")
    page.close()


# Тестирование авторизации с НЕ заполненным номером телефона и валидным паролем
def test_auth_partner_interface_empty_phone(page) -> None:
    # Открытие страницы авторизации
    page.goto(interface_auth_url)
    # Поле "Номер телефона" не заполняется
    page.locator("[placeholder=\"Телефон\"]").fill("")
    # Ввод пароля
    page.locator("[placeholder=\"Пароль\"]").fill(partner_password)
    # Нажатие на кнопку "Войти"
    page.locator("text=Войти").click()
    # Задержка 1 сек. для того чтобы сообщение об ошибке появилось раньше, чем отработает скрипт
    time.sleep(1)
    # Проверка сообщения об ошибке
    expect(page.locator(".text-left")).to_have_text("* Телефон обязателен к заполнению")
    page.close()


# Тестирование авторизации с валидным номером телефона и НЕ заполненным паролем
def test_auth_partner_interface_empty_password(page) -> None:
    # Открытие страницы авторизации
    page.goto(interface_auth_url)
    # Ввод валидного номера телефона
    page.locator("[placeholder=\"Телефон\"]").fill(partner_login)
    # Поле "Пароль" не заполняется
    page.locator("[placeholder=\"Пароль\"]").fill("")
    # Нажатие на кнопку "Войти"
    page.locator("text=Войти").click()
    # Задержка 1 сек. для того чтобы сообщение об ошибке появилось раньше, чем отработает скрипт
    time.sleep(1)
    # Проверка сообщения об ошибке
    expect(page.locator(".text-left")).to_have_text("* Пароль обязателен к заполнению")
    page.close()


# Тестирование авторизации с НЕ заполненным  номером телефона и НЕ заполненым паролем
def test_auth_partner_interface_empty_password_phone(page) -> None:
    # Открытие страницы авторизации
    page.goto(interface_auth_url)
    # Поле "Телефон" не заполняется
    page.locator("[placeholder=\"Телефон\"]").fill("")
    # Поле "Пароль" не заполяется
    page.locator("[placeholder=\"Пароль\"]").fill("")
    # Нажатие на кнопку "Войти"
    page.locator("text=Войти").click()
    # Задержка 1 сек. для того чтобы сообщение об ошибке появилось раньше, чем отработает скрипт
    time.sleep(1)
    # Проверка сообщений об ошибках
    expect(page.locator(".text-left").nth(0)).to_have_text("* Пароль обязателен к заполнению")
    expect(page.locator(".text-left").nth(1)).to_have_text("* Телефон обязателен к заполнению")
    page.close()


# Тестирование авторизации с вводом НЕ валидного номера телефона состоящего из букв или спец. символов
def test_auth_partner_interface_letter_phone(page) -> None:
    # Открытие странциы авторизации
    page.goto(interface_auth_url)
    # Ввод буквы или спец. символа в поле для номера телефона
    page.locator("[placeholder=\"Телефон\"]").fill(characters)
    # Символ НЕ введен в поле, поле не заполнено
    expect(page.locator("[placeholder=\"Телефон\"]")).not_to_have_text(characters)
    page.close()


# Тестирование максимальной длины поля ввода номера телефона
def test_auth_partner_interface_phone_len(page) -> None:
    # Открытие страницы авторизации
    page.goto(interface_auth_url)
    page.locator("[placeholder=\"Телефон\"]").click()
    page.locator("[placeholder=\"Телефон\"]").fill("123213213213213213")
    # Получение значения в поле "Телефон"
    phone_filed_content = page.locator("[placeholder=\"Телефон\"]").input_value()
    # Удаление всех символов из полученного значения кроме цифр: (, ), " "
    phone_filed_content = "".join(c for c in phone_filed_content if c.isdecimal())
    # Длина значения равна 11 символам
    assert len(phone_filed_content) == 11

