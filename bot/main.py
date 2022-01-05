import telebot

from utils.config import TOKEN
from commands.timetable import timetable

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=["start"])
def start(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('/Понедельник', '/Вторник', '/Среда', '/Четверг', '/Пятница', '/Суббота')
    bot.send_message(message.chat.id, 'Выберите день', reply_markup=keyboard)

@bot.message_handler(commands=["расписание",'Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Cуббота'])
def rasp(message):
    rasp = timetable(message=message.text)
    bot.send_message(message.chat.id, rasp)


bot.infinity_polling()