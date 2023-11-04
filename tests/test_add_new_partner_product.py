import time
import pytest
from playwright.sync_api import Page, expect
from playwright.sync_api import Playwright, sync_playwright
from auth_data import link_to_partner_interface, partner_login, partner_password
from data_for_testing import *


# Функция для ввода информации на складах: Остатки, базовая цена, цена по акции
def input_stock_info(locator: object, param: str, step: int) -> None:
    # locator - множество всех полей для ввода какого либо параметра: Остатки и т.д.
    for l in locator:
        # l - заполняемое в текущей итерации поле
        l.click()
        # param - заполняемый параметр: Остатки и т.д.
        l.fill(str(param))
        # step - шаг заполнения - необходимо для получения различных значений в каждом поле
        param += step


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
    return page


# Нажатие на иконку "Товары" открывает раздел "Товары"
def test_goto_products_page(auth_in_interface) -> None:
    with auth_in_interface.expect_navigation(url="https://dev.partner.domka.shop/products"):
        auth_in_interface.locator(".fas.fa-shopping-cart").click()


# Открытие интерфейса создания товара
def test_open_interface_create_product(auth_in_interface) -> None:
    page = auth_in_interface
    # Тест открытия интерфейса создания товара
    with auth_in_interface.expect_navigation(url="https://dev.partner.domka.shop/products/add"):
        time.sleep(1)
        page.get_by_role("button", name="Добавить").click()


