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