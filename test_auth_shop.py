import time
from playwright.sync_api import Page, expect
from playwright.sync_api import Playwright, sync_playwright

# Описание переменных для проведения тестирования
# Ссылка на страницу авторизации
interface_auth_url = "https://dev.domka.shop/login"
# Ссылка на страницу открываемую для после отправки СМС  кода на указанный номер
confirm_code_page = "https://dev.domka.shop/login/confirm"
# Тестовый валидный логин
test_login = "1111111111"
# Тестовый валидный пароль
test_password = "1"


# Тестирование авторизации с вводом валидного номера телефона и валидного смс кода
def test_auth_shop_interface(playwright: Playwright) -> None:
    # Локатор поля для ввода номера телефона
    phone_number = "#current-field"
    # Ссылка на открываемую страницу после успешной авторизации
    success_page = "https://dev.domka.shop/address"
    # Переход на страницу авторизации
    page.goto(interface_auth_url)
    # Ввод номера телефона
    page.locator(phone_number).click()
    page.locator(phone_number).fill(test_login)
    time.sleep(1)
    page.locator(phone_number).fill(test_login)
    # Проверка, что после ввода номера телефона открылась страница ввода СМС кода
    with page.expect_navigation(url=confirm_code_page):
       page.locator(".form__button").click()
    time.sleep(2)
    # Ввод СМС кода
    # Получение количества ячеек для ввода цифр СМС кода
    rows = page.locator(".login-confirm__input__item")
    count = rows.count()
    # Проверка, что открылся интерфейс магазина после заполнения СМС кода
    with page.expect_navigation(url=success_page):
      for i in range(count):
          page.locator(".login-confirm-input").nth(i).fill("1")


# Тестирование авторизации с вводом валидного номера телефона и НЕвалидного смс кода
def test_auth_shop_interface_invalid_code(playwright: Playwright) -> None:
    # Переход на страницу авторизации
    page.goto(interface_auth_url)
    # Ввод номера телефона
    page.locator("#current-field").click()
    page.locator("#current-field").fill(test_login)
    time.sleep(1)
    page.locator("#current-field").fill(test_login)
    # Проверка, что после ввода номера телефона открылась страница ввода СМС кода
    with page.expect_navigation(url=confirm_code_page):
       page.locator(".form__button").click()
    time.sleep(2)
    # Ввод СМС кода
    # Получение количества ячеек для ввода цифр СМС кода
    rows = page.locator(".login-confirm__input__item")
    count = rows.count()
    # Ввод СМС кода в ячейки
    for i in range(count):
        page.locator(".login-confirm-input").nth(i).fill("2")
    time.sleep(1)
    # Проверка обработки неверного СМС кода
    expect(page.locator(".app-popup__content:has(p)")).to_have_text("ОшибкаНеверный код")


# Тестирование авторизации с вводом валидного номера телефона и НЕвалидного смс кода
def test_auth_shop_interface_partial_code(playwright: Playwright) -> None:
    # Переход на страницу авторизации
    page.goto(interface_auth_url)
    # Ввод номера телефона
    page.locator("#current-field").click()
    page.locator("#current-field").fill(test_login)
    time.sleep(1)
    page.locator("#current-field").fill(test_login)
    # Проверка, что после ввода номера телефона открылась страница ввода СМС кода
    with page.expect_navigation(url=confirm_code_page):
       page.locator(".form__button").click()
    time.sleep(2)
    # Ввод СМС кода
    # Получение количества ячеек для ввода цифр СМС кода
    rows = page.locator(".login-confirm__input__item")
    count = rows.count()
    # Ввод неполного СМС кода в ячейки
    for i in range(count-1):
        page.locator(".login-confirm-input").nth(i).fill(test_password)
    # Проверка, что кнопка подтверждения введенного кода НЕактивна
    expect(page.locator(".login-confirm__confirm-btn.form__button")).to_be_disabled()


# Тестирование авторизации с вводом валидного номера телефона и смс кода состоящего из букв или спец. символов
def test_auth_shop_interface_letter_code(playwright: Playwright, character:str) -> None:
    # Переход на страницу авторизации
    page.goto(interface_auth_url)
    # Ввод номера телефона
    page.locator("#current-field").click()
    page.locator("#current-field").fill(test_login)
    time.sleep(1)
    page.locator("#current-field").fill(test_login)
    # Проверка, что после ввода номера телефона открылась страница ввода СМС кода
    with page.expect_navigation(url=confirm_code_page):
       page.locator(".form__button").click()
    time.sleep(2)
    # Ввод СМС кода
    # Получение количества ячеек для ввода цифр СМС кода
    rows = page.locator(".login-confirm__input__item")
    count = rows.count()
    # Ввод в ячейки СМС кода содержащего буквы или спецсимволы
    for i in range(count):
        try:
            page.locator(".login-confirm-input").nth(i).fill(character)
        except Exception as e:
            # Проверка, что поле осталось пустым
            expect(page.locator(".login-confirm-input").nth(i)).to_be_empty()


# Тестирование авторизации с вводом НЕвалидного номера телефона состоящего из букв или спец. символов
def test_auth_shop_interface_letter_phone(playwright: Playwright, character:str) -> None:
    # Переход на страницу авторизации
    page.goto(interface_auth_url)
    # Ввод буквы или спецсимвола в поле для номера телефона
    page.locator("#current-field").click()
    try:
        page.locator("#current-field").fill(character)
        time.sleep(1)
        page.locator("#current-field").fill(character)
    except Exception as e:
        # Проверка, что поле осталось пустым
        expect(page.locator("#current-field")).to_be_empty()


# Тестирование максимальной длины поля ввода номера телефона
def test_auth_shop_interface_phone_len(playwright: Playwright) -> None:
    # Переход на страницу авторизации
    page.goto(interface_auth_url)
    page.locator("#current-field").click()
    page.locator("#current-field").fill("123213213213213213")
    # Получения введенного значения в поле
    phone_filed_content = page.locator("#current-field").input_value()
    # Удаление всех символов из полученного значения кроме цифр: (, ), " "
    phone_filed_content = "".join(c for c in phone_filed_content if c.isdecimal())
    # Проверка, длина введенного значения должна равняться 11 символам
    assert len(phone_filed_content) == 11


def run_shop_auth_test():
    test_auth_shop_interface_phone_len(playwright)
    test_auth_shop_interface_letter_phone(playwright, "y")
    test_auth_shop_interface_letter_phone(playwright, "!")
    test_auth_shop_interface_letter_phone(playwright, "ч")
    test_auth_shop_interface_letter_code(playwright, "j")
    test_auth_shop_interface_letter_code(playwright, "@")
    test_auth_shop_interface_letter_code(playwright, "д")
    test_auth_shop_interface_invalid_code(playwright)
    test_auth_shop_interface_partial_code(playwright)
    test_auth_shop_interface(playwright)


# Запуск сценария
if __name__ == '__main__':
    with sync_playwright() as playwright:
        # Запуск браузера - по умолчанию Google Chrome
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        # Запуск тестов
        run_shop_auth_test()