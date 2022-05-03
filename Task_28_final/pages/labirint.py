import os
from tests.tests_config import *
from pages.base import WebPage
from pages.elements import *


class MainPage(WebPage):

    _attr_loc_filter = None
    _attr_loc_sort = None
    filtered_prod = None
    sorted_prod = None

    def __init__(self, web_driver, url=''):

        if not url:
            url = os.getenv("MAIN_URL") or HOST

        super().__init__(web_driver, url)

    # Метод обработки разных локаторов через атрибут
    def __setattr__(self, name, value):
        if name == '_attr_loc_filter':
            self.filtered_prod = ManyWebElements(xpath=value)
        if name == '_attr_loc_sort':
            self.sorted_prod = ManyWebElements(xpath=value)
        self.__dict__[name] = value

    # Кнопка принятия куки
    agree_cookie_button = WebElement(xpath=loc_agree_cookie_button)

    # Элементы меню в хидере и футере
    header_menu1 = ManyWebElements(xpath=loc_header_menu1)
    header_menu2 = ManyWebElements(xpath=loc_header_menu2)
    footer_items = ManyWebElements(xpath=loc_footer_items)

    # Поле ввода и кнопка поиска
    search = WebElement(xpath=loc_search)
    search_run_button = WebElement(xpath=loc_search_run_button)

    # Поиск всех товаров на странице
    products_card = ManyWebElements(xpath=loc_products_card)
    products_card_links = ManyWebElements(xpath=loc_products_card_links)

    # Меню разделов в результатах поиска
    slider_menu = ManyWebElements(xpath=loc_slider_menu)
    slider_val = ManyWebElements(xpath=loc_slider_val)

    # Пагинатор
    pagin_page_num = ManyWebElements(xpath=loc_pagin_page_num)
    pagin_page_count = ManyWebElements(xpath=loc_pagin_page_count)

    # Элементы фильтра
    filter_type = ManyWebElements(xpath=loc_filter_type)
    filter_type_menu = ManyWebElements(xpath=loc_filter_type_menu)
    filter_type_menu_keys = ManyWebElements(xpath=loc_filter_type_menu_keys)
    filter_menu_view = WebElement(xpath=loc_filter_menu_view)

    # Фильтр по цене
    price_filter = WebElement(xpath=loc_price_filter)
    price_min_input = WebElement(xpath=loc_price_min_input)
    price_max_input = WebElement(xpath=loc_price_max_input)

    # Элементы сортировки
    sort_menu = WebElement(xpath=loc_sort_menu)
    sort_menu_item = ManyWebElements(xpath=loc_sort_menu_item)
