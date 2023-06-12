import time
from playwright.sync_api import Page, expect
from playwright.sync_api import Playwright, sync_playwright
from test_auth_shop import confirm_code_page, test_login, interface_auth_url
from project_locators import *

# Счетчик товаров в корзине
products_count = 0
# Список добавляемых товаров в корзину
product_names = ["Товар_Domka#1"]


# Авторизация в магазине
def auth_in_shop(playwright: Playwright, page:Page) -> None:
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


# Тестирование подтверждения адреса - функционал активируется сразу после авторизации
def test_confirm_address(playwright: Playwright, page:Page) -> None:
    # Нажатие на кнопку "Подтвердить" на странице выбора адреса
    page.locator("text=Подтвердить").click()
    page.wait_for_url("https://dev.domka.shop/address/confirm?edit=1")
    time.sleep(1)
    # Подтверждение выбранного адреса
    page.locator("text=Подтвердить").click()
    page.wait_for_url("https://dev.domka.shop/profile/addresses")
    time.sleep(1)
    # Переход в профиль
    page.locator("text=Профиль").click()
    page.wait_for_url("https://dev.domka.shop/profile")
    time.sleep(1)
    # Переход на главную страницу магазина
    page.locator(".bottom-menu__item > img").first.click()
    # Проверка, что открылась главная страница магазина
    page.wait_for_url("https://dev.domka.shop/home")


# Тестирование перехода в категорию товаров домки
def test_goto_category_products(playwright: Playwright, category_name: str, page:Page) -> None:
    # Получение типов партнеров: Домка, Магазины, Рестораны
    partner_types = page.locator(".main__top-buttons")
    # Переход в категории товаров домки
    partner_types.locator("a").nth(0).click()
    # Проверка, что открылась страница с списком категорий товаров домки
    page.wait_for_url("https://dev.domka.shop/categories/delivery")
    # Переход в искомую категорию товаров
    page.locator(".categories__item", has_text=category_name).click()
    # Проверка, что открылась страница с товарами домки
    page.wait_for_url("https://dev.domka.shop/categories/1")
    time.sleep(2)


# Тест добавления товара в корзину нажатием на кнопку в превью категории
def test_add_in_cart(playwright: Playwright, product_names: list, page:Page) -> dict:
    global products_count
    # Словарь с добавленными в корзину продуктами
    added_product_dict = {}
    # Список аттрибутов добавленного товара
    product_attributes = []
    time.sleep(8)
    for product_name in product_names:
        product_attributes.clear()
        # Поиск нужного товара для добавления в корзину
        product_card = page.locator(".product-card", has_text=product_name)
        # Получение стоимости товара
        product_price_card = product_card.locator(".product-card__price")
        product_price = product_price_card.locator(".product-card__price_current").text_content().strip()
        # Получение веса добавляемого в корзину товара
        product_weight = product_card.locator(product_card_weight_ltr).text_content().strip()
        # Добавление товара в корзину
        product_card.locator(".form__button--outline.product-card__button").hover()
        product_card.locator(".form__button--outline.product-card__button").click()
        #time.sleep(3)
        #product_card.locator(".form__button--outline.product-card__button").click()
        # Получение количества добавленного товара
        product_added_count = product_card.locator(counter_sum_ltr).input_value()
        # Добавление в список цены добавленного товара
        product_attributes.append(product_price)
        # Добавление в список количества добавленного в корзину товара
        product_attributes.append(product_added_count)
        # Добавление в список веса добавленного товара
        product_attributes.append(product_weight)
        # Присвоение ключу (название товара) в качестве значения список с атрибутами товара
        added_product_dict[product_name] = product_attributes
        print(added_product_dict)
        # Проверка, товар добавлен в корзину в количестве равном 1 шт. Проверка осуществляется в элементе input
        expect(product_card.locator(counter_sum_ltr)).to_have_value("1")
        # Увеличиваем счетчкик товаров в корзине
        products_count += 1
    return added_product_dict


# Тест возвраащения в категории домки нажатием на хлебные крошки
def test_back_to_categories(playwright: Playwright, page:Page) -> None:
    # Получение локатора блоков в которых находится ссылка
    bread_crumbs = page.locator(".breadcrumbs")
    bread_crumbs_item = bread_crumbs.locator(".breadcrumbs__item")
    # Нажатие по ссылке
    bread_crumbs_item.locator("a", has_text = "Категории товаров").click()
    # Проверка, что после нажатия на ссылку открылась категория с товарами домки
    page.wait_for_url("https://dev.domka.shop/categories/delivery")


# Тестирование перехода в корзину с добавленными товарами
def test_go_to_basket(playwright:Playwright, page:Page) -> None:
    # Получение локатора нижнего меню
    bottom_menu = page.locator(".bottom-menu")
    # Нажатие на кнопку перехода в корзину
    bottom_menu.locator("a").nth(2).click()
    # Проверка, что открылась корзина
    page.wait_for_url("https://dev.domka.shop/basket")
    time.sleep(1)
    # Получение элемента содержащего стрелку разворачивающую список товаров в корзине
    partner_section_header = page.locator(".basket-section__header")
    # Разворачивание списка товаров в корзине
    partner_section_header.locator(".svg-inline--fa.fa-angle-up.closed").click()
    time.sleep(1)
    # Проверка, что в корзине находится добавленное количество товара
    expect(page.locator(".basket__item")).to_have_count(products_count)
    time.sleep(2)


