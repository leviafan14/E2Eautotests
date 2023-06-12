import time
import pytest
from playwright.sync_api import Page, expect
from playwright.sync_api import Playwright
from auth_data import link_to_partner_interface, partner_login, partner_password

# Ссылка на страницу товара для тестирования блокировок на складах
product_link = "https://dev.partner.domka.shop/products/edit/523539"
product_name = "Без категории2"

# Авторизация перед выполнением тестов
@pytest.fixture(scope="session")
def auth_in_interface(playwright: Playwright) -> Page:
    # Открытие окна бразуера
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    # Переход на страницу авторизации
    page.goto(link_to_partner_interface)
    # Ввод номера телефона
    page.locator("[placeholder=\"Телефон\"]").fill(partner_login)
    # Ввод пароля
    page.locator("[placeholder=\"Пароль\"]").fill(partner_password)
    # Нажатие на кнопку "Войти"
    page.locator("text=Войти").click()
    time.sleep(2)
    return page


# Блокировка товара на втором складе в списке
def test_block_on_one_stock(auth_in_interface) -> None:
    page = auth_in_interface
    # Открытие раздела Товары
    with page.expect_navigation(url="https://dev.partner.domka.shop/products"):
        page.locator(".bx-cart").click()
    # Открытие страницы товара для редактирования
    page.get_by_role("link", name=product_name, exact=True).click()
    time.sleep(2)
    # Блокировка товара на указанном складе, склад определяется по номеру в списке
    button_status = page.locator('.ban.position-relative.btn.text-body').nth(2)
    button_status.locator(".fas.fa-lock-open.in-stock").click()

    # Проверка, что иконка состояния блокировки изменилась на закрытый замочек
    expect(button_status.locator(".fas.fa-lock.in-stock")).to_be_enabled()
    time.sleep(2)

    # Сохранение изменений
    page.locator(".add_btn_partner.mt-0.ml-4").click()
    time.sleep(2)
    # Закрытие окна уведомляющего об изменении данных товара
    page.locator("#myModal").get_by_text("×").click()
    time.sleep(2)


# Иконка полной блокировки не изменилась в списке товаров - Замочек раскрыт.
def test_block_status_on_products_list(auth_in_interface) -> None:
    page = auth_in_interface
    # Получение строки с товаром
    row_products = page.locator(".v_table__body_row").filter(has_text=product_name)
    row_status_button = row_products.locator(".ban.position-relative.btn.text-body")
    time.sleep(2)

    # Проверка, что товар отображается разблокированным после блокировки на одном из складов
    expect(row_status_button.locator(".fas.fa-lock-open")).to_be_enabled()


# Проверка статуса блокировки товара на указанном в списке складе
def test_unblock_on_one_stock(auth_in_interface) -> None:
    page = auth_in_interface
    locator_stocks_block_buttons = ".ban.position-relative.btn.text-body"
    block_status_button = page.locator(".ban.position-relative.btn.text-body")
    page.get_by_role("link", name=product_name, exact=True).click()
    time.sleep(2)

    block_status_button.nth(0).focus()
    block_status_button.nth(0).hover()
    # Проверка, что товар не заблокирован полностью
    expect(block_status_button.nth(0).locator(".fas.fa-lock-open")).to_be_enabled()

    block_status_button.nth(1).focus()
    block_status_button.nth(1).hover()
    # Проверка, что товар заблокирован только на складе из предыдущего теста
    expect(block_status_button.nth(1).locator(".fas.fa-lock-open.in-stock")).to_be_enabled()

    block_status_button.nth(2).focus()
    block_status_button.nth(2).hover()
    # Проверка, что товар заблокирован на складе из предыдущего теста
    expect(block_status_button.nth(2).locator(".fas.fa-lock.in-stock")).to_be_enabled()

