from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask import session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Use relative path for better portability
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///orders.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'sonal_designer_boutique_secret_key_2025'

db = SQLAlchemy(app)

# Fixed credentials
VALID_USERNAME = 'sonaldesignerboutique'
VALID_PASSWORD = 'Shilpa@1430'

# Database Models
class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    measurements = db.relationship('Measurement', backref='customer', lazy=True, cascade="all, delete-orphan")
    
    def to_dict(self):
        return {
            'id': self.id,
            'customer_name': self.customer_name,
            'phone_number': self.phone_number
        }

class Measurement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    garment_type = db.Column(db.String(20), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    
    # Blouse measurements
    shoulder = db.Column(db.Float)
    chest = db.Column(db.Float)
    waist = db.Column(db.Float)
    bust = db.Column(db.Float)
    bust_point = db.Column(db.Float)
    bust_to_bust = db.Column(db.Float)
    sleeves = db.Column(db.Float)
    penalty_crease = db.Column(db.Float)
    back_neck = db.Column(db.Float)
    front_neck = db.Column(db.Float)
    length = db.Column(db.Float)
    lower_chest = db.Column(db.Float)
    neck_round = db.Column(db.Float)
    
    # Pant measurements
    pant_waist = db.Column(db.Float)
    pant_length = db.Column(db.Float)
    thigh = db.Column(db.Float)
    knee = db.Column(db.Float)
    bottom = db.Column(db.Float)
    hip = db.Column(db.Float)
    
    # Dress measurements
    dress_shoulder = db.Column(db.Float)
    dress_chest = db.Column(db.Float)
    dress_waist = db.Column(db.Float)
    dress_hip = db.Column(db.Float)
    dress_length = db.Column(db.Float)
    arm_whole_round = db.Column(db.Float)
    dress_sleeves = db.Column(db.Float)
    penalty_circle = db.Column(db.Float)
    dress_front_neck = db.Column(db.Float)
    dress_back_neck = db.Column(db.Float)
    matha_round = db.Column(db.Float)
    
    # Meta fields
    additional_notes = db.Column(db.Text)
    delivery_date = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'customer_id': self.customer_id,
            'garment_type': self.garment_type,
            'delivery_date': self.delivery_date,
            'additional_notes': self.additional_notes,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            # Blouse fields
            'shoulder': self.shoulder,
            'chest': self.chest,
            'waist': self.waist,
            'bust': self.bust,
            'bust_point': self.bust_point,
            'bust_to_bust': self.bust_to_bust,
            'sleeves': self.sleeves,
            'penalty_crease': self.penalty_crease,
            'back_neck': self.back_neck,
            'front_neck': self.front_neck,
            'length': self.length,
            'lower_chest': self.lower_chest,
            'neck_round': self.neck_round,
            # Pant fields
            'pant_waist': self.pant_waist,
            'pant_length': self.pant_length,
            'thigh': self.thigh,
            'knee': self.knee,
            'bottom': self.bottom,
            'hip': self.hip,
            # Dress fields
            'dress_shoulder': self.dress_shoulder,
            'dress_chest': self.dress_chest,
            'dress_waist': self.dress_waist,
            'dress_hip': self.dress_hip,
            'dress_length': self.dress_length,
            'arm_whole_round': self.arm_whole_round,
            'dress_sleeves': self.dress_sleeves,
            'penalty_circle': self.penalty_circle,
            'dress_front_neck': self.dress_front_neck,
            'dress_back_neck': self.dress_back_neck,
            'matha_round': self.matha_round
        }

# Authentication routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == VALID_USERNAME and password == VALID_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error="Invalid username or password")
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

def login_required(f):
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

# Main routes
@app.route('/')
@login_required
def index():
    return render_template('index.html')

