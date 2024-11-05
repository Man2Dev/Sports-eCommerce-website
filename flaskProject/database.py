from __init__ import db, login_manager
from datetime import datetime
from flask_login import UserMixin

from pygments.lexer import default


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    email = db.Column(db.String(50),unique=True, nullable=False,primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    surname = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(100), nullable=True)
    phonenum = db.Column(db.String(20), unique=True, nullable=False)
    address = db.Column(db.String(100),unique=False, nullable=False)
    type = db.Column(db.String(50))
    __mapper_args__ = {
            'polymorphic_identity':'user',
            'polymorphic_on':type
        }

class Customer(User):
    __tablename__ = 'customer'
    __mapper_args__ = {
        'polymorphic_identity': 'customer',
    }
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'), nullable=False)

    def __repr__(self):
        return f'Customer {self.id} {self.name} {self.surname} created'


class Cart(db.Model):
    __tablename__ = 'cart'
    id=db.Column(db.Integer,primary_key=True)
    #Search how to create list of items
    owner_id=db.relationship('customer', backref="owner",lazy=True)
    def __repr__(self):
        return f'Cart {self.id} created'


class Admin(User):
    __tablename__ = 'Admin'
    __mapper_args__ = {
        'polymorphic_identity': 'admin',
    }
    def __repr__(self):
        return f'Admin {self.id} {self.name} {self.surname} created'

class Seller(User):
    __tablename__ = 'seller'
    __mapper_args__ = {
        'polymorphic_identity': 'seller',
    }
    def __repr__(self):
        return f'Seller {self.id} {self.name} {self.surname} created'

class Category(db.Model):
    __tablename__ = 'category'
    id=db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    def __repr__(self):
        return f'Category {self.id} {self.name} created'



class Item(db.Model):
    __tablename__ = 'item'
    id=db.Column(db.Integer,primary_key=True)
    price = db.Column(db.Float, nullable=False, default = 0.0)
    status = db.Column(db.String(50), nullable=False, default = 'active')
    amount = db.Column(db.Integer, nullable=False, default = 0)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(300), nullable=False)
    category = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    def __repr__(self):
        return f'Item {self.id} {self.name} {self.price} created'

class Item_Images(db.Model):
    __tablename__ = 'item_images'
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False, primary_key=True)
    image_url = db.Column(db.String(100), nullable=False, primary_key = True)
    def __repr__(self):
        return f'Item_image {self.item_id} {self.image_url}created'


class Item_Size(db.Model):
    __tablename__ = 'item_size'
    item_id = db.Column(db.Integer,db.ForeignKey('item.id'), primary_key=True)
    size = db.Column(db.String(5), primary_key=True)
    def __repr__(self):
        return f'Item_size {self.item_id} {self.size} created'


class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer,primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    customer_email = db.Column(db.String(50), db.ForeignKey('user.email'), nullable=False)
    def __repr__(self):
        return f'Order {self.id} {self.name} created'


class Cart_Item(db.Model):
    __tablename__ = 'cart_item'
    item_id = db.Column(db.Integer,db.ForeignKey('item.id'), primary_key=True)
    cart_id = db.Column(db.Integer,db.ForeignKey('cart.id'), primary_key=True)
    def __repr__(self):
        return f'Cart_Item {self.item_id} {self.cart_id} created'


class Order_Items(db.Model):
    __tablename__ = 'order_items'
    order_id = db.Column(db.Integer,db.ForeignKey('order.id'), primary_key=True)
    item_id = db.Column(db.Integer,db.ForeignKey('item.id'), primary_key=True)
    def __repr__(self):
        return f'Order_Items {self.order_id} {self.item_id} created'

class Seller_Items(db.Model):
    __tablename__ = 'seller_items'
    seller_email = db.Column(db.String(50), db.ForeignKey('user.email'), primary_key=True)
    item_id = db.Column(db.Integer,db.ForeignKey('item.id'), primary_key=True)
    def __repr__(self):
        return f'Seller_Items {self.seller_id} {self.item_id} created'

