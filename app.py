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
app.config['JWT_SECRET_KEY'] = "starz#"
app.config['JWT_ACCESS_TOKEN_EXPIRES'] =timedelta(days=365)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:starz@localhost/Civil'
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

@app.route('/machinery', methods=['GET'])
def get_machinery():
    # Query the labour column
    machinery_data = db.session.query(options.machinery).all()
    # Convert tuples to a list of strings
    machinery_list = [machinery[0] for machinery in machinery_data]
    # Return as JSON
    print(machinery_list)
    return jsonify({'machinery': machinery_list})


@app.route('/add-machinery', methods=['POST'])
def add_machinery():
    data = request.get_json()
    
    # Validate the incoming data
    if not data or 'machinery' not in data:
        return jsonify({"error": "Missing 'machinery' field in request data"}), 400  # Include 'error' keyword
    
    machinery_type = data['machinery']
    
    try:
        # Ensure labour_type is unique (example query, adjust for your DB structure)
        existing_machinery = db.session.query(options).filter_by(machinery=machinery_type).first()
        if existing_machinery:
            return jsonify({"error": "Machinery type already exists."}), 400  # Prevent duplicate additions

        # Add new labour type
        new_machinery = options(labour='', machinery=machinery_type, material='')  # Default values for machinery and material
        db.session.add(new_machinery)
        db.session.commit()
        
        return jsonify({"success": True, "message": "Machinery added successfully!", "machinery": machinery_type}), 201  # Include 'success' keyword
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to add machinery. " + str(e)}), 500  # Include 'error' keyword
    

@app.route('/material', methods=['GET'])
def get_material():
    # Query the labour column
    material_data = db.session.query(options.material).all()
    # Convert tuples to a list of strings
    material_list = [material[0] for material in material_data]
    # Return as JSON
    print(material_list)
    return jsonify({'material': material_list})


@app.route('/add-material', methods=['POST'])
def add_material():
    data = request.get_json()
    
    # Validate the incoming data
    if not data or 'material' not in data:
        return jsonify({"error": "Missing 'material' field in request data"}), 400  # Include 'error' keyword
    
    material_type = data['material']
    
    try:
        # Ensure labour_type is unique (example query, adjust for your DB structure)
        existing_material = db.session.query(options).filter_by(material=material_type).first()
        if existing_material:
            return jsonify({"error": "Material type already exists."}), 400  # Prevent duplicate additions

        # Add new labour type
        new_material = options(labour='', machinery='', material=material_type)  # Default values for machinery and material
        db.session.add(new_material)
        db.session.commit()
        
        return jsonify({"success": True, "message": "Material added successfully!", "material": material_type}), 201  # Include 'success' keyword
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to add material. " + str(e)}), 500  # Include 'error' keyword




@app.route('/submit_project', methods=['POST'])
def submit_project():
    data = request.json
    project_name = data.get('projectname')
    estimated_amount = data.get('estimated_amount', 0)  # Fixed name
    payments = data.get('rows', [])  # Fixed from 'payments' to 'rows'

    # Check if project already exists
    existing_project = projects.query.filter_by(projectname=project_name).first()

    if not existing_project:
        # Insert project into `projects` table
        new_project = projects(projectname=project_name, quotedamount=estimated_amount, totexpense=0)
        db.session.add(new_project)
        db.session.commit()  # Commit immediately to avoid foreign key issues

    # Insert into `payments1`
    for payment in payments:
        new_payment = payments1(
            projectname=project_name,
            type=payment.get('type'),
            estamount=payment.get('estamount'),
            expense=payment.get('expense', 0)
        )
        db.session.add(new_payment)

    db.session.commit()  # Commit all payments

    return jsonify({"message": "Project and payments added successfully"}), 200




if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port=5000)