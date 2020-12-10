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
    answer_part1 = dict.get("answer")
    answer_part2 = dict.get("image")
    bot.send_message(message.from_user.id, answer_part1)
    bot.send_message(message.from_user.id, answer_part2)


# вспомогательная функция, загружает информацию по указанному URL-адресу и возвращает их в формате словаря
def load_info():
    return json.loads(requests.get(URL).text)


if __name__ == '__main__':
     bot.infinity_polling()
# еще можно просто одной строчкой:
# bot.polling(none_stop=True)
