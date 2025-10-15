import os
from app import app, db

uri = app.config.get('SQLALCHEMY_DATABASE_URI')
print("SQLALCHEMY_DATABASE_URI:", uri)

if not uri:
    raise SystemExit("No URI found in app.config")

if uri.startswith("sqlite:///"):
    path = uri.replace("sqlite:///", "")
else:
    path = uri
abs_path = os.path.abspath(path)
print("Resolved absolute path:", abs_path)
print("Exists:", os.path.exists(abs_path))
if os.path.exists(abs_path):
    print("Size (bytes):", os.path.getsize(abs_path))

with app.app_context():
    db.create_all()
    try:
        tables = db.engine.table_names()
    except Exception as e:
        tables = f"ERROR: {e}"
    print("Tables visible to SQLAlchemy:", tables)
