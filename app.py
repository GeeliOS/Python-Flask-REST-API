
from flask import Flask, abort, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from pathlib import Path

BASE_DIR = Path(__file__).parent

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{BASE_DIR / 'main.db'}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.app_context().push()

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class AuthorModel(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.String(32), unique=True)
   quotes = db.relationship('QuoteModel', backref='author', lazy='dynamic')

   def __init__(self, name):
       self.name = name

   def to_dict(self):
       return {
           "id": self.id,
           "name": self.name
       }

class QuoteModel(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   author_id = db.Column(db.Integer, db.ForeignKey(AuthorModel.id))
   text = db.Column(db.String(255), unique=False)

   def __init__(self, author, text):
       self.author_id = author.id
       self.text = text

   def to_dict(self):
       return {
           "id": self.id,
           "text": self.text,
           "author": self.author.to_dict
       }

   # dict --> JSON - сериализация
   # JSON --> dict - десериализация
   # Object --> dict --> JSON
@app.route("/quotes")
def get_quotes():
    quotes: list[QuoteModel] = QuoteModel.query.all()
    quotes_dict: list[dict] = []
    for quote in quotes:
        quotes_dict.append(quote.to_dict())
    return quotes_dict


@app.route("/quotes/<int:quote_id>")
def get_quote_by_id(quote_id):
    quote = QuoteModel.query.get(quote_id)
    if quote is None:
        return "Not found", 404
    return quote.to_dict()

@app.route("/quotes", methods=["POST"])
def create_quote():
    new_quote = request.json
    quote = QuoteModel(**new_quote)
    db.session.add(quote)
    db.session.commit()
    return quote.to_dict(), 201
