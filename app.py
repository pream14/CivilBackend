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
app.config['JWT_SECRET_KEY'] = "Jackdog02#"
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
        return jsonify({"error": "Missing 'name', 'type', or 'id' in request data"}), 400  # Include 'error' keyword in the message
    
    id = data['id']
    name = data['name']
    type_ = data['type']

    try:
        new_category = category(name=name, type=type_, id=id)
        db.session.add(new_category)
        db.session.commit()
        return jsonify({"success": True, "message": "Category added successfully!", "id": new_category.id}), 201  # Include 'success' keyword
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to add category. " + str(e)}), 500  # Include 'error' keyword

@app.route('/labour', methods=['GET'])
def get_labour():
    # Query the labour column
    labour_data = db.session.query(options.labour).all()
    # Convert tuples to a list of strings
    labour_list = [labour[0] for labour in labour_data]
    # Return as JSON
    print(labour_list)
    return jsonify({'labour': labour_list})

@app.route('/add-labour', methods=['POST'])
def add_labour():
    data = request.get_json()
    
    # Validate the incoming data
    if not data or 'labour' not in data:
        return jsonify({"error": "Missing 'labour' field in request data"}), 400  # Include 'error' keyword
    
    labour_type = data['labour']
    
    try:
        # Ensure labour_type is unique (example query, adjust for your DB structure)
        existing_labour = db.session.query(options).filter_by(labour=labour_type).first()
        if existing_labour:
            return jsonify({"error": "Labour type already exists."}), 400  # Prevent duplicate additions

        # Add new labour type
        new_labour = options(labour=labour_type, machinery='', material='')  # Default values for machinery and material
        db.session.add(new_labour)
        db.session.commit()
        
        return jsonify({"success": True, "message": "Labour added successfully!", "labour": labour_type}), 201  # Include 'success' keyword
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to add labour. " + str(e)}), 500  # Include 'error' keyword

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port=5000)