# Проверка, что цена товары полученная с превью товара в категории равна стоимости товара отображаемой в корзине
def test_assert_product_prices(playwright: Playwright, product_dict: dict, page: Page) -> None:
    # Получение количества позиций товаров в корзине
    basket_items = page.locator(".basket__item__content").count()
    # Перебор добавленных в корзину товаров
    for n in product_dict.keys():
        # Перебор добавленных в корзину товаров
        for i in range(basket_items):
            # Полчение ячейки добавленного товара
            basket_item_content = page.locator(".basket__item", has_text=n)
            # Получение цены товара из ячейки товара за 1 единицу
            basket_price = basket_item_content.locator("p").first.text_content().strip()
            # Получение стоимости добавленного товара из футера карточки в корзине
            basket_item_footer_price = basket_item_content.locator(".basket__item__footer__calc").text_content().split()[4].split(".")[0]
            # Получение количества товара из футера карточки в корзине
            basket_item_footer_count = basket_item_content.locator(".basket__item__footer__calc").text_content().split()[2]
            # Вычисление стоимости товара с учетом его количества в корзине
            basket_footer_price = int(basket_price.split("₽")[0]) * int(basket_item_footer_count)
            # Проверка, что цена товара полученная с превью товара в категории равна стоимости товара
            # отображаемой в корзине
            assert basket_price == product_dict[n][0], f"prices product {product_dict[n]} is not equal. " \
                                                 f"Preview: {product_dict[n][0]} basket: {basket_price}"
            # Проверка соответствие цены товара с учетом его количества в корзине
            assert int(basket_footer_price) == int(basket_item_footer_price), f"price product in .basket__item__footer__calc is not" \
                                                                  f" equal in product {n}"


# Тестирование, что вес отображается в корзине и равен весу указанному в превью товара
def test_product_weight(playwright: Playwright, product_dict:dict, page:Page):
    # Получение количества позиций товаров в корзине
    basket_items = page.locator(".basket__item__content").count()
    # Перебор добавленных в корзину товаров
    for n in product_dict.keys():
        # Перебор добавленных в корзину товаров
        for i in range(basket_items):
            # Полчение ячейки добавленного товара
            basket_item_content = page.locator(".basket__item", has_text=n)
            # Получение веса товара из ячейки товара
            basket_weight = basket_item_content.locator(".basket__item__content__description__extra:has(p)").text_content().strip()
            print(f"basket_weight: {basket_weight}")
            # Тестирование, что вес отображается в корзине и равен весу указанному в превью товара
            assert basket_weight == product_dict[n][2], f"weight product {product_dict[n]} is not equal. " \
                                                       f"Preview: {product_dict[n][2]} basket: {basket_weight}" \
                                                        f" in product {n}"


# Тестирование соответствия количества добавленного товара в превью товара количествую товара в корзине
def test_product_count(playwright: Playwright, product_dict: dict, page: Page):
    # Получение количества позиций товаров в корзине
    basket_items = page.locator(".basket__item__content").count()
    # Получение общего количества товаров партнера в корзине
    product_count = page.locator(basket_section_total_ltr).locator(".basket-section__total__row"). \
        nth(0).text_content().split()[0]
    # Перебор добавленных в корзину товаров
    for n in product_dict.keys():
        # Перебор добавленных в корзину товаров
        for i in range(basket_items):
            # Полчение ячейки добавленного товара
            basket_item_content = page.locator(basket__item_ltr, has_text=n)
            # Получение локатора инпута количества добавленного товара в корзину
            input_product_count = basket_item_content.locator(counter_sum_ltr)
            # Получение количества товара из футера карточки в корзине
            basket_item_footer = basket_item_content.locator(".basket__item__footer__calc").text_content().split()[2]
            # Тестирование соответствия количества добавленного товара с превью товара с количеством в инпуте в корзине
            expect(input_product_count).to_have_value(product_dict[n][1])
            # Тестирование соответствия количества добавленного товара в футере карточки
            assert basket_item_footer == product_dict[n][1], f"Count product {n} in .basket__item__footer__calc " \
                                                             f"is not equal"


# Функция для запуска тестов
def run_tests() -> None:
    auth_in_shop(Playwright, page)
    test_confirm_address(Playwright, page)
    test_goto_category_products(Playwright, "Бакалея и крупы", page)
    product_data = test_add_in_cart(Playwright, product_names, page)
    test_back_to_categories(Playwright, page)
    test_go_to_basket(Playwright, page)
    test_assert_product_prices(Playwright, product_data)


# Запуск тестов
if __name__ == '__main__':
    with sync_playwright() as playwright:
        # Запуск браузера - по умолчанию Google Chrome
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        # Запуск тестов
        run_tests()