# FIXED: Customer API routes with proper error handling
@app.route('/api/customers', methods=['GET', 'POST'])
@login_required
def customers():
    try:
        if request.method == 'GET':
            customers = Customer.query.all()
            return jsonify([{
                **customer.to_dict(),
                'measurements': [m.to_dict() for m in customer.measurements]
            } for customer in customers])
        
        elif request.method == 'POST':
            # Handle both JSON and form data
            if request.is_json:
                data = request.get_json()
            else:
                data = request.form.to_dict()
            
            # Validate required fields
            if not data.get('customer_name') or not data.get('phone_number'):
                return jsonify({'error': 'Customer name and phone number are required'}), 400
            
            # Create customer
            customer = Customer(
                customer_name=data['customer_name'],
                phone_number=data['phone_number']
            )
            
            db.session.add(customer)
            db.session.flush()  # Get customer.id before commit
            
            # Handle measurements if provided
            measurements_data = data.get('measurements', [])
            if measurements_data:
                for m in measurements_data:
                    measurement = Measurement(
                        customer_id=customer.id,
                        garment_type=m.get('garment_type', 'blouse'),
                        delivery_date=m.get('delivery_date', ''),
                        additional_notes=m.get('additional_notes', '')
                    )
                    
                    # Helper function to safely convert to float
                    def safe_float(value):
                        if value in [None, '']:
                            return None
                        try:
                            return float(value)
                        except (ValueError, TypeError):
                            return None
                    
                    # Set measurements based on garment type
                    garment_type = m.get('garment_type', 'blouse')
                    
                    if garment_type == 'blouse':
                        measurement.shoulder = safe_float(m.get('shoulder'))
                        measurement.chest = safe_float(m.get('chest'))
                        measurement.waist = safe_float(m.get('waist'))
                        measurement.bust = safe_float(m.get('bust'))
                        measurement.bust_point = safe_float(m.get('bust_point'))
                        measurement.bust_to_bust = safe_float(m.get('bust_to_bust'))
                        measurement.sleeves = safe_float(m.get('sleeves'))
                        measurement.penalty_crease = safe_float(m.get('penalty_crease'))
                        measurement.back_neck = safe_float(m.get('back_neck'))
                        measurement.front_neck = safe_float(m.get('front_neck'))
                        measurement.length = safe_float(m.get('length'))
                        measurement.lower_chest = safe_float(m.get('lower_chest'))
                        measurement.neck_round = safe_float(m.get('neck_round'))
                        
                    elif garment_type == 'pant':
                        measurement.pant_waist = safe_float(m.get('pant_waist'))
                        measurement.pant_length = safe_float(m.get('pant_length'))
                        measurement.thigh = safe_float(m.get('thigh'))
                        measurement.knee = safe_float(m.get('knee'))
                        measurement.bottom = safe_float(m.get('bottom'))
                        measurement.hip = safe_float(m.get('hip'))
                        
                    elif garment_type == 'dress':
                        measurement.dress_shoulder = safe_float(m.get('dress_shoulder'))
                        measurement.dress_chest = safe_float(m.get('dress_chest'))
                        measurement.dress_waist = safe_float(m.get('dress_waist'))
                        measurement.dress_hip = safe_float(m.get('dress_hip'))
                        measurement.dress_length = safe_float(m.get('dress_length'))
                        measurement.arm_whole_round = safe_float(m.get('arm_whole_round'))
                        measurement.dress_sleeves = safe_float(m.get('dress_sleeves'))
                        measurement.penalty_circle = safe_float(m.get('penalty_circle'))
                        measurement.dress_front_neck = safe_float(m.get('dress_front_neck'))
                        measurement.dress_back_neck = safe_float(m.get('dress_back_neck'))
                        measurement.matha_round = safe_float(m.get('matha_round'))
                    
                    db.session.add(measurement)
            
            db.session.commit()
            return jsonify({'message': 'Customer and measurements added successfully', 'customer_id': customer.id}), 201
            
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Database error: {str(e)}'}), 500

