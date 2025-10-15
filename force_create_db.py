import os
from app import app, db
from sqlalchemy import inspect

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/opgam/OneDrive/Documents/GitHub/sonal-Designer-Boutique/orders.db'

with app.app_context():
    db.create_all()
    path = os.path.abspath(app.config['SQLALCHEMY_DATABASE_URI'].replace("sqlite:///", ""))
    print("CREATED_DB_PATH:", path)
    print("EXISTS_AFTER_CREATE:", os.path.exists(path))
    if os.path.exists(path):
        print("SIZE_BYTES:", os.path.getsize(path))
    inspector = inspect(db.engine)
    print("TABLES:", inspector.get_table_names())
