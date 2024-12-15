# inspect_db.py
from sqlalchemy import create_engine, inspect
from app.config import DATABASE_URL  # Adjust this import to your actual database URL

engine = create_engine(DATABASE_URL)
inspector = inspect(engine)

# List all tables
tables = inspector.get_table_names()
print("Tables in the database:", tables)

# Inspect each table
for table_name in tables:
    print(f"\nSchema for table {table_name}:")
    columns = inspector.get_columns(table_name)
    for column in columns:
        print(f"Column: {column['name']}, Type: {column['type']}, Nullable: {column['nullable']}")