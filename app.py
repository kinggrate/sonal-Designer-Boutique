from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///orders.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Model
class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False, unique=True)
    phone_number = db.Column(db.String(20), nullable=False)
    garment_type = db.Column(db.String(20), nullable=False, default='blouse')
    
    # Blouse fields
    shoulder = db.Column(db.String(20))
    chest = db.Column(db.String(20))
    bust = db.Column(db.String(20))
    waist = db.Column(db.String(20))
    bust_point = db.Column(db.String(20))
    bust_to_bust = db.Column(db.String(20))
    sleeves = db.Column(db.String(20))
    penalty_crease = db.Column(db.String(20))
    back_neck = db.Column(db.String(20))
    front_neck = db.Column(db.String(20))
    length = db.Column(db.String(20))
    lower_chest = db.Column(db.String(20))
    
    # Pant fields
    pant_waist = db.Column(db.String(20))
    heap = db.Column(db.String(20))
    pant_length = db.Column(db.String(20))
    thigh = db.Column(db.String(20))
    knee = db.Column(db.String(20))
    bottom = db.Column(db.String(20))
    
    # Dress fields
    dress_shoulder = db.Column(db.String(20))
    dress_chest = db.Column(db.String(20))
    dress_waist = db.Column(db.String(20))
    dress_heap = db.Column(db.String(20))
    dress_length = db.Column(db.String(20))
    arm_whole_round = db.Column(db.String(20))
    dress_sleeves = db.Column(db.String(20))
    penalty_circle = db.Column(db.String(20))
    dress_front_neck = db.Column(db.String(20))
    dress_back_neck = db.Column(db.String(20))
    matha_round = db.Column(db.String(20))
    
    additional_notes = db.Column(db.Text)
    delivery_date = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'customer_name': self.customer_name,
            'phone_number': self.phone_number,
            'garment_type': self.garment_type,
            
            # Blouse fields
            'shoulder': self.shoulder,
            'chest': self.chest,
            'bust': self.bust,
            'waist': self.waist,
            'bust_point': self.bust_point,
            'bust_to_bust': self.bust_to_bust,
            'sleeves': self.sleeves,
            'penalty_crease': self.penalty_crease,
            'back_neck': self.back_neck,
            'front_neck': self.front_neck,
            'length': self.length,
            'lower_chest': self.lower_chest,
            
            # Pant fields
            'pant_waist': self.pant_waist,
            'heap': self.heap,
            'pant_length': self.pant_length,
            'thigh': self.thigh,
            'knee': self.knee,
            'bottom': self.bottom,
            
            # Dress fields
            'dress_shoulder': self.dress_shoulder,
            'dress_chest': self.dress_chest,
            'dress_waist': self.dress_waist,
            'dress_heap': self.dress_heap,
            'dress_length': self.dress_length,
            'arm_whole_round': self.arm_whole_round,
            'dress_sleeves': self.dress_sleeves,
            'penalty_circle': self.penalty_circle,
            'dress_front_neck': self.dress_front_neck,
            'dress_back_neck': self.dress_back_neck,
            'matha_round': self.matha_round,
            
            'additional_notes': self.additional_notes,
            'delivery_date': self.delivery_date,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/customers', methods=['GET'])
def get_customers():
    customers = Customer.query.all()
    return jsonify([customer.to_dict() for customer in customers])

