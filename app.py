from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import date, datetime, timedelta  # Use this for datetime functionality
from sqlalchemy import func
from decimal import Decimal
from werkzeug.security import generate_password_hash, check_password_hash  # Import from werkzeug
from flask_cors import CORS
from sqlalchemy import or_
import joblib
import numpy as np
import pandas as pd
from sqlalchemy import func, case 

app = Flask(__name__)
CORS(app)  # This will allow all domains to access your Flask app
app.config['JWT_SECRET_KEY'] = "Jackdog02#"
app.config['JWT_ACCESS_TOKEN_EXPIRES'] =timedelta(days=365)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:Jackdog02#@localhost/Civil'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# Load the saved model
model = joblib.load("final_cost_prediction_model.pkl")

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
    projectname = db.Column(db.String(100), unique=True, primary_key=True)
    quotedamount = db.Column(db.BigInteger, nullable=False, default=0)
    totexpense = db.Column(db.BigInteger, nullable=False)
    startdate = db.Column(db.Date, nullable=False)  # Add this line
    duration = db.Column(db.Integer, nullable=False)  # Add this line

    def __init__(self, projectname, quotedamount, totexpense, startdate, duration):
        self.projectname = projectname
        self.quotedamount = quotedamount
        self.totexpense = totexpense
        self.startdate = startdate  # Add this line
        self.duration = duration  # Add this line


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
    start_date = data.get('start_date', datetime.today().strftime('%Y-%m-%d'))  # Use current date if not provided
    duration = data.get('duration', 0)  # Fixed name
    payments = data.get('rows', [])  # Fixed from 'payments' to 'rows'

    # Check if project already exists
    existing_project = projects.query.filter_by(projectname=project_name).first()

    if not existing_project:
        # Insert project into projects table
        new_project = projects(projectname=project_name, quotedamount=estimated_amount, totexpense=0,startdate=start_date,duration=duration)
        db.session.add(new_project)
        db.session.commit()  # Commit immediately to avoid foreign key issues

    # Insert into payments1
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

@app.route('/add_expense', methods=['POST'])
def add_expense():
    data = request.get_json()
    projectname = data.get('projectname')
    category_id = data.get('category_id')  # ID from category table
    expense_amount = data.get('expense')
    selected_type = data.get('type')  # Labour, Material, Machinery
    date = data.get('date', datetime.today().strftime('%Y-%m-%d'))  # Use current date if not provided

    if not projectname or not category_id or not expense_amount or not selected_type:
        return jsonify({"error": "Missing required fields"}), 400

    try:
        # Fetch the project and update total expense
        project = projects.query.filter_by(projectname=projectname).first()
        if not project:
            return jsonify({"error": "Project not found"}), 404

        project.totexpense += int(expense_amount)

        # Update the expense in payments1
        payment_entry = payments1.query.filter_by(projectname=projectname, type=selected_type).first()
        if payment_entry:
            payment_entry.expense += int(expense_amount)
        else:
            return jsonify({"error": "Payment entry not found for given project and type"}), 404

        # Insert new row into payments2
        new_payment = payments2(
            projectname=projectname,
            id=category_id,
            amount=int(expense_amount),
            date=datetime.strptime(date, '%Y-%m-%d')
        )
        db.session.add(new_payment)

        # Commit changes to the database
        db.session.commit()

        return jsonify({"message": "Expense added successfully"}), 200

    except Exception as e:
        db.session.rollback()  # Rollback in case of error
        return jsonify({"error": str(e)}), 500


@app.route('/get_project_payment_details', methods=['GET'])
def get_project_payment_details():
    projectname = request.args.get('projectname')
    selected_type = request.args.get('type')  # Labour, Material, Machinery

    if not projectname or not selected_type:
        return jsonify({"error": "Missing projectname or type"}), 400

    # Check if the project exists in payments1 for the given type
    project_exists = (
        db.session.query(payments1)
        .filter(payments1.projectname == projectname, payments1.type == selected_type)
        .first()
    )

    if not project_exists:
        return jsonify({"error": "add the quoted amount for selected typr"+selected_type}), 404

    # Fetch all category names and IDs where type matches
    results = (
        db.session.query(category.id.label('category_id'), category.name.label('category_name'))
        .filter(category.type == selected_type)
        .all()
    )

    if results:
        categories = [{"category_id": row.category_id, "category_name": row.category_name} for row in results]
        print(categories)
        return jsonify({
            "projectname": projectname,
            "categories": categories
        })
    else:
        return jsonify({"error": "No matching categories found"}), 404


@app.route('/search', methods=['GET'])
def search_projects():
    search_text = request.args.get('project_name', '').strip()

    if not search_text:
        return jsonify({"filtered_projects": []})  # Return empty list if no input

    try:
        # Query database for matching projects
        project_list = projects.query.filter(projects.projectname.ilike(f"%{search_text}%")).all()

        # Convert results to a list of dictionaries
        filtered_projects = [{"projectname": project.projectname} for project in project_list]

        return jsonify({"filtered_projects": filtered_projects})

    except Exception as e:
        print(f"Error in /search: {str(e)}")  # Log error to console
        return jsonify({"error": "Internal server error"}), 500  # Return a proper error response


@app.route('/projects', methods=['GET'])
def get_projects():
    projects_list = projects.query.all()
    projects_data = [
        {
            "projectname": proj.projectname,
            "quotedamount": proj.quotedamount,
            "totexpense": proj.totexpense
        }
        for proj in projects_list
    ]
    return jsonify({"projects": projects_data})


