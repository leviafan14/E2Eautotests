from functions_from_test_add_in_cart import *


#@pytest.fixture
def page(playwright: Playwright):
    # Открытие окна бразуера
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    # Если нужна авторизация в магазине
    if auth_state == "yes":
        auth_in_shop(page)
    else:
        pass
    return page


# Добавление товаров в корзину
def test_add_prdoucts(playwright: Playwright) -> None:
    # Открытие окна бразуера
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    # Если нужна авторизация в магазине
    if auth_state == "yes":
        auth_in_shop(page)
    else:
        pass
    flush_cart(page)
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    # Открытие списка партнеров
    page.goto(category_url)
    # Открытие страницы партнера
    page.locator(".css-qbyb0p").nth(3).click()
    # Добавление указанного количества товаров в корзину
    for i in range(5):
        try:
            page.get_by_role("button", name="В КОРЗИНУ").nth(i).click()
        except Exception as e:
            print(f" Не удалось добавить товар в корзину, на итерации {i} \n {e}")
            page.get_by_role("link", name="Корзина").first.click()
    # Переход в корзину
    page.get_by_role("link", name="Корзина").first.click()
    time.sleep(3)
    count_added_product = page.get_by_role("button", name="Удалить").count()
    print(f"\nКоличество добавленных в корзину товаров {count_added_product}")
    try:
        page.get_by_text("Очистить корзину").click()
    except Exception as e:
        context.tracing.stop(path="context_trace.zip")
        print("\nКорзина пуста")
    # Получение количества добавленных в корзину товаров

    time.sleep(2)
    assert count_added_product >= 1, "\nТовары в корзину не добавлены"
    page.close()