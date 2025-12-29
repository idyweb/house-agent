from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from .base_model import Base
from api.config.settings import settings
from pgvector.psycopg import register_vector

# Get current environment
ENVIRONMENT = settings.environment

# Determine DATABASE_URL based on environment
if ENVIRONMENT == "development":
    DATABASE_URL = settings.database_url
elif ENVIRONMENT == "staging":
    DATABASE_URL = settings.staging_database_url
elif ENVIRONMENT == "production":
    DATABASE_URL = settings.production_database_url
else:
    DATABASE_URL = settings.database_url # Fallback to development URL or raise an error as needed

if not DATABASE_URL:
    raise ValueError(f"No database URL configured for environment: {ENVIRONMENT}")


engine = create_engine(DATABASE_URL)

@event.listens_for(engine, "connect")
def connect(dbapi_connection, connection_record):
    """Register the vector type on new database connections"""
    register_vector(dbapi_connection)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Creates a new database session for each request"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_environment():
    """Utility function to get current environment"""
    return settings.environment