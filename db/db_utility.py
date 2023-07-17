from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import Base

# Define the SQLite database URL
DATABASE_URL = 'sqlite:///db/project_planner.db'

# Create the database engine
engine = create_engine(DATABASE_URL)

# Create a session factory
Session = sessionmaker(bind=engine)


# Function to get a new session
def get_session():
    session = Session()
    Base.metadata.create_all(bind=engine)
    return session
