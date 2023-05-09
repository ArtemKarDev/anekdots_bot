import requests
import random
from random import randrange
from datetime import date
import telebot
from telebot import types
from bs4 import BeautifulSoup as bs



TOKEN_BOT = ''
with open('token.txt','r') as f:
    TOKEN_BOT = f.read()


# функция генерации случайной даты в определенном диапазоне
def random_day():
    day = f'202{str(randrange(4))}-{str(randrange(12)).zfill(2)}-{str(randrange(31)).zfill(2)}'
    return day

# функция проверки дотупности сгенерированного URL
def get_url():
    for i in range(3):
        URL = "https://www.anekdot.ru/release/anekdot/day/"+random_day()+"/"
        r = requests.head(URL)
        if str(r.status_code) == '200':
            break
        else:
            continue
    if str(r.status_code) != '200':
        URL  = "https://www.anekdot.ru/release/anekdot/week/"
    return URL

# функция парсинга 3 первых анектдотов со страницы
def parser():
    URL1 = get_url()
    r = requests.get(URL1)
    soup = bs(r.text, 'html.parser')
    for br in soup('br'):
        br.replace_with('\n')
    html_text = soup.find_all('div', class_='text')
    clear_anekdots = [c.text for c in html_text[:3]]
    anekdot = clear_anekdots[randrange(2)]
    return anekdot


bot = telebot.TeleBot(TOKEN_BOT)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Рассказать анекдот.")
    #btn2 = types.KeyboardButton("Анекдот дня.")
    markup.add(btn1) #,btn2)
    bot.send_message(message.chat.id, "Что хотел?", reply_markup=markup)

@bot.message_handler(content_types=['text'])
def get_text_message(message):
    if message.text == "Рассказать анекдот.":
        bot.send_message(message.chat.id, parser())


def main():
    # запускаем нашего бота
    bot.infinity_polling()


if __name__ == '__main__':
    main()