from flask import Blueprint, request, jsonify
from app import bcrypt, db
import secrets
from app.models import User, Patient, Doctor, SuperAdmin

api = Blueprint('api', __name__)


@api.route("/api/add/user", methods=["POST"])
def api_add_user():

    """Add new user
    Will receive data like this
    {
        "email": "farhadhossain0085@gmail.com",
        "date_of_birth": "1999-06-18",
        "role": "patient" or "doctor" "super_admin"
        "password": "1234",
        "full_name": "Farhad Hossain",
        "address": "Stadium para, Maijdee court",
        "contact_no": "01983495680",
        "age": 21
    }
    """

    data = request.get_json()

    username = secrets.token_hex(8)
    email = data['email'].lower()
    password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    date_of_birth = data['date_of_birth']
    role = data['role']

    full_name = data['full_name']
    address = data['address']
    contact_no = data['contact_no']
    age = data['age']

    # check if email already exists
    user = User.query.filter_by(email=email).first()

    if user:
        return jsonify({"message":"Hmm! User with this email already exist!"}), 403

    user = User(username=username,
                email=email,
                password=password,
                date_of_birth=date_of_birth,
                role=role)

    db.session.add(user)
    db.session.commit()

    if role == "patient":
        # now add the patient infos
        patient = Patient(full_name=full_name,
                          address=address,
                          contact_no=contact_no,
                          age=age,
                          user_id=user.id)

        db.session.add(patient)
        db.session.commit()

    elif role == "doctor":
        # now add the doctor infos
        doctor = Doctor(full_name=full_name,
                          address=address,
                          contact_no=contact_no,
                          age=age,
                          user_id=user.id)

        db.session.add(doctor)
        db.session.commit()

    elif role == "super_admin":
        # now add the super_admin infos
        super_admin = SuperAdmin(full_name=full_name,
                          address=address,
                          contact_no=contact_no,
                          age=age,
                          user_id=user.id)

        db.session.add(super_admin)
        db.session.commit()
    else:
        return jsonify({"message": "Invalid role!"}), 403

    return jsonify({"message": "Account created!"}), 201


@api.route("/api/get/user/<int:user_id>", methods=["GET"])
def api_get_user(user_id):
    """Get a single user info"""

    user = User.query.get(user_id)

    output = {}

    if not user:
        # if no user found with that user id
        return jsonify(output, {"message": "Not found"}), 404

    output['id'] = user.id
    output['username'] = user.username
    output['email'] = user.email
    output['role'] = user.role
    output['date_of_birth'] = user.date_of_birth

    if user.role == "patient":
        output['address'] = user.patient.address
        output['full_name'] = user.patient.full_name
        output['contact_no'] = user.patient.contact_no
        output['age'] = user.patient.age

    elif user.role == "doctor":
        output['address'] = user.doctor.address
        output['full_name'] = user.doctor.full_name
        output['contact_no'] = user.doctor.contact_no
        output['age'] = user.doctor.age

    else:
        output['address'] = user.super_admin.address
        output['full_name'] = user.super_admin.full_name
        output['contact_no'] = user.super_admin.contact_no
        output['age'] = user.super_admin.age


    return jsonify(output, {"message": "Success"}), 200