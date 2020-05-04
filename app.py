from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# Initialize App
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init Database
db = SQLAlchemy(app)

# Init Marshmallow
ma = Marshmallow(app)

##### Models #####

# Instructions for creating DB
# 1. Open Python Shell
# 2. Run: from flask import db
# 3. Run: db.create_all()

# Example Products Model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    price = db.Column(db.Float)
    amount = db.Column(db.Integer)

    def __init__(self, name, price, amount):
        self.name = name
        self.price = price
        self.amount = amount

##### Schemas #####

# Example Product Schema 
class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'price', 'amount')

# Init Schema
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

##### Routes #####

# Add Product POST
@app.route('/product', methods=['POST'])
def add_product():
    name = request.json['name']
    price = request.json['price']
    amount = request.json['amount']
    
    new_product = Product(name, price, amount)

    db.session.add(new_product)
    db.session.commit()

    return product_schema.jsonify(new_product)

# GET All Products 
@app.route('/product', methods=['GET'])
def get_products():
    all_products = Product.query.all()
    result = products_schema.dump(all_products)
    return jsonify(result)

# GET Single Product
@app.route('/product/<id>', methods=['GET'])
def get_product(id):
    product = Product.query.get(id)
    return product_schema.jsonify(product)

# Update a Product
@app.route('/product/<id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get(id)

    name = request.json['name']
    price = request.json['price']
    amount = request.json['amount']
    
    product.name = name
    product.price = price
    product.amount = amount

    db.session.commit()

    return product_schema.jsonify(product)

# DELETE Single Product
@app.route('/product/<id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get(id)
    db.session.delete(product)
    db.session.commit()

    return product_schema.jsonify(product)

# Run Server
if __name__ == '__main__':
    app.run(debug=True)