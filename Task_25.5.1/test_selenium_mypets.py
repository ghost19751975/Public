import pytest
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from settings import valid_email, valid_password


@pytest.fixture(autouse=True)
def test_login():
    s = Service('D:/Документы/SkillFactory/PyCharm/geckodriver.exe')
    pytest.driver = webdriver.Firefox(service=s)
    # Устанавливаем неявное ожидание
    pytest.driver.implicitly_wait(10)
    # Переходим на страницу авторизации
    pytest.driver.get('http://petfriends1.herokuapp.com/login')
    # Вводим email
    pytest.driver.find_element(By.ID, 'email').send_keys(valid_email)
    # Вводим пароль
    pytest.driver.find_element(By.ID, 'pass').send_keys(valid_password)
    # Нажимаем на кнопку входа в аккаунт
    pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

    yield

    pytest.driver.quit()


def test_my_pets():
    # Явно ожидаем элемент "Мои питомцы"
    menu_my_pets = WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href*="my_pets"]'))
    )
    menu_my_pets.click()
    # Неявно ожидаем карточки питомцев
    pytest.driver.find_element(By.XPATH, './/tbody/tr/th/img')  # Фото
    pytest.driver.find_elements(By.XPATH, './/tbody/tr/td')  # Имя, порода, возраст
    # Явно ожидаем элемент статистики
    element = WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_element_located((By.XPATH, ".//div[@class='.col-sm-4 left']"))
    )
    # Определяем количество питомцев
    cnt_stat = int(element.text.split(': ')[1].split('\n')[0])
    cnt_with_photo = len(pytest.driver.find_elements(By.XPATH, './/tbody/tr/th/img[@src!=""]'))
    lst_pets = pytest.driver.find_elements(By.XPATH, './/tbody/tr')

    # Заполняем массивы по каждому полю
    pets_name = []
    pets_breed = []
    pets_age = []
    pets_nba = []  # name + breed + age
    for item in lst_pets:
        fields_pet = item.find_elements(By.XPATH, './/td')
        pets_name.append(fields_pet[0].text)
        pets_breed.append(fields_pet[1].text)
        pets_age.append(fields_pet[2].text)
        pets_nba.append(' '.join([fields_pet[0].text, fields_pet[1].text, fields_pet[2].text]))

    # Присутствуют все питомцы
    assert cnt_stat == len(lst_pets)
    # Хотя бы у половины питомцев есть фото
    assert cnt_stat / cnt_with_photo <= 2
    # У всех питомцев есть имя, возраст и порода
    assert "" not in pets_name
    assert "" not in pets_breed
    assert "" not in pets_age
    # У всех питомцев разные имена
    assert len(set(pets_name)) == cnt_stat
    # В списке нет повторяющихся питомцев
    assert len(set(pets_nba)) == cnt_stat
