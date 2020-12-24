import telebot
import requests
import json

token = '1401557252:AAGmtPSFaHlEu1AVMcAP2Kt8gWV9tqzWyVk'
bot = telebot.TeleBot(token)
URL = "https://yesno.wtf/api"


@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id, "Привет, я помогу тебе принять решение! Задай вопрос, на который можно ответить Да ✔ или Нет ❌")
    bot.register_next_step_handler(message, show_answer)  # следующий шаг – функция show_answer


@bot.message_handler(commands=['help'])
def help_command(message):
    help = 'Привет, я решатель! \n\n' \
           'Своим рождением я обязан API сервиса yesno.wtf. ' \
            'Если вместо ответа ты видишь ошибку, значит, этот сервис временно не работает. ' \
            'Обещаю, я начну свою работу сразу, как только смогу! :)'
    bot.send_message(message.chat.id, text=help)


@bot.message_handler(content_types=['text'])
def show_answer(message):
    global URL
    if check_url(URL) is False:
        error = 'Извини, у меня выходной! Загляни пока в /help'
        bot.send_message(message.from_user.id, error)
    else:
        if message.text[-1] != '?':
            bot.send_message(message.from_user.id, "❓ Я жду вопрос :)")
            bot.register_next_step_handler(message, show_answer)
        else:
            dict = load_info()
            answer = dict.get("answer")
            image = dict.get("image")
            if answer == 'yes':
                bot.send_message(message.from_user.id, 'Да!')
                bot.send_message(message.from_user.id, image)
            else:
                bot.send_message(message.from_user.id, 'Нет!')
                bot.send_message(message.from_user.id, image)


# вспомогательная функция, проверяет корректность ответа URL-адреса
def check_url(URL):
    try:
        requests.head(URL)
    except:
        return False


# вспомогательная функция, загружает информацию по указанному URL-адресу и возвращает их в формате словаря
def load_info():
    return json.loads(requests.get(URL).text)


if __name__ == '__main__':
    bot.infinity_polling()

