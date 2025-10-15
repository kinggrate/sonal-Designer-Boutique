import os
from sqlalchemy import create_engine
from sqlalchemy import inspect
from app import db, app

# Use the absolute path we want
db_path = r"C:/dev/sonal/orders.db"
sqlite_uri = f"sqlite:///{db_path}"

# Ensure directory exists
os.makedirs(os.path.dirname(db_path), exist_ok=True)

# Create engine directly and bind metadata to it
engine = create_engine(sqlite_uri, echo=False)

with app.app_context():
    # bind metadata to engine and create tables on disk
    db.metadata.create_all(bind=engine)

# Check file and tables
print("DB_PATH:", os.path.abspath(db_path))
print("EXISTS:", os.path.exists(db_path))
if os.path.exists(db_path):
    print("SIZE_BYTES:", os.path.getsize(db_path))
inspector = inspect(engine)
print("TABLES:", inspector.get_table_names())
