from flask import Blueprint, request, jsonify, make_response, g
from app import bcrypt, db
import secrets, base64
from app.models import User, Patient, Doctor, SuperAdmin, Product, ProductPicture
from app import auth
from app.utils import save_picture

api = Blueprint('api', __name__)

"""
We will use this for check user access, this is really great
current_user = auth.current_user()
then we can access current user infos.
"""

@auth.verify_password
def verify_password(email_or_token, password):

    user = User.verify_auth_token(email_or_token)
    if not user:
        # try to authenticate with username/password

        user = User.query.filter_by(email=email_or_token).first()
        if not user or not bcrypt.check_password_hash(user.password, password):
            return False

    g.user = user
    return user

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)

@api.route('/api/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token(3600)
    return jsonify({'token': token.decode('ascii'), 'duration': 3600, 'user_id': g.user.id})


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
        "age": 21,
        "profile_pic": "base64 encoded image string"
    }
    """
    data = request.get_json()
   
    username = secrets.token_hex(8)
    
    email = data['email'].lower()

    password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    date_of_birth = data['date_of_birth']

    if 'role' not in data:
    	role = 'patient'
    else:
	    role = data['role']

    full_name = data['full_name']
    address = data['address']
    contact_no = data['contact_no']
    age = data['age']
    

    if 'profile_pic' in data:
        profile_pic = data['profile_pic']
        imgdata = base64.b64decode(profile_pic.split(',')[1])
        filename = save_picture(img=imgdata, folder="profile_pics")
    
    # check if email already exists
    user = User.query.filter_by(email=email).first()


    if user:
        return jsonify({"message":"user exists"}), 403

    user = User(username=username,
                email=email,
                password=password,
                date_of_birth=date_of_birth,
                role=role)

    db.session.add(user)
    db.session.commit()

    if role == "patient":
        # now add the patient infos
        if 'profile_pic' in data:
            # now add the patient infos
            patient = Patient(full_name=full_name,
                              address=address,
                              contact_no=contact_no,
                              age=age,
                              profile_pic=filename,
                              user_id=user.id)
        else:
            patient = Patient(full_name=full_name,
                              address=address,
                              contact_no=contact_no,
                              age=age,
                              user_id=user.id)

        db.session.add(patient)
        db.session.commit()

    elif role == "doctor":
        # now add the doctor infos
        if 'profile_pic' in data:
            # now add the patient infos
            doctor = Doctor(full_name=full_name,
                              address=address,
                              contact_no=contact_no,
                              age=age,
                              profile_pic=filename,
                              user_id=user.id)
        else:
            doctor = Doctor(full_name=full_name,
                              address=address,
                              contact_no=contact_no,
                              age=age,
                              user_id=user.id)

        db.session.add(doctor)
        db.session.commit()

    elif role == "super_admin":
        # now add the super_admin infos
        if 'profile_pic' in data:
            # now add the patient infos
            super_admin = SuperAdmin(full_name=full_name,
                              address=address,
                              contact_no=contact_no,
                              age=age,
                              profile_pic=filename,
                              user_id=user.id)
        else:
            super_admin = SuperAdmin(full_name=full_name,
                              address=address,
                              contact_no=contact_no,
                              age=age,
                              user_id=user.id)

        db.session.add(super_admin)
        db.session.commit()
    else:
        return jsonify({"message": "invalid role"}), 403

    return jsonify({"message": "success"}), 201


@api.route("/api/get/user/<int:user_id>", methods=["GET"])
@auth.login_required
def api_get_user(user_id):
    """Get a single user info"""

    user = User.query.get(user_id)

    output = {}

    if not user:
        # if no user found with that user id
        return jsonify(output, {"message": "not found"}), 404

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
        output['profile_pic'] = user.patient.profile_pic

    elif user.role == "doctor":
        output['address'] = user.doctor.address
        output['full_name'] = user.doctor.full_name
        output['contact_no'] = user.doctor.contact_no
        output['age'] = user.doctor.age
        output['profile_pic'] = user.doctor.profile_pic

    else:
        output['address'] = user.super_admin.address
        output['full_name'] = user.super_admin.full_name
        output['contact_no'] = user.super_admin.contact_no
        output['age'] = user.super_admin.age
        output['profile_pic'] = user.super_admin.profile_pic


    return jsonify(output, {"message": "success"}), 200


@api.route("/api/get/users", methods=["GET"])
@auth.login_required
def api_get_users():
    """Get a single user info"""

    users = User.query.all()

    users_list = []

    for user in users:

        output = {}

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
            output['profile_pic'] = user.patient.profile_pic

        elif user.role == "doctor":
            output['address'] = user.doctor.address
            output['full_name'] = user.doctor.full_name
            output['contact_no'] = user.doctor.contact_no
            output['age'] = user.doctor.age
            output['profile_pic'] = user.doctor.profile_pic

        else:
            output['address'] = user.super_admin.address
            output['full_name'] = user.super_admin.full_name
            output['contact_no'] = user.super_admin.contact_no
            output['age'] = user.super_admin.age
            output['profile_pic'] = user.super_admin.profile_pic

        users_list.append(output)


    return jsonify(users_list, {"message": "success"}), 200


@api.route("/api/add/user/<int:user_id>", methods=["PUT"])
def api_edit_user(user_id):

    """Edit new user
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

    user = User.query.get(user_id)

    if not user:
        return jsonify({"message": "not found"}), 404

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

    profile_pic = data['profile_pic']

    if 'profile_pic' in data:
        imgdata = base64.b64decode(profile_pic.split(',')[1])
        filename = save_picture(img=imgdata, folder="profile_pics")

    # check if email already exists
    if user.email != email:
        user = User.query.filter_by(email=email).first()

        if user:
            return jsonify({"message":"user exists"}), 403

    user.username=username
    user.email=email
    user.password=password
    user.date_of_birth=date_of_birth
    user.role=role

    db.session.commit()

    if role == "patient":
        # now edit the patient infos

        patient = user.patient

        patient.full_name=full_name
        patient.address=address
        patient.contact_no=contact_no
        patient.age=age
        patient.profile_pic=filename
        patient.user_id=user.id

        db.session.commit()

    elif role == "doctor":
        # now edit the doctor infos
        doctor = user.doctor

        doctor.full_name=full_name
        doctor.address=address
        doctor.contact_no=contact_no
        doctor.age=age
        doctor.profile_pic=filename
        doctor.user_id=user.id

        db.session.commit()

    elif role == "super_admin":
        # now edit the super_admin infos
        super_admin = user.super_admin

        super_admin.full_name=full_name
        super_admin.address=address
        super_admin.contact_no=contact_no
        super_admin.age=age
        super_admin.profile_pic=filename
        super_admin.user_id=user.id

        db.session.commit()
    else:
        return jsonify({"message": "invalid role"}), 403

    return jsonify({"message": "success"}), 200