# FIXED: Separate measurement endpoint
@app.route('/api/measurements', methods=['POST'])
@login_required
def add_measurement():
    try:
        # Handle both JSON and form data
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form.to_dict()
        
        # Validate required fields
        customer_id = data.get('customer_id')
        garment_type = data.get('garment_type')
        delivery_date = data.get('delivery_date')
        
        if not customer_id or not garment_type or not delivery_date:
            return jsonify({'error': 'customer_id, garment_type, and delivery_date are required'}), 400
        
        # Check if customer exists
        customer = Customer.query.get(customer_id)
        if not customer:
            return jsonify({'error': 'Customer not found'}), 404
        
        measurement = Measurement(
            customer_id=customer_id,
            garment_type=garment_type,
            delivery_date=delivery_date,
            additional_notes=data.get('additional_notes', '')
        )
        
        # Helper function to safely convert to float
        def safe_float(value):
            if value in [None, '']:
                return None
            try:
                return float(value)
            except (ValueError, TypeError):
                return None
        
        # Set measurements based on garment type
        if garment_type == 'blouse':
            measurement.shoulder = safe_float(data.get('shoulder'))
            measurement.chest = safe_float(data.get('chest'))
            measurement.waist = safe_float(data.get('waist'))
            measurement.bust = safe_float(data.get('bust'))
            measurement.bust_point = safe_float(data.get('bust_point'))
            measurement.bust_to_bust = safe_float(data.get('bust_to_bust'))
            measurement.sleeves = safe_float(data.get('sleeves'))
            measurement.penalty_crease = safe_float(data.get('penalty_crease'))
            measurement.back_neck = safe_float(data.get('back_neck'))
            measurement.front_neck = safe_float(data.get('front_neck'))
            measurement.length = safe_float(data.get('length'))
            measurement.lower_chest = safe_float(data.get('lower_chest'))
            measurement.neck_round = safe_float(data.get('neck_round'))
            
        elif garment_type == 'pant':
            measurement.pant_waist = safe_float(data.get('pant_waist'))
            measurement.pant_length = safe_float(data.get('pant_length'))
            measurement.thigh = safe_float(data.get('thigh'))
            measurement.knee = safe_float(data.get('knee'))
            measurement.bottom = safe_float(data.get('bottom'))
            measurement.hip = safe_float(data.get('hip'))
            
        elif garment_type == 'dress':
            measurement.dress_shoulder = safe_float(data.get('dress_shoulder'))
            measurement.dress_chest = safe_float(data.get('dress_chest'))
            measurement.dress_waist = safe_float(data.get('dress_waist'))
            measurement.dress_hip = safe_float(data.get('dress_hip'))
            measurement.dress_length = safe_float(data.get('dress_length'))
            measurement.arm_whole_round = safe_float(data.get('arm_whole_round'))
            measurement.dress_sleeves = safe_float(data.get('dress_sleeves'))
            measurement.penalty_circle = safe_float(data.get('penalty_circle'))
            measurement.dress_front_neck = safe_float(data.get('dress_front_neck'))
            measurement.dress_back_neck = safe_float(data.get('dress_back_neck'))
            measurement.matha_round = safe_float(data.get('matha_round'))
        
        db.session.add(measurement)
        db.session.commit()
        
        return jsonify({'message': f'{garment_type.capitalize()} measurement added successfully'}), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Database error: {str(e)}'}), 500

