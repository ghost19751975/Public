from settings import valid_email, valid_password
from api import PetFriends
from tools_for_test import *
import pytest
import os


class TestPetFriendsPost:
    @pytest.fixture(autouse=True)
    def test_get_api_key_for_valid_user(self):
        """ Проверяем, что запрос api ключа возвращает статус 200 и в результате содержится слово key"""

        self.pf = PetFriends()
        status, self.auth_key, ct = self.pf.get_api_key(email=valid_email, password=valid_password)
        assert status == 200
        assert 'application/json' in ct
        assert 'key' in self.auth_key

        yield

        assert self.status == self.status_expected

    @pytest.mark.parametrize("accept", ['application/json', '*/*'], ids=['json', 'any'])
    @pytest.mark.parametrize("content_type", ['application/json'], ids=['json'])
    @pytest.mark.parametrize("name", [generate_string(255), generate_string(1001), russian_chars(),
                                      russian_chars().upper(), chinese_chars(), special_chars(), '123'],
                             ids=['255 symbols', 'more than 1000 symbols', 'russian',
                                  'RUSSIAN', 'chinese', 'specials', 'digit'])
    @pytest.mark.parametrize("animal_type", [generate_string(255), generate_string(1001), russian_chars(),
                                             russian_chars().upper(), chinese_chars(), special_chars(), '123'],
                             ids=['255 symbols', 'more than 1000 symbols', 'russian',
                                  'RUSSIAN', 'chinese', 'specials', 'digit'])
    def test_positive_add_new_pet(self, accept, content_type, name, animal_type, age='1', pet_photo='images/cat1.jpg'):
        """Проверяем что можно добавить питомца с корректными данными"""

        self.status_expected = 200
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
        self.status, result, ct = self.pf.add_new_pet(auth_key=self.auth_key, name=name, animal_type=animal_type,
                                                      age=age, pet_photo=pet_photo, accept=accept)
        assert content_type in ct
        assert result['name'] == name

    @pytest.mark.parametrize("accept", ['application/xml', 'text/html'], ids=['xml', 'html'])
    @pytest.mark.parametrize("content_type", ['text/html'], ids=['html'])
    @pytest.mark.parametrize("age", [0, '', '-1', '0', '100', '1.5', '2147483647', '2147483648', special_chars(),
                                     russian_chars(), russian_chars().upper(), chinese_chars()],
                             ids=['valid', 'empty', 'negative', 'zero', 'greater than max', 'float', 'int_max',
                                  'int_max + 1', 'specials', 'russian', 'RUSSIAN', 'chinese'])
    @pytest.mark.parametrize("pet_photo", [0, '', 'images/cat1_crash.jpg', 'images/cat1.txt'],
                             ids=['valid', 'empty string', 'crash photo', 'text file'])
    def test_negative_add_new_pet(self, accept, content_type, age, pet_photo, name='', animal_type=''):
        """Проверяем, что добавление питомца с неверными данными возвращает статус 400,
        content-type возвращает text/html, иначе должен возвращаться статус 415"""

        self.status_expected = 415

        if age == 0 and pet_photo == 0:
            age = '1'
            pet_photo = 'images/cat1.jpg'
        else:
            self.status_expected = 400

        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
        self.status, result, ct = self.pf.add_new_pet(auth_key=self.auth_key, name=name, animal_type=animal_type,
                                                      age=age, pet_photo=pet_photo, accept=accept)
        assert content_type in ct

    @pytest.mark.parametrize("accept", ['application/json', '*/*'], ids=['json', 'any'])
    @pytest.mark.parametrize("content_type", ['application/json'], ids=['json'])
    @pytest.mark.parametrize("name", [generate_string(255), generate_string(1001), russian_chars(),
                                      russian_chars().upper(), chinese_chars(), special_chars(), '123'],
                             ids=['255 symbols', 'more than 1000 symbols', 'russian',
                                  'RUSSIAN', 'chinese', 'specials', 'digit'])
    @pytest.mark.parametrize("animal_type", [generate_string(255), generate_string(1001), russian_chars(),
                                             russian_chars().upper(), chinese_chars(), special_chars(), '123'],
                             ids=['255 symbols', 'more than 1000 symbols', 'russian',
                                  'RUSSIAN', 'chinese', 'specials', 'digit'])
    def test_positive_add_new_pet_without_photo(self, accept, content_type, name, animal_type, age='1'):
        """Проверяем, что можно добавить питомца без фото с корректными данными"""

        self.status_expected = 200
        self.status, result, ct = self.pf.add_new_pet_without_photo(auth_key=self.auth_key, name=name,
                                                                    animal_type=animal_type, age=age, accept=accept)
        assert content_type in ct
        assert result['name'] == name

    @pytest.mark.parametrize("accept", ['application/xml', 'text/html'], ids=['xml', 'html'])
    @pytest.mark.parametrize("content_type", ['text/html'], ids=['html'])
    @pytest.mark.parametrize("age", [0, '', '-1', '0', '100', '1.5', '2147483647', '2147483648', special_chars(),
                                     russian_chars(), russian_chars().upper(), chinese_chars()],
                             ids=['valid', 'empty', 'negative', 'zero', 'greater than max', 'float', 'int_max',
                                  'int_max + 1', 'specials', 'russian', 'RUSSIAN', 'chinese'])
    def test_negative_add_new_pet_without_photo(self, accept, content_type, age, name='', animal_type=''):
        """Проверяем, что добавление питомца без фото с неверными данными возвращает статус 400,
        content-type возвращает text/html, иначе должен возвращаться статус 415"""

        self.status_expected = 415

        if age == 0:
            age = '1'
        else:
            self.status_expected = 400

        self.status, result, ct = self.pf.add_new_pet_without_photo(auth_key=self.auth_key, name=name,
                                                                    animal_type=animal_type, age=age, accept=accept)
        assert content_type in ct

    @pytest.mark.parametrize("accept", ['application/json', '*/*'], ids=['json', 'any'])
    @pytest.mark.parametrize("content_type", ['application/json'], ids=['json'])
    def test_positive_add_photo_of_pet(self, accept, content_type, pet_photo='images/cat1.jpg'):
        """Проверяем, что можно добавить фото питомца с корректными данными"""

        self.status_expected = 200
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
        _, my_pets, _ = self.pf.get_list_of_pets(auth_key=self.auth_key, filter="my_pets")

        if len(my_pets['pets']) > 0:
            self.status, result, ct = self.pf.add_photo_of_pet(auth_key=self.auth_key, pet_id=my_pets['pets'][0]['id'],
                                                               pet_photo=pet_photo, accept=accept)
            assert content_type in ct
            assert result['id'] == my_pets['pets'][0]['id']
        else:
            raise Exception("There is no my pets")

    @pytest.mark.parametrize("accept", ['application/xml', 'text/html'], ids=['xml', 'html'])
    @pytest.mark.parametrize("content_type", ['text/html'], ids=['html'])
    @pytest.mark.parametrize("pet_photo", [0, '', 'images/cat1_crash.jpg', 'images/cat1.txt'],
                             ids=['valid', 'empty string', 'crash photo', 'text file'])
    @pytest.mark.parametrize("pet_id", [0, '', generate_string(255), generate_string(1001), russian_chars(),
                                        russian_chars().upper(), chinese_chars(), special_chars(), '123'],
                             ids=['valid', 'empty string', '255 symbols', 'more than 1000 symbols', 'russian',
                                  'RUSSIAN', 'chinese', 'specials', 'digit'])
    def test_negative_add_photo_of_pet(self, accept, content_type, pet_photo, pet_id):
        """Проверяем, что добавление неверного фото возвращает статус 400,
        content-type возвращает text/html, иначе должен возвращаться статус 415,
        при неверном id питомца должен возвращаться статус 404"""

        self.status_expected = 415

        if pet_photo == 0:
            pet_photo = 'images/cat1.jpg'
        else:
            self.status_expected = 400

        if pet_id == 0:
            _, my_pets, _ = self.pf.get_list_of_pets(auth_key=self.auth_key, filter="my_pets")

            if len(my_pets['pets']) > 0:
                pet_id = my_pets['pets'][0]['id']
            else:
                raise Exception("There is no my pets")
        else:
            self.status_expected = 404

        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
        self.status, result, ct = self.pf.add_photo_of_pet(auth_key=self.auth_key, pet_id=pet_id,
                                                           pet_photo=pet_photo, accept=accept)
        assert content_type in ct
