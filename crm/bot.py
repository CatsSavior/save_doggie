import os
import django
os.environ["DJANGO_SETTINGS_MODULE"] = 'GoToCRM.settings'
django.setup()
from crm.models import Student

import telebot
import uuid


token = "973907064:AAHUO1lOJ2-sflQ8AR-i6NLBo9oylcQB8jU"

# Обходим блокировку с помощью прокси
telebot.apihelper.proxy = {'https': 'socks5h://geek:socks@t.geekclass.ru:7777'}

# подключаемся к телеграму
bot = telebot.TeleBot(token=token)

exists = 0


# реагируем на команды /start и /help
@bot.message_handler(commands=['start', 'help'])
def help(message):
    user = message.chat.id
    bot.send_message(user, "Это бот попугай! Просто пришли и я повторю.")

# content_types=['text'] - сработает, если нам прислали текстовое сообщение
@bot.message_handler(content_types=['text'])
def echo(message):

    global name_id

    # message - входящее сообщение
    # message.text - это его текст
    # message.chat.id - это номер его автора
    text = message.text
    user = message.chat.id



    text_out = 'Такого ученика нет'

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


    #отправляем сообщение тому же пользователю с тем же текстом
    bot.send_message(user, text_out)


def add_pic(filename):
    global name_id
    student = Student.objects.get(pk=name_id)
    student.photo = filename
    student.save()

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