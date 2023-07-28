from flask import Flask, json
from random import choice

app = Flask(__name__)
json.provider.DefaultJSONProvider.ensure_ascii = False

about_me = {
   "name": "Евгений",
   "surname": "Юрченко",
   "email": "eyurchenko@specialist.ru"
}

quotes = [
   {
       "id": 3,
       "author": "Rick Cook",
       "text": "Программирование сегодня — это гонка разработчиков программ, стремящихся писать программы с большей и лучшей идиотоустойчивостью, и вселенной, которая пытается создать больше отборных идиотов. Пока вселенная побеждает."
   },
   {
       "id": 5,
       "author": "Waldi Ravens",
       "text": "Программирование на С похоже на быстрые танцы на только что отполированном полу людей с острыми бритвами в руках."
   },
   {
       "id": 6,
       "author": "Mosher’s Law of Software Engineering",
       "text": "Не волнуйтесь, если что-то не работает. Если бы всё работало, вас бы уволили."
   },
   {
       "id": 8,
       "author": "Yoggi Berra",
       "text": "В теории, теория и практика неразделимы. На практике это не так."
   },

]


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/about")
def about_author():
    return about_me




@app.route("/quotes/<int:quote_id>")    # Данная функция выполняется по Заданию-2
def get_quote(quote_id):
    for quote in quotes:
        if quote["id"]==quote_id:
            return quote

    return f"Quote with id={quote_id} not found", 404


@app.route("/quotes/homework/<int:quote_id>")   # Данная функция выполняется по Заданию-4*
def get_quote_by_id(quote_id):
    for quote in quotes:
        if quote["id"]==quote_id:
            quot=choice(quotes)
            return quot["text"]
    return f"Quote with id={quote_id} not found", 404


@app.route("/quotes/count")    # Данная функция выполняется по Заданию-3
def quotes_count():
    return {
        "count": len(quotes)
    }