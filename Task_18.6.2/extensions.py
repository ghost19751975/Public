import requests
import json
from config import currency


class APIException(Exception):
    pass


class CurrencyConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):
        if base not in currency.keys():
            raise APIException(f'"{base}" : неверная исходная валюта!')
        if quote not in currency.keys():
            raise APIException(f'"{quote}" : неверная конечная валюта!')
        if quote == base:
            raise APIException('Укажите разные валюты!')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'"{amount}" : неверное количество валюты!')

        req_ = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={currency[base]}&tsyms={currency[quote]}')
        val_ = json.loads(req_.content)[currency[quote]]
        return val_ * amount


