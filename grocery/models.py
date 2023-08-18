from grocery import db,login_manager
from grocery import bcrypt
from flask_login import UserMixin
from datetime import datetime
from sqlalchemy import func


@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))

class User(db.Model,UserMixin):
  id = db.Column(db.Integer(), primary_key=True)
  username = db.Column(db.String(length=30), nullable=False, unique=True)
  email_address = db.Column(db.String(length=50), nullable=False, unique=True)
  password_hash = db.Column(db.String(length=60), nullable=False)
  carts= db.relationship("Cart",backref="user")
  orders = db.relationship("Order",backref='user')
  engagement = db.relationship("login_count",backref='user')

  @property
  def password(self):
    return self.password

  @password.setter
  def password(self, plain_text_password):
    self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

  def check_password_correction(self, attempted_password):
    return bcrypt.check_password_hash(self.password_hash, attempted_password)


class Category(db.Model):
  id = db.Column(db.Integer(), primary_key=True)
  name=db.Column(db.String(length=30),nullable=False,unique=True)
  description = db.Column(db.String(length=1024))
  items= db.relationship("Item",backref="category")
  def __repr__(self):
    return f'{self.name}'


  
cart_product = db.Table('cart_product',
db.Column('id',db.Integer, primary_key=True),
                      db.Column('cart_id',db.Integer,db.ForeignKey('cart.id'),nullable=False),
                        db.Column('product_id',db.Integer,db.ForeignKey('item.id'),nullable=False),
db.Column('quantity', db.Integer, nullable=False))

class Cart(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Order(db.Model):
  id = db.Column(db.Integer(),primary_key=True)
  user_id=db.Column(db.Integer(), db.ForeignKey('user.id'),nullable=False)
  amount=db.Column(db.Integer(),nullable=False)
  timestamp=db.Column(db.DateTime(),default=datetime.now)


order_product = db.Table('order_product',
db.Column('id',db.Integer, primary_key=True),
                      db.Column('order_id',db.Integer,db.ForeignKey('order.id'),nullable=False),
                        db.Column('product_id',db.Integer,db.ForeignKey('item.id'),nullable=False),
db.Column('quantity', db.Integer, nullable=False))




class Item(db.Model):
  id = db.Column(db.Integer(), primary_key=True)
  product = db.Column(db.String(length=30), nullable=False, unique=True)
  quantity_stored = db.Column(db.Integer(),nullable=False)
  quantity_purchased=db.Column(db.Integer())
  price = db.Column(db.Integer(), nullable=False)
  unit = db.Column(db.String(length=30), nullable=False)
  category_id=db.Column(db.Integer(),db.ForeignKey("category.id"))
  manufacture_date = db.Column(db.Date(),nullable=False)
  expiry_date = db.Column(db.Date(),nullable=False)
  description = db.Column(db.String(length=1024))
  photo_dest_path = db.Column(db.String())
  carts = db.relationship('Cart', secondary=cart_product, backref='products')
  orders = db.relationship('Order',secondary=order_product,backref='products')
  def __repr__(self):
      return f'Item {self.product}'

class login_count(db.Model):
  id = db.Column(db.Integer(), primary_key=True)
  user_id = db.Column(db.Integer,db.ForeignKey("user.id"))
  count = db.Column(db.Integer,default=0)



  


  


 
  
