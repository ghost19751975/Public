import telebot
from config import currency, TOKEN
from extensions import APIException, CurrencyConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message: telebot.types.Message):
    text = 'Шаблон команды для конвертации валюты :\n \
<Исходная валюта> <Конечная валюта> <Количество>\n\n \
/values - вывод доступных валют'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def handle_currency(message: telebot.types.Message):
    text = 'Доступные валюты :'
    for key in currency.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def handle_convert(message: telebot.types.Message):
    try:
        params = message.text.split(' ')
        if len(params) != 3:
            raise APIException('Неверное количество параметров!')

        base, quote, amount = params
        res_amount = CurrencyConverter.get_price(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя :\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду :\n{e}')
    else:
        text = f'{amount} {base} = {round(res_amount, 2)} {quote}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
