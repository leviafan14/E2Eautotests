import time
from playwright.sync_api import Page, expect
from playwright.sync_api import Playwright, sync_playwright

# Ссылка на страницу авторизации
interface_auth_url = "https://dev.courier.domka.shop/login"
# Тестовый валидный логин товароведа
test_login = "79994577766"
# Тестовый валидный пароль товароведа
test_password = "adsadsads"
# Тестовый логин курьера
test_courier_login = "71111111123"
test_courier_password = "1111"
input_auth_element = ".w-100.form-control.material-shadow.box-sizing-bb"


# Тестирование авторизации с вводом валидного номере телефона и валидного пароля
def test_auth_courier_interface(playwright: Playwright) -> None:
    # Переходим на страницу авторизации
    page.goto(interface_auth_url)
    # Вводим номер телефона
    page.locator(input_auth_element).nth(0).fill(test_login)
    # Вводим пароль
    page.locator(input_auth_element).nth(1).fill(test_password)
    # Проверкка, что открылся интерфейс администратора после клика по кнопке Войти
    with page.expect_navigation(url="https://dev.courier.domka.shop/orders"):
        page.locator("text=Войти").click()


# Тестирование авторизации с вводом НЕвалидного номера телефона и валидного пароля
def test_auth_partner_interface_invalid_phone(playwright: Playwright) -> None:
    # Переходим на страницу авторизации
    page.goto(interface_auth_url)
    # Вводим НЕвалидный номер телефона
    page.locator(input_auth_element).nth(0).fill("71111111110")
    # Вводим пароль
    page.locator(input_auth_element).nth(1).fill(test_password)
    # Нажатие на кнопку Войти
    page.locator("text=Войти").click()
    time.sleep(1)
    # Проверкка сообщения об ошибке
    expect(page.locator(".alert.show:has(p)")).to_have_text("Пользователь не найден")


# Тестирование авторизации с вводом валидного номера телефона и НЕвалидного пароля
def test_auth_partner_interface_invalid_password(playwright: Playwright) -> None:
    # Переходим на страницу авторизации
    page.goto(interface_auth_url)
    # Вводим НЕвалидный номер телефона
    page.locator(input_auth_element).nth(0).fill(test_login)
    # Вводим пароль
    page.locator(input_auth_element).nth(1).fill("invalid_password")
    # Нажатие на кнопку Войти
    page.locator("text=Войти").click()
    time.sleep(1)
    # Проверкка сообщения об ошибке
    expect(page.locator(".alert.show:has(p)")).to_have_text("Неверный пароль")


# Тестирование авторизации с НЕзаполненным номером телефона и валидным паролем
def test_auth_partner_interface_empty_phone(playwright: Playwright) -> None:
    # Переходим на страницу авторизации
    page.goto(interface_auth_url)
    # Оставляем номер телефона пустым
    page.locator(input_auth_element).nth(0).fill("")
    # Вводим пароль
    page.locator(input_auth_element).nth(1).fill(test_password)
    # Нажатие на кнопку Войти
    page.locator("text=Войти").click()
    # Задержка 1 сек. для того чтобы сообщение об ошибке появилось раньше, чем отработает скрипт
    time.sleep(1)
    # Проверкка сообщения об ошибке
    expect(page.locator(".alert.show:has(p)")).to_have_text("Телефон - обязательное поле")


# Тестирование авторизации с валидным номером телефона и НЕзаполненым паролем
def test_auth_partner_interface_empty_password(playwright: Playwright) -> None:
    # Переходим на страницу авторизации
    page.goto(interface_auth_url)
    # Вводим валидный номер телефона
    page.locator(input_auth_element).nth(0).fill(test_login)
    # Оставляем пароль пустым
    page.locator(input_auth_element).nth(1).fill("")
    # Нажатие на кнопку Войти
    page.locator("text=Войти").click()
    # Задержка 1 сек. для того чтобы сообщение об ошибке появилось раньше, чем отработает скрипт
    time.sleep(1)
    # Проверкка сообщения об ошибке
    expect(page.locator(".alert.show:has(p)")).to_have_text("Пароль - обязательное поле")


