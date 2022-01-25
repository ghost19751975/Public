from settings import valid_email, valid_password
from api import PetFriends
from tools_for_test import *
import pytest


class TestPetFriendsAuth:
    pf = PetFriends()

    @pytest.mark.parametrize("accept", ['application/json', '*/*'], ids=['json', 'any'])
    @pytest.mark.parametrize("content_type", ['application/json'], ids=['json'])
    def test_positive_get_api_key(self, accept, content_type, email=valid_email, password=valid_password):
        """ Проверяем, что запрос api ключа возвращает статус 200, в результате содержится слово key,
        content-type возвращает application/json"""

        status, result, ct = self.pf.get_api_key(email=email, password=password, accept=accept)
        assert status == 200
        assert content_type in ct
        assert 'key' in result

    @pytest.mark.parametrize("accept", ['application/xml', 'text/html'], ids=['xml', 'html'])
    @pytest.mark.parametrize("content_type", ['text/html'], ids=['html'])
    @pytest.mark.parametrize("email", [0, '', generate_string(255), generate_string(1001), russian_chars(),
                                       russian_chars().upper(), chinese_chars(), special_chars(), '123'],
                             ids=['valid', 'empty string', '255 symbols', 'more than 1000 symbols', 'russian',
                                  'RUSSIAN', 'chinese', 'specials', 'digit'])
    @pytest.mark.parametrize("password", [0, '', generate_string(255), generate_string(1001), russian_chars(),
                                          russian_chars().upper(), chinese_chars(), special_chars(), '123'],
                             ids=['valid', 'empty string', '255 symbols', 'more than 1000 symbols', 'russian',
                                  'RUSSIAN', 'chinese', 'specials', 'digit'])
    def test_negative_get_api_key(self, accept, content_type, email, password):
        """ Проверяем, что запрос api ключа с неверными параметрами возвращает статус 403,
        content-type возвращает text/html, иначе должен возвращаться статус 415 """

        status_expected = 415

        if email == 0 and password == 0:
            email = valid_email
            password = valid_password
        else:
            status_expected = 403

        status, result, ct = self.pf.get_api_key(email=email, password=password, accept=accept)
        assert status == status_expected
        assert content_type in ct
