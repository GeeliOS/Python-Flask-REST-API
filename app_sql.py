import sqlite3
from pathlib import Path
from flask import g
from flask import Flask, json, request

app = Flask(__name__)
json.provider.DefaultJSONProvider.ensure_ascii = False

BASE_DIR = Path(__file__).parent
DATABASE = BASE_DIR / 'test.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def tuple_to_dict(quote: tuple) -> dict:
    keys = ["id", "author", "text"]

    return dict(zip(keys, quote))


def get_object_from_db(sql: str) -> dict:
    connection = sqlite3.connect("test.db")
    cursor = connection.cursor()
    cursor.execute(sql)
    object = cursor.fetchone()
    object = tuple_to_dict(object)
    cursor.close()
    connection.close()
    return object


def get_objects_from_db(sql: str) -> list[dict]:
    connection = sqlite3.connect("test.db")
    cursor = connection.cursor()
    cursor.execute(sql)
    objects = cursor.fetchall()
    objects = list(map(tuple_to_dict, objects))
    cursor.close()
    connection.close()
    return objects


@app.route("/quotes")
def get_quotes():
    select_quotes = "SELECT * from quotes"
    quotes = get_objects_from_db(select_quotes)
    return quotes





@app.route("/quotes/<int:quote_id>")
def get_quote_by_id(quote_id):
    sql = f"SELECT * FROM quotes WHERE id={quote_id}"
    quote = get_object_from_db(sql)
    return quote

    return f"Quote with id={quote_id} not found", 404

# @app.route("/quotes/count")    # ДЗ Практика Данная функция выполняется по Заданию-3
# def quotes_count():
#     return {
#         "count": len(quotes)
#     }

# @app.route("/quotes/homework/<int:quote_id>")   # Практика №1 Данная функция выполняется по Заданию-4*
# def get_quote_by_id(quote_id):
#     for quote in quotes:
#         if quote["id"]==quote_id:
#             quot=choice(quotes)
#             return quot["text"]
#     return f"Quote with id={quote_id} not found", 404
#
#
#
# # Практика №2
# #############################################################################################
# @app.route("/quotes/filter", methods=["GET"])
# def filter_author_quote():
#     new_quote = []
#     args = request.args
#     if len(args) < 2:
#         for quote in quotes:
#             if quote["author"] == args["author"]:
#                 new_quote.append(quote)
#     else:
#         if args.get("up_to_rating") is None or args.get("from_the_rating") is None:
#             for quote in quotes:
#                 if (quote["author"] == args["author"]) and (quote["rating"] == int(args["rating"])):
#                     new_quote.append(quote)
#         else:
#             if int(args["up_to_rating"]) >= int(args["from_the_rating"]):
#                 for quote in quotes:
#                     if int(quote["rating"]) >= int(args["from_the_rating"]) and int(quote["rating"]) <= int(
#                             args["up_to_rating"]):
#                         new_quote.append(quote)
#             else:
#                 return f"Quote not found", 201
#     if new_quote:
#         return new_quote, 200
#     else:
#         return f"Quote not found", 201
#
#
# # @app.route("/quotes/rating", methods=["GET"])
# # def filter_rating():
# #     new_quote = []
# #     args = request.args
# #
# #     if args.get("up_to_rating") is None or args.get("from_the_rating") is None:
# #         return f"Quote not found", 400
# #
# #     for quote in quotes:
# #         if int(quote["rating"]) >= int(args["from_the_rating"]) and int(quote["rating"]) <= int(args["up_to_rating"]):
# #             new_quote.append(quote)
# #
# #
# #     if new_quote:
# #         return new_quote, 200
# #     else:
# #         return f"Quote not found", 201
#
#
#

@app.route("/quotes", methods=["POST"])
def create_quote():
    new_quote = request.json
    connection = get_db()
    cursor = connection.cursor()
    sql = f"INSERT INTO quotes (author, text) VALUES ('{new_quote['author']}', '{new_quote['text']}');"
    cursor.execute(sql)
    connection.commit()
    new_quote["id"] = cursor.lastrowid
    return new_quote, 201
#
#
#
# @app.route("/quotes/<int:quote_id>", methods=['PUT'])
# def edit_quote(quote_id):
#    new_data = request.json
#    for quote in quotes:
#     if quote["id"] == quote_id:
#         if new_data.get("author"):
#             quote["author"] = new_data["author"]
#         if new_data.get("text"):
#             quote["text"] = new_data["text"]
#         if new_data.get("rating"):
#             quote["rating"] = new_data["rating"]
#         return quote, 201
#
#    return f"Quote with id={quote_id} not found", 404
#
#
# @app.route("/quotes/<int:quote_id>", methods=['DELETE'])
# def delete_quote(quote_id):
#     i=0
#     for quote in quotes:
#         if quote["id"] == quote_id:
#           del quotes[i]
#           return quote, 204
#         else:
#           return f"Quote with id={quote_id} not found", 404
#         i+=1
# #############################################################################################
