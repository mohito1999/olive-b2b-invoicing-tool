from sqlalchemy import create_engine, MetaData, text
from sqlalchemy.orm import sessionmaker
from app.config import DATABASE_URL  # Ensure this import points to your actual database URL

# Create a database engine
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Reflect the database schema
metadata = MetaData()
metadata.reflect(bind=engine)

# Disable foreign key constraints
session.execute(text('SET session_replication_role = replica;'))

# Truncate all tables
for table in reversed(metadata.sorted_tables):
    session.execute(text(f'TRUNCATE TABLE {table.name} RESTART IDENTITY CASCADE;'))

# Re-enable foreign key constraints
session.execute(text('SET session_replication_role = DEFAULT;'))

# Commit the changes
session.commit()

# Close the session
session.close()