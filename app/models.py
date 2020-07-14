import datetime
from flask_login import UserMixin
from app import db, app, login_manager, auth
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)


#this will handle user session, so we don't need to do anything
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(60), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.String(100))
    role = db.Column(db.String(20), default="patient")  # patient, doctor, super_admin

    # create a one to one relationship between User and patient
    patient = db.relationship('Patient', backref='user', uselist=False)
    # create a one to one relationship between User and doctor
    doctor = db.relationship('Doctor', backref='user', uselist=False)
    # create a one to one relationship between User and super_admin
    super_admin = db.relationship('SuperAdmin', backref='user', uselist=False)
    
    # create a one to many relationship between user and comment
    comments = db.relationship('ProductComment', backref='user', lazy=True)

    def generate_auth_token(self, expiration=app.config['TOKEN_EXPIRE_IN']):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None    # valid token, but expired
        except BadSignature:
            return None    # invalid token
        user = User.query.get(data['id'])
        return user
    
class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(40))
    address = db.Column(db.String(200))
    contact_no = db.Column(db.String(15))
    age = db.Column(db.Integer)
    profile_pic = db.Column(db.String(50), default="default.png")

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(40))
    address = db.Column(db.String(200))
    contact_no = db.Column(db.String(15))
    age = db.Column(db.Integer)
    profile_pic = db.Column(db.String(50), default="default.png")

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class SuperAdmin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(40))
    address = db.Column(db.String(200))
    contact_no = db.Column(db.String(15))
    age = db.Column(db.Integer)
    profile_pic = db.Column(db.String(50), default="default.png")

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# many to many between gym and trainers
product_checkout = db.Table('product_checkout', db.Column('product_id', db.Integer, db.ForeignKey('product.id')),
                            db.Column('checkout_id', db.Integer, db.ForeignKey('checkout.id')))

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    description = db.Column(db.String(5000))
    price = db.Column(db.Numeric)
    quantity = db.Column(db.Integer)
    post_date = db.Column(db.DateTime, default=datetime.datetime.now)
    last_modified = db.Column(db.DateTime, default=datetime.datetime.now)

    pictures = db.relationship('ProductPicture', backref='product', lazy=True)
    comments = db.relationship('ProductComment', backref='product', lazy=True)

class Checkout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    shipping_address = db.Column(db.String(500))
    cost = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    checkout_time = db.Column(db.DateTime, default=datetime.datetime.now)
    is_completed = db.Column(db.Integer) # 0 for pending checkout 1 for completed one

    # many to many between product and checkout
    products = db.relationship('Product', secondary=product_checkout, backref=db.backref('checkout', lazy=True))

class ProductPicture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    picture = db.Column(db.String(100))

class ProductComment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    comment_author = db.Column(db.Integer, db.ForeignKey('user.id'))
    comment_content = db.Column(db.String(1000))
    comment_date = db.Column(db.DateTime, default=datetime.datetime.now)