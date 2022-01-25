from settings import valid_email, valid_password
from api import PetFriends
from tools_for_test import *
import pytest


class TestPetFriendsGet:
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
    @pytest.mark.parametrize("filter", ['', 'my_pets'], ids=['empty string', 'only my pets'])
    def test_positive_get_pets(self, accept, content_type, filter):
        """ Проверяем, что запрос питомцев возвращает не пустой список,
        content-type возвращает application/json"""

        self.status_expected = 200
        self.status, result, ct = self.pf.get_list_of_pets(auth_key=self.auth_key, filter=filter, accept=accept)
        assert content_type in ct
        assert len(result['pets']) > 0

    @pytest.mark.parametrize("accept", ['application/xml', 'text/html'], ids=['xml', 'html'])
    @pytest.mark.parametrize("content_type", ['text/html'], ids=['html'])
    @pytest.mark.parametrize("filter", [0, generate_string(255), generate_string(1001), russian_chars(),
                                        russian_chars().upper(), chinese_chars(), special_chars(), '123'],
                             ids=['valid', '255 symbols', 'more than 1000 symbols', 'russian',
                                  'RUSSIAN', 'chinese', 'specials', 'digit'])
    def test_negative_get_pets(self, accept, content_type, filter):
        """ Проверяем, что запрос питомцев с неверным фильтром возвращает статус 400,
        content-type возвращает text/html, иначе должен возвращаться статус 415 """

        self.status_expected = 415

        if filter == 0:
            filter = 'my_pets'
        else:
            self.status_expected = 400

        self.status, result, ct = self.pf.get_list_of_pets(auth_key=self.auth_key, filter=filter, accept=accept)
        assert content_type in ct
