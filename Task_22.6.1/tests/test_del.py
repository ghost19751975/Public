from settings import valid_email, valid_password
from api import PetFriends
from tools_for_test import *
import pytest


class TestPetFriendsDel:
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
    def test_positive_delete_pet(self, accept, content_type):
        """Проверяем возможность удаления питомца"""

        self.status_expected = 200
        _, my_pets, _ = self.pf.get_list_of_pets(auth_key=self.auth_key, filter="my_pets")

        if len(my_pets['pets']) == 0:
            self.pf.add_new_pet(auth_key=self.auth_key, name="Суперкот", animal_type="кот", age="3", pet_photo="images/cat1.jpg")
            _, my_pets, _ = self.pf.get_list_of_pets(auth_key=self.auth_key, filter="my_pets")

        pet_id = my_pets['pets'][0]['id']
        self.status, _, ct = self.pf.delete_pet(auth_key=self.auth_key, pet_id=pet_id, accept=accept)
        _, my_pets, _ = self.pf.get_list_of_pets(auth_key=self.auth_key, filter="my_pets")
        assert content_type in ct
        assert pet_id not in my_pets.values()

    @pytest.mark.parametrize("accept", ['application/xml', 'text/html'], ids=['xml', 'html'])
    @pytest.mark.parametrize("content_type", ['text/html'], ids=['html'])
    @pytest.mark.parametrize("pet_id", [0, '', generate_string(255), generate_string(1001), russian_chars(),
                                        russian_chars().upper(), chinese_chars(), special_chars(), '123'],
                             ids=['valid', 'empty string', '255 symbols', 'more than 1000 symbols', 'russian',
                                  'RUSSIAN', 'chinese', 'specials', 'digit'])
    def test_negative_delete_pet(self, accept, content_type, pet_id):
        """Проверяем, что удаление питомца с неверным id возвращает статус 404,
        content-type возвращает text/html, иначе должен возвращаться статус 415"""

        self.status_expected = 415

        if pet_id == 0:
            _, my_pets, _ = self.pf.get_list_of_pets(auth_key=self.auth_key, filter="my_pets")

            if len(my_pets['pets']) > 0:
                pet_id = my_pets['pets'][0]['id']
            else:
                raise Exception("There is no my pets")
        else:
            self.status_expected = 404

        self.status, _, ct = self.pf.delete_pet(auth_key=self.auth_key, pet_id=pet_id)
        assert content_type in ct