@app.route('/project-details', methods=['GET'])
def get_project_details():
    projectname = request.args.get('projectname')
    if not projectname:
        return jsonify({"error": "Missing projectname"}), 400

    project = projects.query.filter_by(projectname=projectname).first()
    if not project:
        return jsonify({"error": "Project not found"}), 404

    return jsonify({
        "projectname": project.projectname,
        "quotedamount": project.quotedamount,
        "totexpense": project.totexpense
    }), 200

@app.route('/employee-details', methods=['GET'])
def get_employee_details():
    projectname = request.args.get('projectname')
    if not projectname:
        return jsonify({"error": "Missing projectname"}), 400

    employee_data = (
        db.session.query(category.name, category.type, payments2.date, payments2.amount)
        .join(payments2, category.id == payments2.id)
        .filter(payments2.projectname == projectname)
        .all()
    )

    result = [
        {
            "name": row.name,
            "type": row.type,
            "date": row.date.strftime('%Y-%m-%d'),
            "amount": row.amount
        }
        for row in employee_data
    ]

    return jsonify(result), 200

@app.route('/category-details', methods=['GET'])
def get_category_details():
    projectname = request.args.get('projectname')
    if not projectname:
        return jsonify({"error": "Missing projectname"}), 400

    category_data = (
        db.session.query(payments1.type, payments1.estamount, payments1.expense, options.material)
       # .join(options, payments1.type == options.labour)
        .filter(payments1.projectname == projectname)
        .all()
    )

    result = [
        {
            "type": row.type,
            "estamount": row.estamount,
            "expense": row.expense,
           # "category": row.material
        }
        for row in category_data
    ]

    return jsonify(result), 200

@app.route('/get_categories', methods=['GET'])
def get_categories():
    selected_type = request.args.get('type')

    if not selected_type:
        return jsonify({"error": "Missing type parameter"}), 400

    try:
        # Fetch all categories where type matches
        results = category.query.filter_by(type=selected_type).all()

        if not results:
            return jsonify({"error": "No matching categories found"}), 404

        # Convert results to JSON format
        categories = [{"category_id": row.id, "category_name": row.name} for row in results]

        return jsonify({"categories": categories})

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500
    
@app.route('/get_projects_by_id', methods=['GET'])
def get_projects_by_id():
    user_id = request.args.get('id')  # Get ID from the request
    if not user_id:
        return jsonify({"error": "ID parameter is required"}), 400

    projects = db.session.query(
        payments2.projectname, payments2.date, payments2.amount
    ).filter_by(id=user_id).all()
    
    project_details = [{
        "project_name": proj[0],
        "date": proj[1],
        "expense": proj[2]  # Assuming 'amount' represents the expense
    } for proj in projects]

    return jsonify({"projects": project_details})


@app.route('/check-overrun', methods=['POST'])
def check_overrun():
    data = request.get_json()
    projectname = data.get('projectname')

    if not projectname:
        return jsonify({"error": "Missing projectname"}), 400

    try:
        # Fetch project details
        project = projects.query.filter_by(projectname=projectname).first()
        if not project:
            return jsonify({"error": "Project not found"}), 404

        # Calculate duration and cost per day
        days_passed = (datetime.today().date() - project.startdate).days
        days_passed = max(days_passed, 1)  # Prevent division by zero
        
        cost_per_day = project.totexpense / days_passed

        project_progress = (days_passed / max(project.duration, 1)) * 100

        # Fetch payments1 data for the project
        payments = payments1.query.filter_by(projectname=projectname).all()

        # Calculate labour, material, and machinery costs
        labour_cost = sum(p.expense for p in payments if p.type in ['Mason', 'Carpenter', 'Painter', 'Electrician', 'Plumber','Shuttering','Tiles Work','RR Mason'])
        material_cost = sum(p.expense for p in payments if p.type in ['Cement', 'Bricks', 'M Sand', 'Metal', 'Steel', 'Shuttering Materials', 'Wood','Hardwares','Paint Shop','Tiles','Tiles Paste','Electrical Materials','Plumbing Materials','Soling','RR Stones'])
        machinery_cost = sum(p.expense for p in payments if p.type in ['Excavator', 'Tipper', 'Tractor', 'Dozer', 'Roller', 'Water Tanker', 'Transport'])

        # Prepare input for the model
        input_values = np.array([[
            project.quotedamount,  # Quoted Budget
            labour_cost,            # Labour Cost
            material_cost,          # Material Cost
            machinery_cost,         # Machinery Cost
            project_progress,       # Project Progress (%)
            cost_per_day            # Cost Per Day
        ]])

        # Convert to DataFrame
        columns = ['Quoted Budget', 'Labor Cost', 'Material Cost', 'Machinery Cost', 'Project Progress (%)', 'Cost Per Day']
        input_df = pd.DataFrame(input_values, columns=columns)

        # Make prediction
        predicted_cost = model.predict(input_df)[0]

      # Check for overrun (Convert to Python bool explicitly)
        overrun = bool(predicted_cost > project.quotedamount)

        return jsonify({
            "overrun": overrun,  # Now it's a Python bool, avoiding serialization issues
            "predicted_cost": float(predicted_cost)  # Also ensure predicted cost is float
        })


    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port=5000)
