HOST = 'https://www.labirint.ru/'
PAGE_NOT_FOUND = 'Ошибка 404'
COUNT_PROD_PAGE = 60
COUNT_PROD_MAX = 1000
COUNT_PROD_TEST = 3

loc_agree_cookie_button = '//button[@class="cookie-policy__button js-cookie-policy-agree"]'

loc_header_menu1 = '//div[@class="b-header-outer"]//a[contains(@class,"b-header-b-menu")]'
loc_header_menu2 = '//div[@class="b-header-outer"]//a[contains(@class,"b-header-b-sec")]'
loc_footer_items = '//a[contains(@class,"b-rfooter-e-item-link") and substring(@href,1,1) = "/" and ' \
                   'substring(@href,string-length(@href)) = "/"]'

loc_search = '//input[@class="b-header-b-search-e-input"]'
loc_search_run_button = '//button[@class="b-header-b-search-e-btn"]'

loc_products_class_0 = '//div[@class="card-column card-column_gutter col-xs-6 col-sm-3 col-md-1-5 col-xl-2"]'
loc_products_class_1 = '//div[contains(@class,"product need-watch")]'
loc_products_card = loc_products_class_0 + loc_products_class_1
loc_products_card_links = f'{loc_products_card}//a[@class="cover"]'

loc_slider_menu = '//a[@data-id_tab]'
loc_slider_val = '//span[@class="b-stab-e-slider-item-e-txt-m-small js-search-tab-count"]'

loc_pagin_page_num = '//div[@class="pagination-number__right"]//a[@class="pagination-number__text"]'
loc_pagin_page_count = '//span[@class="rubric-item-name"]'

loc_filter_class_0 = 'navisort-item__content'
loc_filter_class_1 = 'navisort-line-one swiper-slide swiper-slide-active'
loc_filter_class_2 = 'menu-open navisort-status-head l-spacing12 navisort-item'
loc_filter_point = f'//div[@class="{loc_filter_class_1}"]//span[contains(@class,"{loc_filter_class_2}")]'
loc_filter_menu = f'//span[@class="{loc_filter_class_2}"]'
loc_filter_type = loc_filter_point + f'//span[@class="{loc_filter_class_0}"]'
loc_filter_type_menu = loc_filter_menu[:-2] + ' active"]/..//label[contains(@class,"item-inner checkbox-ui")]'
loc_filter_type_menu_keys = loc_filter_menu[:-2] + ' active"]/..//label[contains(@class,"item-inner checkbox-ui")]//input'
loc_filter_menu_view = loc_filter_menu[:-2] + ' active"]/..//input[contains(@class, "w100p show-goods__button")]'
loc_filter_paperbooks = loc_products_class_0 + '//div[@data-dir="books"]'
loc_filter_ebooks = loc_products_card + '//span[@class="card-label card-label_profit card-label_color-ebooks"]'
loc_filter_otherbooks = loc_products_class_0 + '//div[@data-dir!="books"]'
loc_filter_available = loc_products_card + '//a[@class="btn buy-link btn-primary"]'
loc_filter_preorder = loc_products_card + '//a[@class="btn buy-link preorder-link"]'
loc_filter_wait = loc_products_card + '//a[@class="btn-not-avaliable"]'
loc_filter_no = loc_products_card + '//span[@class="price-val price-gray price-missing"]'
loc_filter_discount = loc_products_card + '//span[@class="price-old"]'
loc_filter_free_delivery = loc_products_card + '//span[@class="card-label__text" and contains(text(), "Доставка 0")]'

loc_price_filter = loc_filter_point + f'//span[@class="{loc_filter_class_0}" and contains(text(), "ЦЕНА")]'
loc_price_min_input = loc_filter_menu[:-2] + ' active"]/..//input[@class="text number" and @name="price_min"]'
loc_price_max_input = loc_filter_menu[:-2] + ' active"]/..//input[@class="text number" and @name="price_max"]'

loc_sort_menu = '//span[@class="sorting-value menu-open l-spacing12 navisort-item"]'
loc_sort_menu_item = loc_sort_menu[:-2] + ' active"]/..//a[contains(@class, "item-link item-inner")]'
loc_sort_menu_review = '//span[@class="product-hint"]//a[@data-event-label="reviewsCount"]/span'
loc_sort_menu_price = '//div[@class="product-cover"]//div[@class="price-label"]//span[@class="price-val"]/span'
loc_sort_menu_discount = '//div[@class="product-cover"]//div[@class="price-label"]' \
                         '//span[contains(@class, "card-label__text") and not(contains(@class, "inversed"))]'
loc_sort_menu_name = '//div[@class="product-cover"]//a[@class="product-title-link"]//span[@class="product-title"]'
loc_sort_menu_author = '//div[@class="product-author"]'

DICT_FILTER_MENU = {
    'paperbooks': loc_filter_paperbooks,  # Бумажные книги
    'ebooks': loc_filter_ebooks,  # Электронные книги
    'otherbooks': loc_filter_otherbooks,  # Другие товары
    'available': loc_filter_available,  # В наличии
    'preorder': loc_filter_preorder,  # Предзаказ
    'wait': loc_filter_wait,  # Ожидаются
    'no': loc_filter_no,  # Нет в продаже
    'discount': loc_filter_discount,  # Со скидкой
    'free_delivery': loc_filter_free_delivery,  # Курьером бесплатно
}

DICT_SORT_MENU = {
    # [локатор, тип данных, направление сортировки]
    0: [None, None, False],  # релевантные
    1: [None, None, False],  # новинки
    2: [None, None, False],  # лидеры продаж
    3: [loc_sort_menu_review, int, True],  # рецензируемые
    4: [loc_sort_menu_price, int, False],  # дешевые
    5: [loc_sort_menu_price, int, True],  # дорогие
    6: [loc_sort_menu_discount, int, False],  # с макс. скидкой
    7: [loc_sort_menu_name, str, False],  # по названию A
    8: [loc_sort_menu_name, str, True],  # по названию Я
    9: [loc_sort_menu_author, str, False],  # по автору A
    10: [loc_sort_menu_author, str, True],  # по автору Я
}

SEARCH_WORDS = [
    ['пушкин', 'пушкин'],
    ['штирлиц', 'штирлиц'],
    ['урфин', 'урфин'],
    ['geirby', 'пушкин'],
    ['inbhkbw', 'штирлиц'],
    ['ehaby', 'урфин'],
]

FILTER_PRICE = [
    [1, 100],
    [100, 1000],
    [1000, 10000],
]
