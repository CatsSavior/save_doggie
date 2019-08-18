import os
import django
os.environ["DJANGO_SETTINGS_MODULE"] = 'GoToCRM.settings'
django.setup()
from crm.models import Student, User
from django.contrib.auth import login, authenticate, logout

import telebot
import uuid
from telebot import types


token = "973907064:AAHUO1lOJ2-sflQ8AR-i6NLBo9oylcQB8jU"

# Обходим блокировку с помощью прокси
telebot.apihelper.proxy = {'https': 'socks5h://geek:socks@t.geekclass.ru:7777'}

# подключаемся к телеграму
bot = telebot.TeleBot(token=token)

exists = 0
log_in = 0


def login(user):

    bot.send_message(user, 'введи логин свой, негодяй')

def photo(user):

    bot.send_message(user, 'Кому аву менять будем?')




@bot.message_handler(commands=["start"])
def repeat_all_messages(message):
    # создаем клавиатуру
    keyboard = types.InlineKeyboardMarkup()

    # добавляем на нее две кнопки
    button1 = types.InlineKeyboardButton(text="Залогиниться", callback_data="button1")
    button2 = types.InlineKeyboardButton(text="Загрузить фото", callback_data="button2")
    keyboard.add(button1)
    keyboard.add(button2)

    # отправляем сообщение пользователю
    bot.send_message(message.chat.id, "Нажмите кнопку!", reply_markup=keyboard)


# функция запустится, когда пользователь нажмет на кнопку
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data == "button1":
            bot.send_message(call.message.chat.id, "Сейчас будем логиниться")
            login(call.message.chat.id)
        if call.data == "button2":
            bot.send_message(call.message.chat.id, "Сейчас будем загружать фото")
            photo(call.message.chat.id)


# content_types=['text'] - сработает, если нам прислали текстовое сообщение
@bot.message_handler(content_types=['text'])
def echo(message):

    global name_id, log_in

    # message - входящее сообщение
    # message.text - это его текст
    # message.chat.id - это номер его автора
    text = message.text
    user = message.chat.id

    for i in User.objects.all():
        if text == i.username:
            print('Пароль подошел')
            bot.send_message(user, 'Здарово, ' + i.username)
            log_in = 1
        else:
            print('Не робит')

    text_out = 'такого ученика нет'

    for e in Student.objects.all():
        global exists
        if text == e.name:
            text_out = 'Такой ученик есть'
            exists = 1
            name_id = e.id
            print(e.photo)
            if e.photo != None:
                with open(e.photo, 'rb') as new_file:
                    bot.send_photo(message.chat.id, new_file.read())
            else:
                text_out = 'Ученик есть, а фото нет'

    if exists == 1:
        bot.send_message(user, text_out)
    else:
        bot.send_message(user, text_out)



def add_pic(filename):
    global name_id, log_in
    if log_in == 1:
        student = Student.objects.get(pk=name_id)
        student.photo = filename
        student.save()
    else:
        print('У вас недостаточно прав')

    # обработка фотографии
    pass

@bot.message_handler(content_types=['photo'])
def photo(message):
    global exists
    # скачивание файла
    if exists == 1:
        file_id = message.photo[-1].file_id
        path = bot.get_file(file_id)
        downloaded_file = bot.download_file(path.file_path)

    # узнаем расширение и случайно придумываем имя
        extn = '.' + str(path.file_path).split('.')[-1]
        name = 'static/' + str(uuid.uuid4()) + extn

    # создаем файл и записываем туда данные
        with open(name, 'wb') as new_file:
            new_file.write(downloaded_file)

    # обрабатываем картинку фильтром
        add_pic(name)

    # открываем файл и отправляем его пользователю
        with open(name, 'rb') as new_file:
            bot.send_photo(message.chat.id, new_file.read())

# поллинг - вечный цикл с обновлением входящих сообщений
bot.polling(none_stop=True)
