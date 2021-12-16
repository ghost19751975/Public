from api import PetFriends
from settings import valid_email, valid_password
import os

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем, что запрос api ключа возвращает статус 200 и в результате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем, что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этот ключ
    запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name='Барбоскин', animal_type='двортерьер',
                                     age='4', pet_photo='images/cat1.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Мурзик', animal_type='Котэ', age=5):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


# Еще 10 тестов по заданию 19.7.2

def test_add_new_pet_without_photo_with_valid_data(name='Барбоскин', animal_type='двортерьер', age='4'):  # 1
    """Проверяем, что можно добавить питомца без фото с корректными данными"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == name


def test_add_photo_of_pet_with_valid_data(pet_photo='images/cat1.jpg'):  # 2
    """Проверяем, что можно добавить фото питомца с корректными данными"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.add_photo_of_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)

        assert status == 200
        assert result['id'] == my_pets['pets'][0]['id']
    else:
        raise Exception("There is no my pets")


def test_get_api_key_for_invalid_email(email='invalid_email', password=valid_password):  # 3
    """ Проверяем, что запрос api ключа с неверным email возвращает статус 403"""

    status, result = pf.get_api_key(email, password)
    assert status == 403


def test_get_api_key_for_empty_password(email=valid_email, password=''):  # 4
    """ Проверяем, что запрос api ключа с пустым паролем возвращает статус 403"""

    status, result = pf.get_api_key(email, password)
    assert status == 403


def test_get_all_pets_with_invalid_key(filter=''):  # 5
    """ Проверяем, что запрос всех питомцев с неверным ключом возвращает статус 403.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее меняем ключ
    на несуществующий и запрашиваем список всех питомцев"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    auth_key['key'] = 'key'
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 403


def test_add_new_pet_with_empty_name(name='', animal_type='двортерьер', age='4'):  # 6
    """Проверяем, что нельзя добавить питомца без имени"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    assert status == 400
    assert len(name) == 0


def test_add_new_pet_with_unlimited_name(name='Барбоскин'*10, animal_type='двортерьер', age='4'):  # 7
    """Проверяем, что нельзя добавить питомца с именем больше 80 символов"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    assert status == 400
    assert len(name) > 80


def test_add_new_pet_with_invalid_animal_type(name='Барбоскин', animal_type='{двортерьер}', age='4'):  # 8
    """Проверяем, что нельзя добавить питомца с породой, имеющей в наименовании лишние символы.
    Для этого создаем множества для породы и нужных символов, и сравниваем их"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    lst_lat = [chr(i) for i in range(32, 123)]  # Символы от ' ' до 'z'
    lst_cyr = [chr(i) for i in range(1040, 1104)]  # Символы от 'А' до 'я'
    set_sym = set(animal_type).difference(lst_lat + lst_cyr)

    assert status == 400
    assert len(set_sym) > 0


def test_add_new_pet_with_invalid_age(name='Барбоскин', animal_type='двортерьер', age='age'):  # 9
    """Проверяем, что нельзя добавить питомца с нечисловым возрастом"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    str_int = None
    try:
        str_int = int(age)
    except ValueError:
        print(f"Значение '{age}' невозможно преобразовать в целое число")

    assert status == 400
    assert not str_int


def test_add_new_pet_with_negative_age(name='Барбоскин', animal_type='двортерьер', age='-3'):  # 10
    """Проверяем, что нельзя добавить питомца с отрицательным возрастом"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    assert status == 400
    assert int(age) < 0
