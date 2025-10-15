import os
from app import app, db
from sqlalchemy import inspect

# Ensure app uses the local DB path you created
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///C:/dev/sonal/orders.db"

with app.app_context():
    db.create_all()
    path = os.path.abspath(app.config["SQLALCHEMY_DATABASE_URI"].replace("sqlite:///", ""))
    print("WROTE_DB_PATH:", path)
    print("EXISTS_AFTER_WRITE:", os.path.exists(path))
    if os.path.exists(path):
        print("SIZE_BYTES:", os.path.getsize(path))
    print("TABLES:", inspect(db.engine).get_table_names())
