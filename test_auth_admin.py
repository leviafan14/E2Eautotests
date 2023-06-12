import time
from playwright.sync_api import Page, expect
from playwright.sync_api import Playwright, sync_playwright

# Ссылка на страницу авторизации
interface_auth_url = "https://dev.admin.domka.shop/login"
# Тестовый валидный логин
test_login = "71111111111"
# Тестовый валидный пароль
test_password = "1111"


# Тестирование авторизации с вводом валидного номере телефона и валидного пароля
def test_auth_admin_interface(playwright: Playwright) -> None:
    # Переходим на страницу авторизации
    page.goto(interface_auth_url)
    # Вводим номер телефона
    page.locator("[placeholder=\"Телефон\"]").fill(test_login)
    # Вводим пароль
    page.locator("[placeholder=\"Пароль\"]").fill(test_password)
    # Проверкка, что открылся интерфейс администратора после клика по кнопке Войти
    with page.expect_navigation(url="https://dev.admin.domka.shop/"):
        page.locator("text=Войти").click()


# Тестирование авторизации с вводом НЕвалидного номера телефона и валидного пароля
def test_auth_admin_interface_invalid_phone(playwright: Playwright) -> None:
    # Переходим на страницу авторизации
    page.goto(interface_auth_url)
    # Вводим НЕвалидный номер телефона
    page.locator("[placeholder=\"Телефон\"]").fill("71111111112")
    # Вводим пароль
    page.locator("[placeholder=\"Пароль\"]").fill(test_password)
    # Нажатие на кнопку Войти
    page.locator("text=Войти").click()
    time.sleep(1)
    # Проверкка сообщения об ошибке
    expect(page.locator(".text-left")).to_have_text("* Пользователь не найден")


# Тестирование авторизации с вводом валидного номера телефона и НЕвалидного пароля
def test_auth_admin_interface_invalid_password(playwright: Playwright) -> None:
    # Переходим на страницу авторизации
    page.goto(interface_auth_url)
    # Вводим НЕвалидный номер телефона
    page.locator("[placeholder=\"Телефон\"]").fill(test_login)
    # Вводим пароль
    page.locator("[placeholder=\"Пароль\"]").fill("1112")
    # Нажатие на кнопку Войти
    page.locator("text=Войти").click()
    time.sleep(1)
    # Проверкка сообщения об ошибке
    expect(page.locator(".text-left")).to_have_text("* Неверный пароль")


# Тестирование авторизации с НЕзаполненным номером телефона и валидным паролем
def test_auth_admin_interface_empty_phone(playwright: Playwright) -> None:
    # Переходим на страницу авторизации
    page.goto(interface_auth_url)
    # Оставляем номер телефона пустым
    page.locator("[placeholder=\"Телефон\"]").fill("")
    # Вводим пароль
    page.locator("[placeholder=\"Пароль\"]").fill(test_password)
    # Нажатие на кнопку Войти
    page.locator("text=Войти").click()
    # Задержка 1 сек. для того чтобы сообщение об ошибке появилось раньше, чем отработает скрипт
    time.sleep(1)
    # Проверкка сообщения об ошибке
    expect(page.locator(".text-left")).to_have_text("* Телефон обязателен к заполнению")


# Тестирование авторизации с валидным номером телефона и НЕзаполненым паролем
def test_auth_admin_interface_empty_password(playwright: Playwright) -> None:
    # Переходим на страницу авторизации
    page.goto(interface_auth_url)
    # Вводим валидный номер телефона
    page.locator("[placeholder=\"Телефон\"]").fill(test_login)
    # Оставляем пароль пустым
    page.locator("[placeholder=\"Пароль\"]").fill("")
    # Нажатие на кнопку Войти
    page.locator("text=Войти").click()
    # Задержка 1 сек. для того чтобы сообщение об ошибке появилось раньше, чем отработает скрипт
    time.sleep(1)
    # Проверкка сообщения об ошибке
    expect(page.locator(".text-left")).to_have_text("* Пароль обязателен к заполнению")


# Тестирование авторизации с НЕзаполненным  номером телефона и НЕзаполненым паролем
def test_auth_admin_interface_empty_password_phone(playwright: Playwright) -> None:
    # Переходим на страницу авторизации
    page.goto(interface_auth_url)
    # Оставляем номер телефона пустым
    page.locator("[placeholder=\"Телефон\"]").fill("")
    # Оставляем пароль пустым
    page.locator("[placeholder=\"Пароль\"]").fill("")
    # Нажатие на кнопку Войти
    page.locator("text=Войти").click()
    # Задержка 1 сек. для того чтобы сообщение об ошибке появилось раньше, чем отработает скрипт
    time.sleep(1)
    # Проверкка сообщений об ошибках
    expect(page.locator(".text-left").nth(0)).to_have_text("* Телефон обязателен к заполнению")
    expect(page.locator(".text-left").nth(1)).to_have_text("* Пароль обязателен к заполнению")


# Тестирование авторизации с вводом НЕвалидного номера телефона состоящего из букв или спец. символов
def test_auth_admin_interface_letter_phone(playwright: Playwright, character:str) -> None:
    # Переход на страницу авторизации
    page.goto(interface_auth_url)
    # Ввод буквы или спецсимвола в поле для номера телефона
    page.locator("[placeholder=\"Телефон\"]").fill(character)
    # Проверка, что символ не удалось ввести в поле
    expect(page.locator("[placeholder=\"Телефон\"]")).not_to_have_text(character)


# Тестирование максимальной длины поля ввода номера телефона
def test_auth_admin_interface_phone_len(playwright: Playwright) -> None:
    # Переход на страницу авторизации
    page.goto(interface_auth_url)
    page.locator("[placeholder=\"Телефон\"]").click()
    page.locator("[placeholder=\"Телефон\"]").fill("123213213213213213")
    # Получения введенного значения в поле
    phone_filed_content = page.locator("[placeholder=\"Телефон\"]").input_value()
    # Удаление всех символов из полученного значения кроме цифр: (, ), " "
    phone_filed_content = "".join(c for c in phone_filed_content if c.isdecimal())
    # Проверка, длина введенного значения должна равняться 11 символам
    assert len(phone_filed_content) == 11


def run_admin_auth_test():
    test_auth_admin_interface_letter_phone(playwright, "j")
    test_auth_admin_interface_letter_phone(playwright, "ю")
    test_auth_admin_interface_letter_phone(playwright, "%")
    test_auth_admin_interface_phone_len(playwright)
    test_auth_admin_interface_empty_password_phone(playwright)
    test_auth_admin_interface_empty_password(playwright)
    test_auth_admin_interface_empty_phone(playwright)
    test_auth_admin_interface_invalid_phone(playwright)
    test_auth_admin_interface_invalid_password(playwright)
    test_auth_admin_interface(playwright)


if __name__ == '__main__':
    with sync_playwright() as playwright:
        # Запускаем браузер
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        # Запуск тестов
        run_admin_auth_test()