@api.route("/api/get/user/<int:user_id>", methods=["DELETE"])
@auth.login_required
def api_delete_user(user_id):
    """Get a single user info"""

    user = User.query.get(user_id)

    if not user:
        return jsonify({"message": "not found"}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "success"}), 200

# User's API ends here!

# Product API starts

@api.route("/api/add/product", methods=["POST"])
#@auth.login_required
def api_add_product():
    """
    Add product
    {
        "name": "Paracetemol",
        "description": "Paracetemol is a very good medicine",
        "price": 20,
        "quantity": 5,
        "pictures": [
                        "base64 encoded image string",
                        "base64 encoded image string",
                        "base64 encoded image string"
                    ]
    }
    """

    try:
        data = request.get_json()

        name = data['name']
        description = data['description']
        price = data['price']
        quantity = data['quantity']
        pictures = data['pictures']

        product = Product(name=name,
                        description=description,
                        price=price,
                        quantity=quantity)

        db.session.add(product)
        db.session.commit()

        for picture in pictures:
            imgdata = base64.b64decode(picture.split(',')[1])
            filename = save_picture(img=imgdata, folder="product_picture")

            product_picture = ProductPicture(product_id=product.id,
                                            picture=filename)
            db.session.add(product_picture)

        db.session.commit()

    except:
        return jsonify({"message": "error"}), 403

    output = {}
    output['id'] = product.id

    return jsonify(output, {"message": "success"}), 200


