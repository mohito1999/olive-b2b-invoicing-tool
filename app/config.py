from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import openai
import os
from dotenv import load_dotenv

load_dotenv()

# PostgreSQL Database URL
DATABASE_URL = "postgresql://mohitmotwani:admin123@localhost/olive_b2b_invoicing_db"

# Create SQLAlchemy engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base model class for defining tables
Base = declarative_base()

# Azure OpenAI Configuration
openai.api_type = "azure"
openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")  # Azure endpoint
openai.api_version = os.getenv("AZURE_OPENAI_API_VERSION")  # API version
openai.api_key = os.getenv("OPENAI_API_KEY")  # API key