# Update routes
@app.route('/api/customers/<int:customer_id>', methods=['PUT'])
@login_required
def update_customer(customer_id):
    try:
        customer = Customer.query.get_or_404(customer_id)
        data = request.get_json()
        
        customer.customer_name = data.get('customer_name', customer.customer_name)
        customer.phone_number = data.get('phone_number', customer.phone_number)
        
        db.session.commit()
        return jsonify({'message': 'Customer updated successfully'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Database error: {str(e)}'}), 500

@app.route('/api/measurements/<int:measurement_id>', methods=['PUT'])
@login_required
def update_measurement(measurement_id):
    try:
        measurement = Measurement.query.get_or_404(measurement_id)
        data = request.get_json()
        
        # Update basic fields
        measurement.delivery_date = data.get('delivery_date', measurement.delivery_date)
        measurement.additional_notes = data.get('additional_notes', measurement.additional_notes)
        
        # Helper function to safely convert to float
        def safe_float(value):
            if value in [None, '']:
                return None
            try:
                return float(value)
            except (ValueError, TypeError):
                return None
        
        # Update measurements based on garment type
        garment_type = measurement.garment_type
        
        if garment_type == 'blouse':
            measurement.shoulder = safe_float(data.get('shoulder'))
            measurement.chest = safe_float(data.get('chest'))
            measurement.waist = safe_float(data.get('waist'))
            measurement.bust = safe_float(data.get('bust'))
            measurement.bust_point = safe_float(data.get('bust_point'))
            measurement.bust_to_bust = safe_float(data.get('bust_to_bust'))
            measurement.sleeves = safe_float(data.get('sleeves'))
            measurement.penalty_crease = safe_float(data.get('penalty_crease'))
            measurement.back_neck = safe_float(data.get('back_neck'))
            measurement.front_neck = safe_float(data.get('front_neck'))
            measurement.length = safe_float(data.get('length'))
            measurement.lower_chest = safe_float(data.get('lower_chest'))
            measurement.neck_round = safe_float(data.get('neck_round'))
            
        elif garment_type == 'pant':
            measurement.pant_waist = safe_float(data.get('pant_waist'))
            measurement.pant_length = safe_float(data.get('pant_length'))
            measurement.thigh = safe_float(data.get('thigh'))
            measurement.knee = safe_float(data.get('knee'))
            measurement.bottom = safe_float(data.get('bottom'))
            measurement.hip = safe_float(data.get('hip'))
            
        elif garment_type == 'dress':
            measurement.dress_shoulder = safe_float(data.get('dress_shoulder'))
            measurement.dress_chest = safe_float(data.get('dress_chest'))
            measurement.dress_waist = safe_float(data.get('dress_waist'))
            measurement.dress_hip = safe_float(data.get('dress_hip'))
            measurement.dress_length = safe_float(data.get('dress_length'))
            measurement.arm_whole_round = safe_float(data.get('arm_whole_round'))
            measurement.dress_sleeves = safe_float(data.get('dress_sleeves'))
            measurement.penalty_circle = safe_float(data.get('penalty_circle'))
            measurement.dress_front_neck = safe_float(data.get('dress_front_neck'))
            measurement.dress_back_neck = safe_float(data.get('dress_back_neck'))
            measurement.matha_round = safe_float(data.get('matha_round'))
        
        db.session.commit()
        return jsonify({'message': f'{garment_type.capitalize()} measurement updated successfully'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Database error: {str(e)}'}), 500

# Delete routes
@app.route('/api/customers/<int:customer_id>', methods=['DELETE'])
@login_required
def delete_customer(customer_id):
    try:
        customer = Customer.query.get_or_404(customer_id)
        db.session.delete(customer)
        db.session.commit()
        return jsonify({'message': 'Customer deleted successfully'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Database error: {str(e)}'}), 500

@app.route('/api/measurements/<int:measurement_id>', methods=['DELETE'])
@login_required
def delete_measurement(measurement_id):
    try:
        measurement = Measurement.query.get_or_404(measurement_id)
        db.session.delete(measurement)
        db.session.commit()
        return jsonify({'message': 'Measurement deleted successfully'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Database error: {str(e)}'}), 500

# Search route
@app.route('/api/customers/search')
@login_required
def search_customers():
    try:
        query = request.args.get('q', '')
        if query:
            customers = Customer.query.filter(
                (Customer.customer_name.contains(query)) |
                (Customer.phone_number.contains(query))
            ).all()
        else:
            customers = Customer.query.all()
        
        return jsonify([{
            **customer.to_dict(),
            'measurements': [m.to_dict() for m in customer.measurements]
        } for customer in customers])
        
    except Exception as e:
        return jsonify({'error': f'Search error: {str(e)}'}), 500

# Database initialization
@app.before_first_request
def create_tables():
    db.create_all()

if __name__ == '__main__':
    # Create tables if they don't exist
    with app.app_context():
        db.create_all()
    
    app.run(host='0.0.0.0', port=5000, debug=True)