@api.route("/api/edit/product", methods=["PUT"])
#@auth.login_required
def api_edit_product():
    """
    Edit product
    {
        "id": 2,
        "name": "Paracetemol",
        "description": "Paracetemol is a very good medicine",
        "price": 20,
        "quantity": 5,
        "pictures": [
                        "base64 encoded image string",
                        "base64 encoded image string",
                        "base64 encoded image string"
                    ]
    }
    """

    try:
        data = request.get_json()

        product_id = data['id']
        name = data['name']
        description = data['description']
        price = data['price']
        quantity = data['quantity']
        pictures = data['pictures']

        product = Product.query.get(product_id)

        if not product:
            return jsonify({'message' : "not found"}), 404

        product.id = product_id
        product.name = name
        product.description = description
        product.price = price
        product.quantity = quantity

        # remove old pictures and then add new
        for picture in product.pictures:
            db.session.delete(product)

        db.session.commit()

        for picture in pictures:
            imgdata = base64.b64decode(picture.split(',')[1])
            filename = save_picture(img=imgdata, folder="product_picture")

            product_picture = ProductPicture(product_id=product.id,
                                            picture=filename)
            db.session.add(product_picture)

        db.session.commit()

    except:
        return jsonify({"message": "error"}), 403

    output = {}
    output['id'] = product.id

    return jsonify(output, {"message": "success"}), 200



@api.route("/api/get/product/<int:product_id>", methods=["GET"])
def api_get_product(product_id):
    """
    Get single products
    """
    product = Product.query.get(product_id)

    output = {}

    if not product:
        # if no product found with that user id
        return jsonify(output, {"message": "Not found"}), 404

    output = {}
    output['id'] = product.id
    output['name'] = product.name
    output['description'] = product.description
    output['price'] = float(product.price)
    output['quantity'] = product.quantity
    output['post_date'] = product.post_date
    output['last_modified'] = product.last_modified

    # add pictures and comments to output
    pictures = []
    comments = []

    for picture in product.pictures:
        picture_dict = {}
        picture_dict['id'] = picture.id
        picture_dict['picture'] = picture.picture
        pictures.append(picture_dict)

    for comment in product.comments:
        comment_dict = {}
        comment_dict['id'] = comment.id
        comment_dict['author'] = comment.comment_author
        comment_dict['content'] = comment.comment_content
        comment_dict['date'] = comment.comment_date
        pictures.append(comment_dict)

    # now add these to output dict
    output['pictures'] = pictures
    output['comments'] = comments

    return jsonify(output, {"message": "success"}), 200


@api.route("/api/get/products", methods=["GET"])
def api_get_products():
    """
    Get all products, pagination available
    Example : /api/get/products?per_page=20&page=2
    """
    try:
        per_page = int(request.args.get('per_page'))
        page = int(request.args.get('page'))
    except:
        per_page = 20
        page = 1

    products = Product.query.all()
    total_product = len(products)

    products = Product.query.order_by(Product.last_modified.desc()).paginate(page=page, per_page=per_page)

    outputs = []

    for product in products.items:
        output = {}
        output['id'] = product.id
        output['name'] = product.name
        output['description'] = product.description
        output['price'] = float(product.price)
        output['quantity'] = product.quantity
        output['post_date'] = product.post_date
        output['last_modified'] = product.last_modified

        # add pictures and comments to output
        pictures = []
        comments = []

        for picture in product.pictures:
            picture_dict = {}
            picture_dict['id'] = picture.id
            picture_dict['picture'] = picture.picture
            pictures.append(picture_dict)

        for comment in product.comments:
            comment_dict = {}
            comment_dict['id'] = comment.id
            comment_dict['author'] = comment.comment_author
            comment_dict['content'] = comment.comment_content
            comment_dict['date'] = comment.comment_date
            pictures.append(comment_dict)

        # now add these to output dict
        output['pictures'] = pictures
        output['comments'] = comments

        outputs.append(output)

    return jsonify(outputs, {"message" : "success", "total": total_product})

@api.route("/api/delete/product/<int:product_id>", methods=["DELETE"])
def api_delete_product(product_id):
    product = Product.query.get(product_id)

    if not product:
        # if no product found with that user id
        return jsonify({"message": "not found"}), 404

    # first delete comments of this product
    for comment in product.comments:
        db.session.delete(comment)

    # now delete all pictures of this product
    for picture in product.pictures:
        db.session.delete(picture)

    db.session.delete(product)
    db.session.commit()

    return jsonify({"message" : "success"}), 200

