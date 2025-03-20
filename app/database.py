import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

try:
    POSTGRES_USER = os.environ["POSTGRES_USER"]
    POSTGRES_PASSWORD = os.environ["POSTGRES_PASSWORD"]
    POSTGRES_DB = os.environ["POSTGRES_DB"]
    POSTGRES_HOST = os.environ["POSTGRES_HOST"]
    POSTGRES_PORT = os.environ["POSTGRES_PORT"]
except KeyError as e:
    raise EnvironmentError(f"Missing required environment variable: {e}")

# Get database URL from environment variable with fallback
# Construct from individual components if DATABASE_URL is not directly provided
DB_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
