from functions_from_test_add_in_cart import *


@pytest.fixture
def page(playwright: Playwright):
    # Открытие окна бразуера
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    # Если нужна авторизация в магазине
    if auth_state == "yes":
        auth_in_shop(page)
    else:
        pass
    return page


# Добавление товаров в корзину
def test_add_prdoucts(page) -> None:
    flush_cart(page)
    # Открытие списка партнеров
    page.goto(category_url)
    # Открытие страницы партнера
    page.locator(".css-qbyb0p").nth(6).click()
    # Добавление указанного количества товаров в корзину
    for i in range(13):
        try:
            page.get_by_role("button", name="В КОРЗИНУ").nth(i).click()
            print(f"Итерация {i} товар добавлен")
        except Exception as e:
            print(f" Не удалось добавить товар в корзину, на итерации {i} \n {e}")
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