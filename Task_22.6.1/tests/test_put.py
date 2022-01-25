from settings import valid_email, valid_password
from api import PetFriends
from tools_for_test import *
import pytest


class TestPetFriendsPut:
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
    def test_positive_update_pet_info(self, accept, content_type, name, animal_type, age='1'):
        """Проверяем возможность обновления информации о питомце"""

        self.status_expected = 200
        _, my_pets, _ = self.pf.get_list_of_pets(auth_key=self.auth_key, filter="my_pets")

        if len(my_pets['pets']) > 0:
            self.status, result, ct = self.pf.update_pet_info(auth_key=self.auth_key, pet_id=my_pets['pets'][0]['id'],
                                                              name=name, animal_type=animal_type, age=age, accept=accept)
            assert content_type in ct
            assert result['name'] == name
        else:
            raise Exception("There is no my pets")

    @pytest.mark.parametrize("accept", ['application/xml', 'text/html'], ids=['xml', 'html'])
    @pytest.mark.parametrize("content_type", ['text/html'], ids=['html'])
    @pytest.mark.parametrize("age", [0, '', '-1', '0', '100', '1.5', '2147483647', '2147483648', special_chars(),
                                     russian_chars(), russian_chars().upper(), chinese_chars()],
                             ids=['valid', 'empty', 'negative', 'zero', 'greater than max', 'float', 'int_max',
                                  'int_max + 1', 'specials', 'russian', 'RUSSIAN', 'chinese'])
    @pytest.mark.parametrize("pet_id", [0, '', generate_string(255), generate_string(1001), russian_chars(),
                                        russian_chars().upper(), chinese_chars(), special_chars(), '123'],
                             ids=['valid', 'empty string', '255 symbols', 'more than 1000 symbols', 'russian',
                                  'RUSSIAN', 'chinese', 'specials', 'digit'])
    def test_negative_update_pet_info(self, accept, content_type, age, pet_id, name='', animal_type=''):
        """Проверяем, что изменение питомца с неверными данными возвращает статус 400,
        content-type возвращает text/html, иначе должен возвращаться статус 415,
        при неверном id питомца должен возвращаться статус 404"""

        self.status_expected = 415

        if age == 0:
            age = '1'
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

        self.status, result, ct = self.pf.update_pet_info(auth_key=self.auth_key, pet_id=pet_id, name=name,
                                                          animal_type=animal_type, age=age, accept=accept)
        assert content_type in ct
