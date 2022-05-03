import random
import pytest_check as check
import pytest
from pages.labirint import *
from selenium.webdriver.common.keys import Keys


# Подготовка ресурса
@pytest.fixture(scope='session')
def create_page(start_browser):

    page = MainPage(pytest.driver)
    page.agree_cookie_button.click()

    yield page

    pass


# Подготовка обработки результатов поиска
@pytest.fixture(scope='session')
def search_page(create_page):

    page = create_page
    page.search.send_keys(SEARCH_WORDS[0][0])
    page.search_run_button.click()
    page.wait_page_loaded()
    page.search.send_keys('')

    yield page

    pass


def test_check_header_links(create_page):
    """ Проверка ссылок в меню хидера """

    page = create_page
    phm1 = page.header_menu1
    phm2 = page.header_menu2
    phm_txt = phm1.get_text() + phm2.get_text()
    print('')

    for item_id in range(0, phm1.count() + phm2.count()):
        lst_phm = list(page.header_menu1) + list(page.header_menu2)

        if not lst_phm[item_id].is_displayed() or phm_txt[item_id] == ' ':
            continue

        lst_phm[item_id].click()
        page.wait_page_loaded()

        chk = check.is_not_in(PAGE_NOT_FOUND, page.get_page_source(), phm_txt[item_id])
        print(phm_txt[item_id] + (' : PASSED' if chk else ' : FAILED'))


def test_check_footer_links(create_page):
    """ Проверка ссылок в меню футера """

    page = create_page
    pfi = page.footer_items
    pfi_txt = pfi.get_text()
    print('')

    for item_id in range(0, pfi.count()):
        lst_pfi = list(page.footer_items)
        lst_pfi[item_id].send_keys(Keys.ESCAPE)

        is_clickable = False
        while not is_clickable:
            try:
                lst_pfi[item_id].click()
                is_clickable = True
            except Exception:
                lst_pfi[item_id].send_keys(Keys.END)

        page.wait_page_loaded()
        chk = check.is_not_in(PAGE_NOT_FOUND, page.get_page_source(), pfi_txt[item_id])
        print(pfi_txt[item_id] + (' : PASSED' if chk else ' : FAILED'))


@pytest.mark.parametrize("words", SEARCH_WORDS)
def test_check_main_search(create_page, words):
    """ Проверка результатов поиска на наличие и релевантность """

    page = create_page
    page.search.send_keys(words[0])
    page.search_run_button.click()
    page.wait_page_loaded()
    page.search.send_keys('')

    assert page.products_card.count() > 0, 'Товар не найден'

    for txt in page.products_card.get_text():
        assert words[1] in txt.lower(), f'Неверный товар в результатах поиска "{txt}"'


@pytest.mark.parametrize("card_num", [i for i in range(0, COUNT_PROD_TEST)])
def test_check_prod_card(search_page, card_num):
    """ Случайная проверка товаров """

    page = search_page
    ptl = page.products_card_links
    att = ptl.get_attribute('title')
    hrf = ptl.get_attribute('href')
    ind = random.randint(0, ptl.count())
    ptl[ind].send_keys(Keys.DOWN)
    ptl[ind].click()
    page.wait_page_loaded()
    src = page.get_page_source()

    print(att[ind])
    print(page.get_current_url())
    assert src.find(PAGE_NOT_FOUND) == -1, f'Страница {page.get_current_url()} не найдена'
    assert src.find(att[ind]) != -1, f'Неверная карточка продукта "{hrf[ind]}"'

    page.go_back()


def test_check_slider_menu(search_page):
    """ Проверка меню разделов на соотвествие количеству результатов """

    page = search_page
    sgm = page.slider_menu
    sgm_txt = sgm.get_text()
    sgv_txt = page.slider_val.get_text()
    print('')

    # Обходим все элементы меню
    lst = list(sgm)
    for elem in lst:
        el_id = lst.index(elem)
        el_cnt = int(sgv_txt[el_id].replace(' ', ''))
        tab_id = elem.get_attribute('data-id_tab')
        elem.click()
        page.wait_page_loaded()

        el_pag_cnt = 0
        if el_cnt > COUNT_PROD_PAGE:
            # Если превышен максимум товаров на странице, определяем их количество по пагинатору
            pag = page.pagin_page_num
            pag[-1].send_keys(Keys.DOWN)
            pag_txt = pag.get_text()
            el_pag_cnt = (int(pag_txt[-1])-1) * COUNT_PROD_PAGE
            pag[-1].click()
            page.wait_page_loaded()

        # Определяем количество на последней странице
        if tab_id == '0':
            el_last_pag_cnt = page.products_card.count()
        else:
            el_last_pag_cnt = page.pagin_page_count.count()

        el_total_cnt = el_pag_cnt + el_last_pag_cnt
        chk = check.is_true(el_total_cnt in (el_cnt, COUNT_PROD_MAX), sgm_txt[el_id])
        print(sgm_txt[el_id] + (' : PASSED' if chk else ' : FAILED'))


