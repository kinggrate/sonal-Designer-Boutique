from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask import session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/dev/sonal/orders.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'sonal_designer_boutique_secret_key_2025'
db = SQLAlchemy(app)

# Fixed credentials
VALID_USERNAME = 'sonaldesignerboutique'
VALID_PASSWORD = 'Shilpa@1430'

# Database Model
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

    # Blouse
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

    # Pant
    pant_waist = db.Column(db.Float)
    pant_length = db.Column(db.Float)
    thigh = db.Column(db.Float)
    knee = db.Column(db.Float)
    bottom = db.Column(db.Float)
    hip = db.Column(db.Float)

    # Dress
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

    # Meta
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

        # Blouse
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

        # Pant
        'pant_waist': self.pant_waist,
        'pant_length': self.pant_length,
        'thigh': self.thigh,
        'knee': self.knee,
        'bottom': self.bottom,
        'hip': self.hip,

        # Dress
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


# Routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == VALID_USERNAME and password == VALID_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Invalid username or password')
    
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

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/api/customers', methods=['GET'])
@login_required
def get_customers():
    customers = Customer.query.all()
    return jsonify([
        {
            **customer.to_dict(),
            'measurements': [m.to_dict() for m in customer.measurements]
        }
        for customer in customers
    ])

@app.route('/api/customers', methods=['POST'])
@login_required
def add_customer():
    data = request.form  # or request.get_json() if you're using JSON
    customer = Customer(
        customer_name=data['customer_name'],
        phone_number=data['phone_number']
    )
    db.session.add(customer)
    db.session.commit()
    return jsonify({'message': 'Customer added', 'customer_id': customer.id}), 201

@app.route('/api/measurements', methods=['POST'])
@login_required
def add_measurement():
    data = request.form  # or request.get_json()
    garment_type = data['garment_type']

    measurement = Measurement(
        customer_id=data['customer_id'],
        garment_type=garment_type,
        delivery_date=data['delivery_date'],
        additional_notes=data.get('additional_notes')
    )

    if garment_type == 'blouse':
        measurement.shoulder = data.get('shoulder')
        measurement.chest = data.get('chest')
        measurement.waist = data.get('waist')
        measurement.bust = data.get('bust')
        measurement.bust_point = data.get('bust_point')
        measurement.bust_to_bust = data.get('bust_to_bust')
        measurement.sleeves = data.get('sleeves')
        measurement.penalty_crease = data.get('penalty_crease')
        measurement.back_neck = data.get('back_neck')
        measurement.front_neck = data.get('front_neck')
        measurement.length = data.get('length')
        measurement.lower_chest = data.get('lower_chest')
        measurement.neck_round = data.get('neck_round')

    elif garment_type == 'pant':
        measurement.pant_waist = data.get('pant_waist')
        measurement.pant_length = data.get('pant_length')
        measurement.thigh = data.get('thigh')
        measurement.knee = data.get('knee')
        measurement.bottom = data.get('bottom')
        measurement.hip = data.get('hip')

    elif garment_type == 'dress':
        measurement.dress_shoulder = data.get('dress_shoulder')
        measurement.dress_chest = data.get('dress_chest')
        measurement.dress_waist = data.get('dress_waist')
        measurement.dress_hip = data.get('dress_hip')
        measurement.dress_length = data.get('dress_length')
        measurement.arm_whole_round = data.get('arm_whole_round')
        measurement.dress_sleeves = data.get('dress_sleeves')
        measurement.penalty_circle = data.get('penalty_circle')
        measurement.dress_front_neck = data.get('dress_front_neck')
        measurement.dress_back_neck = data.get('dress_back_neck')
        measurement.matha_round = data.get('matha_round')

    db.session.add(measurement)
    db.session.commit()
    return jsonify({'message': f'{garment_type.capitalize()} measurement added'}), 201


@app.route('/api/customers/<int:customer_id>', methods=['PUT'])
@login_required
def update_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    data = request.json

    if data['customer_name'] != customer.customer_name:
        existing_customer = Customer.query.filter_by(customer_name=data['customer_name']).first()
        if existing_customer:
            return jsonify({'error': 'Customer with this name already exists'}), 400

    customer.customer_name = data['customer_name']
    customer.phone_number = data['phone_number']
    db.session.commit()
    return jsonify({'message': 'Customer updated successfully'})

@app.route('/api/measurements/<int:measurement_id>', methods=['PUT'])
@login_required
def update_measurement(measurement_id):
    measurement = Measurement.query.get_or_404(measurement_id)
    data = request.json
    garment_type = measurement.garment_type

    measurement.delivery_date = data['delivery_date']
    measurement.additional_notes = data.get('additional_notes')

    if garment_type == 'blouse':
        measurement.shoulder = data.get('shoulder')
        measurement.chest = data.get('chest')
        measurement.waist = data.get('waist')
        measurement.bust = data.get('bust')
        measurement.bust_point = data.get('bust_point')
        measurement.bust_to_bust = data.get('bust_to_bust')
        measurement.sleeves = data.get('sleeves')
        measurement.penalty_crease = data.get('penalty_crease')
        measurement.back_neck = data.get('back_neck')
        measurement.front_neck = data.get('front_neck')
        measurement.length = data.get('length')
        measurement.lower_chest = data.get('lower_chest')
        measurement.neck_round = data.get('neck_round')

    elif garment_type == 'pant':
        measurement.pant_waist = data.get('pant_waist')
        measurement.pant_length = data.get('pant_length')
        measurement.thigh = data.get('thigh')
        measurement.knee = data.get('knee')
        measurement.bottom = data.get('bottom')
        measurement.hip = data.get('hip')

    elif garment_type == 'dress':
        measurement.dress_shoulder = data.get('dress_shoulder')
        measurement.dress_chest = data.get('dress_chest')
        measurement.dress_waist = data.get('dress_waist')
        measurement.dress_hip = data.get('dress_hip')
        measurement.dress_length = data.get('dress_length')
        measurement.arm_whole_round = data.get('arm_whole_round')
        measurement.dress_sleeves = data.get('dress_sleeves')
        measurement.penalty_circle = data.get('penalty_circle')
        measurement.dress_front_neck = data.get('dress_front_neck')
        measurement.dress_back_neck = data.get('dress_back_neck')
        measurement.matha_round = data.get('matha_round')

    db.session.commit()
    return jsonify({'message': f'{garment_type.capitalize()} measurement updated'})

@app.route('/api/customers/<int:customer_id>', methods=['DELETE'])
@login_required
def delete_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    db.session.delete(customer)
    db.session.commit()
    return jsonify({'message': 'Customer deleted successfully'})

@app.route('/api/customers/search')
@login_required
def search_customers():
    query = request.args.get('q', '')
    if query:
        customers = Customer.query.filter(
            (Customer.customer_name.contains(query)) | 
            (Customer.phone_number.contains(query))
        ).all()
    else:
        customers = Customer.query.all()
    
    return jsonify([customer.to_dict() for customer in customers])

# if __name__ == '__main__':
#     with app.app_context():
#         db.create_all()
#     app.run(debug=True, host='0.0.0.0', port=5000)
 # Main execution
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
