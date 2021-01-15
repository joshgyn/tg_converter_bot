import telebot
from pycbrf import ExchangeRates
from datetime import datetime
from telebot.types import KeyboardButton
import creds

rates = ExchangeRates(datetime.now())

bot = telebot.TeleBot(creds.TG_TOKEN)

keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2)
btn1 = telebot.types.KeyboardButton("USD->EUR")
btn2 = telebot.types.KeyboardButton("USD->RUB")
btn3 = telebot.types.KeyboardButton("RUB->EUR")
btn4 = telebot.types.KeyboardButton("RUB->USD")
btn5 = telebot.types.KeyboardButton("EUR->USD")
btn6 = telebot.types.KeyboardButton("EUR->RUB")
keyboard.add(btn1, btn2, btn3, btn4, btn5, btn6)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Hello, I am currency converter bot. "
                                      "If you want to see the list of available currencies tap /help",
                     reply_markup=keyboard)

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(message.chat.id, "You can use next currencies:\nAUD - Australian dollar\nAZN - Azerbaijani manat\nBYN"
                                      " - Belarusian Ruble\nBGN - Bulgarian Lev\nBRL - Brazilian Real\nDKK"
                                      " - Danish Krone\nUSD - US Dollar\nEUR - Euro\nCAD - Canadian Dollar\nCNY"
                                      " - China Yuan\nTMT - New Turkmenistan Manat\nPLN - Polish Zloty\nRON"
                                      " - Romanian Leu\nXDR - Special Drawing Rights\nSGD - Singapore Dollar\nGBP"
                                      " - British Pound Sterling\nCHF - Swiss Franc\nRUB - Russian Ruble")


@bot.message_handler(content_types=['text'])
def select_converting_type(message):
    if '->' in message.text:
        currency = message.text.split("->")
        bot.send_message(message.chat.id, f"How many {currency[0]} do you have?")
        bot.register_next_step_handler(message, converting, currency)
    else:
        bot.send_message(message.chat.id, "Something went wrong! Try again please", reply_markup=keyboard)


def converting(message, currency):
    if message.text.isdigit():
        if currency[1] == "RUB":
            bot.send_message(message.chat.id,
                             f"You have {round(float(message.text) * float(rates[currency[0]].value), 2)} {currency[1]}",
                             reply_markup=keyboard)
        elif currency[0] == "RUB":
            bot.send_message(message.chat.id,
                             f"You have {round(float(message.text) / float(rates[currency[1]].value), 2)} {currency[1]}",
                             reply_markup=keyboard)
        else:
            bot.send_message(message.chat.id,
                             f"You have {round(float(message.text) * float(rates[currency[0]].value) / float(rates[currency[1]].value), 2)} {currency[1]}",
                             reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, "It is not a number! Please, try again", reply_markup=keyboard)




bot.polling()