def test_prod_filters(search_page):
    """ Проверка фильтрации товаров """

    page = search_page
    start_link = page.get_current_url()
    pft = page.filter_type
    print('')

    # Обходим фильтры
    for pft_id in range(0, pft.count()):
        pft[pft_id].click()
        ptm = page.filter_type_menu
        ptm_keys = page.filter_type_menu_keys.get_attribute('name')
        ptm_txt = ptm.get_text()

        # Обходим элементы фильтра
        for ptm_id in range(0, ptm.count()):
            pft[pft_id].click()
            ptm_lst = list(ptm)

            # Отключаем все фильтры кроме текущего
            for elem in ptm_lst:
                is_checked = elem.get_attribute('class').endswith('checked')
                if (ptm_lst[ptm_id] == elem and not is_checked) or (ptm_lst[ptm_id] != elem and is_checked):
                    elem.click()
                    page.wait_page_loaded()

            fmv = page.filter_menu_view
            is_disabled = fmv.get_attribute('class').endswith('disabled')
            if not is_disabled:
                fmv.click()
                page.wait_page_loaded()
                ppc = page.products_card
                dict_id = ptm_keys[ptm_id]
                page._attr_loc_filter = DICT_FILTER_MENU[dict_id]
                chk = check.equal(page.filtered_prod.count(), ppc.count(), ptm_txt[ptm_id])
                print(ptm_txt[ptm_id] + (' : PASSED' if chk else ' : FAILED'))
                page.get(start_link)


@pytest.mark.parametrize("price_type", ['min', 'max'])
def test_filter_price_values_negative(search_page, price_type):
    """ Проверка полей ввода цен на неверные значения """

    page = search_page
    pf = page.price_filter
    pf.click()

    ipm = None
    if price_type == 'min':
        ipm = page.price_min_input
    if price_type == 'max':
        ipm = page.price_max_input

    if ipm:
        str_1 = [chr(i) for i in range(32, 48)]  # Символы от ' ' до '/'
        str_2 = [chr(i) for i in range(58, 127)]  # Символы от ':' до '~'
        str_3 = [chr(i) for i in range(1040, 1104)]  # Символы от 'А' до 'я'
        ipm.send_keys(''.join(str_1 + str_2 + str_3))
        ipm.send_keys('00.0')
        ipm.send_keys('1000000')

        fmv = page.filter_menu_view
        is_disabled = fmv.get_attribute('class').endswith('disabled')
        if not is_disabled:
            fmv.click()
            page.wait_page_loaded()
            assert '100+000' in page.get_current_url()
        pf.click()
        ipm.send_keys('')


@pytest.mark.parametrize("price", FILTER_PRICE)
def test_filter_price_range(search_page, price):
    """ Проверка фильтрации товаров в ценовом диапазоне """

    page = search_page
    pf = page.price_filter
    pf.click()
    page.price_min_input.send_keys(str(price[0]))
    page.price_max_input.send_keys(str(price[1]))

    fmv = page.filter_menu_view
    is_disabled = fmv.get_attribute('class').endswith('disabled')
    if not is_disabled:
        fmv.click()
        page.wait_page_loaded()

        ppc = page.products_card
        ddp = list(map(lambda x: int(x), ppc.get_attribute('data-discount-price')))
        assert min(ddp) >= price[0] and max(ddp) <= price[1]


def test_prod_sort(search_page):
    """ Проверка сортировки товаров """

    page = search_page
    psm = page.sort_menu
    psm.click()
    smi = page.sort_menu_item
    smi_dec = smi.get_attribute('data-event-content')
    print('')

    # Обходим элементы сортировки
    for smi_id in range(0, smi.count()):
        smi[smi_id].click()
        page.wait_page_loaded()

        # Определяем наличие локатора элемента
        add_loc = DICT_SORT_MENU[smi_id][0]
        if add_loc:
            page._attr_loc_sort = loc_products_card + add_loc
            psp = page.sorted_prod

            # Обрабатываем данные для идентичной сортировки
            if psp.count() > 0:
                all_prods = psp.get_text()
                all_prods = list(map(lambda x: x.lower(), all_prods))
                if DICT_SORT_MENU[smi_id][1] == int:
                    all_prods = list(map(lambda x: x.replace('–', '-'), all_prods))
                    all_prods = list(map(lambda x: x.replace(' ', ''), all_prods))
                    all_prods = list(map(lambda x: x.replace('%', ''), all_prods))
                    all_prods = list(map(lambda x: int(x), all_prods))
                if DICT_SORT_MENU[smi_id][1] == str:
                    all_prods = list(map(lambda x: x.replace(',', ''), all_prods))
                    all_prods = list(map(lambda x: x.replace('.', ''), all_prods))
                    all_prods = list(map(lambda x: x.replace('"', ''), all_prods))

                rev = DICT_SORT_MENU[smi_id][2]
                chk = check.equal(all_prods, sorted(all_prods, reverse=rev), smi_dec[smi_id])
                print(smi_dec[smi_id] + (' : PASSED' if chk else ' : FAILED'))

        psm.click()
