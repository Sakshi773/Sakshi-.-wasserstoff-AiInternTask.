import os
from sqlalchemy import create_engine
from dotenv import load_dotenv
from backend.db.models import Base
 

# Loading environment variables from .env
load_dotenv()
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB")

# Creating the database URL
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Creating a database engine
engine = create_engine(DATABASE_URL)

# This will create all tables if they dont exist
def init_db():
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("All tables created!")

# Run the function if this script is executed directly
if __name__ == "__main__":
    init_db()






# Connect to PostgreSQL
engine = create_engine(DATABASE_URL)

# Create tables
def create_tables():
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully.")

# If this script is run directly
if __name__ == "__main__":
    create_tables()

