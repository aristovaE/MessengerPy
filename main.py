# http запрос
# GET /search?q=Skillbox HTTP/1.1 #request line
# Host: google.com
# Accept: */*
# host,accept - ключи
# труба между сервером и пользователем - сокет(пара адрес порт)
# спец соглашения-протоколы-спецификации - определенные правила обмена информации (http)

# GET /status HTTP/1.1 #request line
# Host: 127.0.0.1:5000
# Accept: */*

# POST /send HTTP/1.1 #request line
# Host: 127.0.0.1:5000
# Accept: */*
# Content-Type: application/json
# Content-Length:69
# .............................

# 400е статус коды ошибок -пользователя, 500-е - сервера

# json объекты  - списки { "name": "nameee", "text": "texttt"}

# send message == положить message в db
# get messages == достать из db сообщения,
# которые не подгружены на клиенте

from flask import Flask, request, abort
import time
import json
import requests
from collections import Counter

app = Flask(__name__)

db = [
    {
        'time': time.time(),
        'name': 'Jack',
        'text': 'hi!',
    },
    {
        'time': time.time(),
        'name': 'Mary',
        'text': 'hello!',
    },
]


@app.route("/")
def hello():
    return "Hello, World!"


# добавить уникальных польхзователей и сколько сообщений всего
@app.route("/status")
def status():
    response = requests.get(
        'http://127.0.0.1:5000/messages',
        params={'after': 0}
    )
    messages = response.json()['message']
    list_names = []
    for message in messages:
        list_names.append(message['name'])
    unique_users = set(list_names)
    count_of_users = len(unique_users)
    count_of_message = len(messages)
    return {
        "status": True,
        "name": "myMes",
        "time": time.ctime(time.time()),
        # time.asctime() #Tue Feb 9 21:35:44 2021
        # datetime.now() #tue 09 feb 2021 21:35:44 GMT
        # str(datetime.now()
        # datetime.now().strtime('%Y/%m/%d') # 2021/02/09
        # datetime.now().iso #2021-02-09T21:39::29.212312
        "Count_of_Users": count_of_users,
        "Count_of_Message": count_of_message
    }


# POST
# request.json
# extract name,text
# validate name,text
@app.route("/send", methods=['POST'])
def send_message():
    data = request.json
    # проверка на корректность полученного data, чтобы была ошибка пользователя а не сервера
    if not isinstance(data, dict):
        return abort(400)

    name = data['name']
    text = data['text']

    # проверка на то что не пропущены данные
    if 'name' not in data or 'text' not in data:
        return abort(400)
    # проверка на то что элемента отправленоого 2
    if len(data) != 2:
        return abort(400)
    # проверка на то что name text являются нужного значения ИЛИ они пустые
    if not isinstance(name, str) or not isinstance(text, str) or name == '' or text == '':
        return abort(400)

    message = {
        'time': time.time(),
        'name': name,
        'text': text,
    }
    db.append(message)
    return {'ok': True}


# request.args
# extract after
# validate after
# paginate
@app.route("/messages")
def get_messages():
    # по умолчанию after - str
    try:
        after = float(request.args['after'])
    except:
        return abort(400)
    result = []
    for message in db:
        if message['time'] > after:
            result.append(message)
            if len(result) >= 100:
                break
    # пагинация slice первые сто элементов
    return {'message': result[:100]}


app.run()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
