from config import TOKEN
from quickchart import QuickChart
from telebot import types
import telebot

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'Новый_график'])
def barName(message):
    msg = bot.send_message(message.chat.id, 'Введите название графика', reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, userBarName)

chooseSizeBar = types.ReplyKeyboardMarkup(row_width=2)
chooseSizeBar1 = types.KeyboardButton('Маленький')
chooseSizeBar2 = types.KeyboardButton('Средний')
chooseSizeBar3 = types.KeyboardButton('Большой')
chooseSizeBar.add(chooseSizeBar1, chooseSizeBar2, chooseSizeBar3)

def userBarName(message):
    user_data = {}
    user_data['name'] = message.text
    msg = bot.send_message(message.chat.id, 'Веберите размер графика', reply_markup=chooseSizeBar)
    bot.register_next_step_handler(msg, sizeStep, user_data)

def sizeStep(message, user_data):
    if message.text == 'Маленький':
        user_data['size'] = '300, 150'
    elif message.text ==  'Средний':
        user_data['size'] = '500, 300'
    elif message.text == 'Большой':
        user_data['size'] = '700, 400'
    msg = bot.send_message(message.chat.id, 'Укажите названия столбоцов через запятую. \nПример: Молоко, Сахар, Соль', reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, barLabels, user_data)

def barLabels(message, user_data):
    user_data['labels'] = message.text
    msg = bot.send_message(message.chat.id, 'Введите данные для ваших столбов через запятую. В том-же порядке, что и ваши названия столбцов\n' + user_data['labels'])
    bot.register_next_step_handler(msg, barData, user_data)


newBar = types.ReplyKeyboardMarkup(row_width=2)
newBar1 = types.KeyboardButton('/Новый_график')
newBar.add(newBar1)

def barData(message, user_data):
    user_data['data'] = message.text
    msg = bot.send_message(message.chat.id, 'Отлично все данные собраны!')
    qc = QuickChart()
    userBarSize = user_data['size'].split(',')
    userLabeles = user_data['labels'].split(',')
    userBarData = (user_data['data']).split(',')
    qc.width = userBarSize[0]
    qc.height = userBarSize[1]
    qc.config = {
    "type": "bar",
    "data": {
            "labels": userLabeles,
            "datasets": [{
                "label": user_data['name'],
                "data": userBarData
            }]
        }
    }

    bot.send_photo(message.chat.id, qc.get_url())
    bot.send_message(message.chat.id, 'Ваш график готов!\nСпасибо @MaxWatson', reply_markup=newBar)


bot.infinity_polling()