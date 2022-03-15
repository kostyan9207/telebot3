import telebot
from config import keys, TOKEN
from extensions import ConvertionException, CriptoConverter


bot = telebot.TeleBot(TOKEN)



@bot.message_handler(commands=['start', 'help'])
def help_help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду боту в следующем формате (через пробел):\n' \
           '<имя валюты цену которой он хочет узнать>\n' \
           '<имя валюты в которой надо узнать цену первой валюты>\n' \
           '<количество первой валюты>\n/values - вывод информации о всех доступных валютах(Как валюта обозначена так ее и указывать) '
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты(Как валюта обозначена так ее и указывать): '
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.upper().split(' ')
        if len(values) != 3:
            raise ConvertionException('Слишком много параметров.')
        # values[0] = values[0].upper()
        # values[1] = values[1].upper()
        # quote_ticker, base_ticker,  = keys[qoute], keys[base]
        quote, base, amount = values
        total_base = CriptoConverter.convert(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Стоимость {amount} {quote}  = {total_base} {base}'
        bot.send_message(message.chat.id, text)


bot.polling()