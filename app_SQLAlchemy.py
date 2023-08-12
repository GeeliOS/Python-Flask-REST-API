from flask import Flask, json, request
from random import choice


app = Flask(__name__)
json.provider.DefaultJSONProvider.ensure_ascii = False

about_me = {
   "name": "Евгений",
   "surname": "Юрченко",
   "email": "eyurchenko@specialist.ru",
   "rating": 1
}

quotes = [
   {
       "id": 3,
       "author": "Rick Cook",
       "text": "Программирование сегодня — это гонка разработчиков программ, стремящихся писать программы с большей и лучшей идиотоустойчивостью, и вселенной, которая пытается создать больше отборных идиотов. Пока вселенная побеждает.",
       "rating": 1
   },
    {
        "id": 6,
        "author": "Yoggi Berra",
        "text": "Блины вкусные когда они горячие.",
        "rating": 2
    },
    {
        "id": 11,
        "author": "Yoggi Berra",
        "text": "Алладий",
        "rating": 2
    },
   {
       "id": 5,
       "author": "Waldi Ravens",
       "text": "Программирование на С похоже на быстрые танцы на только что отполированном полу людей с острыми бритвами в руках.",
       "rating": 3
   },
   {
       "id": 6,
       "author": "Mosher’s Law of Software Engineering",
       "text": "Не волнуйтесь, если что-то не работает. Если бы всё работало, вас бы уволили.",
       "rating": 1
   },
   {
       "id": 8,
       "author": "Yoggi Berra",
       "text": "В теории, теория и практика неразделимы. На практике это не так.",
       "rating": 4
   },

]








@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/about")
def about_author():
    return about_me

@app.route("/quotes")
def get_quotes():
    return quotes



@app.route("/quotes/<int:quote_id>")    # Практика №1 Данная функция выполняется по Заданию-2
def get_quote(quote_id):
    for quote in quotes:
        if quote["id"] == quote_id:
            return quote

    return f"Quote with id={quote_id} not found", 404

@app.route("/quotes/count")    # ДЗ Практика Данная функция выполняется по Заданию-3
def quotes_count():
    return {
        "count": len(quotes)
    }

@app.route("/quotes/homework/<int:quote_id>")   # Практика №1 Данная функция выполняется по Заданию-4*
def get_quote_by_id(quote_id):
    for quote in quotes:
        if quote["id"]==quote_id:
            quot=choice(quotes)
            return quot["text"]
    return f"Quote with id={quote_id} not found", 404



# Практика №2
#############################################################################################
@app.route("/quotes/filter", methods=["GET"])
def filter_author_quote():
    new_quote = []
    args = request.args
    if len(args) < 2:
        for quote in quotes:
            if quote["author"] == args["author"]:
                new_quote.append(quote)
    else:
        if args.get("up_to_rating") is None or args.get("from_the_rating") is None:
            for quote in quotes:
                if (quote["author"] == args["author"]) and (quote["rating"] == int(args["rating"])):
                    new_quote.append(quote)
        else:
            if int(args["up_to_rating"]) >= int(args["from_the_rating"]):
                for quote in quotes:
                    if int(quote["rating"]) >= int(args["from_the_rating"]) and int(quote["rating"]) <= int(
                            args["up_to_rating"]):
                        new_quote.append(quote)
            else:
                return f"Quote not found", 201




    if new_quote:
        return new_quote, 200
    else:
        return f"Quote not found", 201


# @app.route("/quotes/rating", methods=["GET"])
# def filter_rating():
#     new_quote = []
#     args = request.args
#
#     if args.get("up_to_rating") is None or args.get("from_the_rating") is None:
#         return f"Quote not found", 400
#
#     for quote in quotes:
#         if int(quote["rating"]) >= int(args["from_the_rating"]) and int(quote["rating"]) <= int(args["up_to_rating"]):
#             new_quote.append(quote)
#
#
#     if new_quote:
#         return new_quote, 200
#     else:
#         return f"Quote not found", 201



@app.route("/quotes", methods=["POST"])
def create_quote():
   new_quote = request.json
   new_id = quotes[-1]["id"]+1
   new_quote["id"] = new_id
   if(int(new_quote["rating"])==0):
       new_rating = 1
       new_quote["rating"] = new_rating
   quotes.append(new_quote)
   return new_quote, 200



@app.route("/quotes/<int:quote_id>", methods=['PUT'])
def edit_quote(quote_id):
   new_data = request.json
   for quote in quotes:
    if quote["id"] == quote_id:
        if new_data.get("author"):
            quote["author"] = new_data["author"]
        if new_data.get("text"):
            quote["text"] = new_data["text"]
        if new_data.get("rating"):
            quote["rating"] = new_data["rating"]
        return quote, 201

   return f"Quote with id={quote_id} not found", 404


@app.route("/quotes/<int:quote_id>", methods=['DELETE'])
def delete_quote(quote_id):
    i=0
    for quote in quotes:
        if quote["id"] == quote_id:
          del quotes[i]
          return quote, 204
        else:
          return f"Quote with id={quote_id} not found", 404
        i+=1
#############################################################################################