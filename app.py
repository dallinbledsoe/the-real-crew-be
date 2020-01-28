from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_heroku import Heroku
from environs import Env
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)
heroku = Heroku(app)
env = Env()
env.read_env()
DATABASE_URL= env("DATABASE_URL")

basedir = os.path.abspath(os.path.dirname(__file__))
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "app.sqlite")
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Product(db.Model):
  __tablename__ = "products"
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(150), unique=True, nullable=False)
  hat = db.Column(db.Boolean())
  category = db.Column(db.String(100))
  price = db.Column(db.String(100))
  prodimg = db.Column(db.String(1000))


  def __init__(self, title, hat, category, price, prodimg):
    self.title = title
    self.hat = hat
    self.category = category
    self.price = price
    self.prodimg = prodimg

class ProductSchema(ma.Schema):
  class Meta:
    fields = ("id", "title", "shirt", "hat", "category", "price", "prodimg")

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

# CRUD
# GET
@app.route("/products", methods=["GET"])
def get_products():
  all_products = Product.query.all()
  result = products_schema.dump(all_products)

  return jsonify(result)

# POST
@app.route("/product", methods=["POST"])
def add_product():
  title = request.json["title"]
  hat = request.json["hat"]
  category = request.json["category"]
  price = request.json["price"]
  prodimg = request.json["prodimg"]

  new_product = Product(title, hat, category, price, prodimg)

  db.session.add(new_product)
  db.session.commit()

  product = Product.query.get(new_product.id)
  return product_schema.jsonify(product)


# PUT/PATCH by ID
@app.route("/product/<id>", methods=["PATCH"])
def update_product(id):
product = Product.query.get(id)

new_done = request.json["done"]

product.done = new_done

db.session.commit()
return product_schema.jsonify(product)

# DELETE
@app.route("/product/<id>", methods=["DELETE"])
def delete_product(id):
  product = Product.query.get(id)
  db.session.delete(product)
  db.session.commit()

  return jsonify("Got rid of that ish!")

if __name__ == "__main__":
  app.debug = True
  app.run()