@app.route('/api/customers', methods=['POST'])
def add_customer():
    data = request.json
    
    # Check if customer already exists
    existing_customer = Customer.query.filter_by(customer_name=data['customer_name']).first()
    if existing_customer:
        return jsonify({'error': 'Customer with this name already exists'}), 400
    
    try:
        customer = Customer(
            customer_name=data['customer_name'],
            phone_number=data['phone_number'],
            garment_type=data['garment_type'],
            
            # Blouse fields
            shoulder=data.get('shoulder', ''),
            chest=data.get('chest', ''),
            bust=data.get('bust', ''),
            waist=data.get('waist', ''),
            bust_point=data.get('bust_point', ''),
            bust_to_bust=data.get('bust_to_bust', ''),
            sleeves=data.get('sleeves', ''),
            penalty_crease=data.get('penalty_crease', ''),
            back_neck=data.get('back_neck', ''),
            front_neck=data.get('front_neck', ''),
            length=data.get('length', ''),
            lower_chest=data.get('lower_chest', ''),
            
            # Pant fields
            pant_waist=data.get('pant_waist', ''),
            heap=data.get('heap', ''),
            pant_length=data.get('pant_length', ''),
            thigh=data.get('thigh', ''),
            knee=data.get('knee', ''),
            bottom=data.get('bottom', ''),
            
            # Dress fields
            dress_shoulder=data.get('dress_shoulder', ''),
            dress_chest=data.get('dress_chest', ''),
            dress_waist=data.get('dress_waist', ''),
            dress_heap=data.get('dress_heap', ''),
            dress_length=data.get('dress_length', ''),
            arm_whole_round=data.get('arm_whole_round', ''),
            dress_sleeves=data.get('dress_sleeves', ''),
            penalty_circle=data.get('penalty_circle', ''),
            dress_front_neck=data.get('dress_front_neck', ''),
            dress_back_neck=data.get('dress_back_neck', ''),
            matha_round=data.get('matha_round', ''),
            
            additional_notes=data.get('additional_notes', ''),
            delivery_date=data['delivery_date']
        )
        
        db.session.add(customer)
        db.session.commit()
        
        return jsonify(customer.to_dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/customers/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    data = request.json
    
    # Check if new name conflicts with existing customer (excluding current customer)
    if data['customer_name'] != customer.customer_name:
        existing_customer = Customer.query.filter_by(customer_name=data['customer_name']).first()
        if existing_customer:
            return jsonify({'error': 'Customer with this name already exists'}), 400
    
    try:
        customer.customer_name = data['customer_name']
        customer.phone_number = data['phone_number']
        customer.garment_type = data['garment_type']
        
        # Blouse fields
        customer.shoulder = data.get('shoulder', '')
        customer.chest = data.get('chest', '')
        customer.bust = data.get('bust', '')
        customer.waist = data.get('waist', '')
        customer.bust_point = data.get('bust_point', '')
        customer.bust_to_bust = data.get('bust_to_bust', '')
        customer.sleeves = data.get('sleeves', '')
        customer.penalty_crease = data.get('penalty_crease', '')
        customer.back_neck = data.get('back_neck', '')
        customer.front_neck = data.get('front_neck', '')
        customer.length = data.get('length', '')
        customer.lower_chest = data.get('lower_chest', '')
        
        # Pant fields
        customer.pant_waist = data.get('pant_waist', '')
        customer.heap = data.get('heap', '')
        customer.pant_length = data.get('pant_length', '')
        customer.thigh = data.get('thigh', '')
        customer.knee = data.get('knee', '')
        customer.bottom = data.get('bottom', '')
        
        # Dress fields
        customer.dress_shoulder = data.get('dress_shoulder', '')
        customer.dress_chest = data.get('dress_chest', '')
        customer.dress_waist = data.get('dress_waist', '')
        customer.dress_heap = data.get('dress_heap', '')
        customer.dress_length = data.get('dress_length', '')
        customer.arm_whole_round = data.get('arm_whole_round', '')
        customer.dress_sleeves = data.get('dress_sleeves', '')
        customer.penalty_circle = data.get('penalty_circle', '')
        customer.dress_front_neck = data.get('dress_front_neck', '')
        customer.dress_back_neck = data.get('dress_back_neck', '')
        customer.matha_round = data.get('matha_round', '')
        
        customer.additional_notes = data.get('additional_notes', '')
        customer.delivery_date = data['delivery_date']
        
        db.session.commit()
        
        return jsonify(customer.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/customers/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    db.session.delete(customer)
    db.session.commit()
    return jsonify({'message': 'Customer deleted successfully'})

@app.route('/api/customers/search')
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

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)