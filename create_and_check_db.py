import os
from app import app, db
from sqlalchemy import inspect

with app.app_context():
    db.create_all()
    uri = app.config.get("SQLALCHEMY_DATABASE_URI")
    if uri and uri.startswith("sqlite:///"):
        path = uri.replace("sqlite:///", "")
    else:
        path = uri or "UNKNOWN"
    abs_path = os.path.abspath(path)
    print("DB_ABS_PATH:", abs_path)
    print("EXISTS:", os.path.exists(abs_path))
    if os.path.exists(abs_path):
        print("SIZE_BYTES:", os.path.getsize(abs_path))
    inspector = inspect(db.engine)
    print("TABLES:", inspector.get_table_names())