# Тестирование авторизации с НЕзаполненным  номером телефона и НЕзаполненым паролем
def test_auth_partner_interface_empty_password_phone(playwright: Playwright) -> None:
    # Переходим на страницу авторизации
    page.goto(interface_auth_url)
    # Оставляем номер телефона пустым
    page.locator(input_auth_element).nth(0).fill("")
    # Оставляем пароль пустым
    page.locator(input_auth_element).nth(1).fill("")
    # Нажатие на кнопку Войти
    page.locator("text=Войти").click()
    # Задержка 1 сек. для того чтобы сообщение об ошибке появилось раньше, чем отработает скрипт
    time.sleep(1)
    # Проверкка сообщений об ошибках
    expect(page.locator(".alert.show:has(p)")).to_have_text("Телефон - обязательное поле Пароль - обязательное поле")


# Тестирование авторизации с вводом НЕвалидного номера телефона состоящего из букв или спец. символов
def test_auth_courier_interface_letter_phone(playwright: Playwright, character:str) -> None:
    # Переход на страницу авторизации
    page.goto(interface_auth_url)
    # Ввод буквы или спецсимвола в поле для номера телефона
    page.locator(input_auth_element).nth(0).fill(character)
    # Проверка, что символ не удалось ввести в поле
    expect(page.locator(input_auth_element).nth(0)).not_to_have_text(character)


# Тестирование максимальной длины поля ввода номера телефона
def test_auth_courier_interface_phone_len(playwright: Playwright) -> None:
    # Переход на страницу авторизации
    page.goto(interface_auth_url)
    page.locator(input_auth_element).nth(0).click()
    page.locator(input_auth_element).nth(0).fill("123213213213213213")
    # Получения введенного значения в поле
    phone_filed_content = page.locator(input_auth_element).nth(0).input_value()
    # Удаление всех символов из полученного значения кроме цифр: (, ), " "
    phone_filed_content = "".join(c for c in phone_filed_content if c.isdecimal())
    # Проверка, длина введенного значения должна равняться 11 символам
    assert len(phone_filed_content) == 11


# Тестирование соответствия указанной пары логин/пароль на соответствие роли
def test_auth_role(playwright: Playwright, role: str, login, password) -> None:
    # Запуск теста и создание контекста для запуска теста
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    # Переходим на страницу авторизации
    page.goto(interface_auth_url)
    # Вводим номер телефона
    page.locator(input_auth_element).nth(0).fill(login)
    # Вводим пароль
    page.locator(input_auth_element).nth(1).fill(password)
    # Проверкка, что открылся интерфейс администратора после клика по кнопке Войти
    with page.expect_navigation(url="https://dev.courier.domka.shop/orders"):
        page.locator("text=Войти").click()

    # Проверка соответствия пары логин/пароль на соответствие роли
    if "courier" in role:
        expect(page.locator("#nav")).to_contain_text("Смены")
    elif "collector" in role:
        expect(page.locator("#nav")).not_to_contain_text("Смены")
    else:
        return "Error invalid worker role"
    browser.close()



def run_courier_auth_test():
    test_auth_role(playwright, "courier", test_courier_login, test_courier_password)
    test_auth_courier_interface_letter_phone(playwright, "g")
    test_auth_courier_interface_letter_phone(playwright, "г")
    test_auth_courier_interface_letter_phone(playwright, ",")
    test_auth_courier_interface_phone_len(playwright)
    test_auth_partner_interface_empty_password_phone(playwright)
    test_auth_partner_interface_empty_password(playwright)
    test_auth_partner_interface_empty_phone(playwright)
    test_auth_partner_interface_invalid_phone(playwright)
    test_auth_partner_interface_invalid_password(playwright)
    test_auth_courier_interface(playwright)
    test_auth_role(playwright, "collector", test_login, test_password)


if __name__ == '__main__':
    with sync_playwright() as playwright:
        # Запускаем браузер
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        # Запуск тестов
        run_courier_auth_test()