# Создание штучного товара с ед. измерения "Объем", срок хранения сутки, заполненными с полями:
# Название, Категория, Описание, Состав, Безлимит,
# Общая базовая цена, Информация на складах,
def test_add_new_product_requarement_fields(auth_in_interface):
    page = auth_in_interface

    # Ввод названия товара с добавлением полученной временной метки
    page.get_by_placeholder("Название").fill(product_names)

    # Раскрытие списка с категориями товара
    category_change = page.get_by_placeholder("Категория")
    category_change.click()
    time.sleep(1)
    category_change.clear()
    category_change.click()
    time.sleep(1)


    # Выбор категории из списка - назначение корневой категории
    # (самая верхняя категория в списке)
    category_list = page.locator("ul.p-0.m-0")
    category_list.locator("li").nth(0).click()
    #page.get_by_text("Алкоплюс").click() # Назначение категории по её названию

    # Ввод описания товара
    page.get_by_placeholder("Описание").first.fill(product_description)

    # Проверка, что поле для ввода состава товара существует
    expect(page.get_by_placeholder("Состав")).to_be_enabled()
    # Сохранение локатора для ввода состава
    compound = page.get_by_placeholder("Состав")
    # Ввод состава заказа
    compound.first.fill(product_compound)

    # Проверка, что поле НДС существует
    expect(page.get_by_placeholder("НДС")).to_be_enabled()
    # Получение локатора для ввода НДС
    nds_product = page.get_by_placeholder("НДС")
    # Ввод НДС из импортированной переменной
    nds_product.click()
    nds_product.fill(nds_percent)

    # Включение безлимитного режима товара
    page.locator(".checkbox-ios-switch.ml-4").click()

    # Закрытие окна уведомляющего о включении безлимитного режима товара
    page.locator("#myModal").locator(".close.color-black").click()

    # Ввод общей базовой цены товара
    page.get_by_placeholder("Цена").first.click()
    page.get_by_placeholder("Цена").first.fill(product_base_price)

    # Проверка, что поле для ввода общей цены по акции существует
    expect(page.get_by_placeholder("Цена по акции").first).to_be_enabled()
    # Сохранение в переменную локатора для воода общей цны по акции
    base_discount_price = page.get_by_placeholder("Цена по акции").first
    # Ввод общей цены по акции товара
    base_discount_price.click()
    base_discount_price.fill(product_base_discount_price)

    # Проверка, что поле для выбора единицы измерения "Вес" или "Объем" существует
    expect(page.locator("#__BVID__21")).to_be_enabled()
    # Выбор единицы измерения - в данном случае "Объем"
    page.locator("#__BVID__22").select_option(unit_volume)

    time.sleep(1)
    # Проверка, что локатор ввода объема существует
    expect(page.get_by_label("Обьем").nth(1)).to_be_enabled()
    page.get_by_label("Обьем").nth(1).fill(weight_value)

    # Проверка, что элемент для загрузки фото доступен
    expect(page.locator(".photo-upload__input")).to_be_enabled()
    # Путь к папке с фото товаров
    path_to_photo = "E:/My files/Attaches/Images/Изображения/"
    # Загрузка 5 фотографий в карточку товара
    page.locator(".photo-upload__input").set_input_files([f"{path_to_photo}burger.png", f"{path_to_photo}burger2.png",
                                                          f"{path_to_photo}udon1.jpg", f"{path_to_photo}udon2.jpg",
                                                         f"{path_to_photo}salat1.jpg"])
    # Получение превью всех загруженных фотографий
    photos_preview = page.locator(".preview").count()
    # Проверка, что загружено 5 фотографий - пол количеству превью.
    assert photos_preview == 5, f"Количество превью не соотвествует 5, получено превью {photos_preview}"

    # Ввод количества по складам
    # Получение всех полей для ввода количества
    stocks_quantity = page.get_by_placeholder("Кол-во").all()
    # Определение стартового количества
    # Вызов функции заполняющей поле - в данном случае остатки по складам
    input_stock_info(stocks_quantity, quantity, step_add_quantity)

    # Ввод базовых цен складов
    # Получение всех полей с базовыми ценами склада - без учета пагинации складов
    stocks_regular_price_locator = page.get_by_role("textbox", name="Цена", exact=True).all()
    # Определение стартового значения базовой цены на складах
    #stocks_base_price = 125
    # Вызов функции заполняющей поле - в данном случае базовые цены складов
    input_stock_info(stocks_regular_price_locator, stocks_base_price, step_add_base_price)

    # Ввод цен по акции на складах
    # Получение всех полей для ввода цен по акции
    stocks_discount_price_locator = page.get_by_role("textbox", name="Цена по акции", exact=True).all()
    # Определение стартового значения скидочной цены на складах
    # Вызов функции заполняющей поле - в данном случае скидочные цены на складах
    input_stock_info(stocks_discount_price_locator, stocks_discount_price, step_add_discount_price)

    # Проверка, что список для выбора ед. измерения срока годности доступен
    expect(page.locator("select[name=\"categories\"]")).to_be_enabled()
    # Проверка, что поле для ввода ед. измерения срока годности доступно
    expect(page.get_by_placeholder("Срок годности")).to_be_enabled()
    # Выбор "Дней" в качестве ед.изм. срока годности
    page.locator("select[name=\"categories\"]").select_option(shelf_life_option)
    # Вввод срока годности
    page.get_by_placeholder("Срок годности").fill(shelf_life)

    # Проверка, что поле для ввода Условий хранения доступно
    expect(page.get_by_label("Условия хранения")).to_be_enabled()
    # Ввод услових хранения
    page.get_by_label("Условия хранения").fill(storage_conditions)

    # Проверка, что поле для ввода Вида упаковки доступно
    expect(page.get_by_label("Вид упаковки")).to_be_enabled()
    # Ввод Вида упаковки
    page.get_by_label("Вид упаковки").fill(packaging)

    # Проверка, что поле для ввода Бренда доступно
    expect(page.get_by_label("Бренд")).to_be_enabled()
    # Ввод Бренда
    page.get_by_label("Бренд").fill(brand)

    # Проверка, что поле для ввода Производиеля доступно
    expect(page.get_by_label("Производитель")).to_be_enabled()
    # Ввод Производителя
    page.get_by_label("Производитель").fill(packaging)

    # Проверка, что поле для ввода Страны - Производителя доступно
    expect(page.get_by_placeholder("Страна производитель")).to_be_enabled()
    # Ввод первых букв Страны - производителя
    page.get_by_placeholder("Страна производитель").click()
    page.get_by_placeholder("Страна производитель").fill(manufacturer_country)
    page.get_by_placeholder("Страна производитель").click()
    # Выбор страницы производителя из сформировавшегося списка
    page.get_by_text("Российская Федерация").click()


    # Тест - после успешного создания товара открывается страница "Товары"
    with auth_in_interface.expect_navigation(url="https://dev.partner.domka.shop/products"):
        # Нажатие на кнопку добавления товара
        page.get_by_role("button", name="Добавить").click()
        # Закрытие модального окна информирующего об успешном создании товара
        page.locator("#myModal").get_by_text("×").click()

    time.sleep(2)