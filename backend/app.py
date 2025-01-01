from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import date, datetime, timedelta  # Use this for datetime functionality
from sqlalchemy import func
from decimal import Decimal
from werkzeug.security import generate_password_hash, check_password_hash  # Import from werkzeug
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will allow all domains to access your Flask app
app.config['JWT_SECRET_KEY'] = "starz"
app.config['JWT_ACCESS_TOKEN_EXPIRES'] =timedelta(days=365)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:Jackdog02#@localhost/Civil'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True


db = SQLAlchemy(app)
jwt = JWTManager(app)

class options(db.Model):
    __tablename__ = 'options'
    sno = db.Column(db.Integer, primary_key=True, autoincrement=True)

    labour = db.Column(db.String(100),  nullable=False)
    machinery = db.Column(db.String(255), nullable=False)
    material = db.Column(db.String(255), nullable=False)
    


    def __init__(self,labour, material, machinery):
        self.labour=labour
        self.machinery = machinery
        self.material = material

class category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.String(15), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(255), nullable=False)


    def __init__(self,id, name, type):
        self.id=id
        self.name = name
        self.type = type

class projects(db.Model):
    __tablename__ = 'projects'
    projectname = db.Column(db.String(100),unique=True, primary_key=True)
    quotedamount = db.Column(db.BigInteger, nullable=False, default=0)
    totexpense = db.Column(db.BigInteger, nullable=False)


    def __init__(self,projectname, quotedamount, totexpense):
        self.projectname=projectname
        self.totexpense = totexpense
        self.quotedamount = quotedamount

class payments1(db.Model):
    __tablename__ = 'payments1'
    pid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    projectname = db.Column(db.String(100),db.ForeignKey('projects.projectname'))
    type = db.Column(db.String(100),nullable=False)
    estamount = db.Column(db.Integer, nullable=False)
    expense = db.Column(db.Integer, nullable=False)



    def __init__(self,projectname, estamount,type, expense):
        self.projectname=projectname
        self.expense = expense
        self.estamount = estamount
        self.type = type

class payments2(db.Model):
    __tablename__ = 'payments2'
    uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    projectname = db.Column(db.String(100),db.ForeignKey('projects.projectname'),nullable=False)
    id = db.Column(db.String(15), db.ForeignKey('category.id'),nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False)  

    def __init__(self,projectname, amount,id, date):
        self.projectname=projectname
        self.date = date
        self.amount = amount
        self.id = id

@app.route('/add-category', methods=['POST'])
def add_category():
    data = request.get_json()  
    if not data or 'name' not in data or 'type' not in data or 'id' not in data:
        return jsonify({"error": "Missing 'name' or 'type' in request data"}), 400
    id=data['id']
    name = data['name']
    type_ = data['type']

    try:
        new_category = category(name=name, type=type_,id=id)
        db.session.add(new_category)
        db.session.commit()
        return jsonify({"message": "Category added successfully!", "id": new_category.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500







if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port=5000)