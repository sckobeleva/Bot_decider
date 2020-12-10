import telebot
import requests
import json

token = '1401557252:AAGmtPSFaHlEu1AVMcAP2Kt8gWV9tqzWyVk'
bot = telebot.TeleBot(token)
URL = "https://yesno.wtf/api"


@bot.message_handler(commands=['start','help'])
def start_command(message):
    bot.send_message(message.chat.id, "Привет, я помогу тебе принять решение! Приступим?")


@bot.message_handler(content_types=['text'])
def ask_question(message):
    bot.send_message(message.from_user.id, "Задай вопрос, на который можно ответить 'Да' или 'Нет'")
    bot.register_next_step_handler(message, show_answer)  # следующий шаг – функция show_answer


@bot.message_handler(content_types=['text'])
def show_answer(message):
    dict = load_info()
    answer = dict.get("answer")
    image = dict.get("image")
    if answer == 'yes':
        bot.send_message(message.from_user.id, 'Да!')
    else:
        bot.send_message(message.from_user.id, 'Нет!')
    bot.send_message(message.from_user.id, image)


# вспомогательная функция, загружает информацию по указанному URL-адресу и возвращает их в формате словаря
def load_info():
    return json.loads(requests.get(URL).text)


if __name__ == '__main__':
    bot.infinity_polling()

