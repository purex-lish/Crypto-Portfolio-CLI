# import logging

# # Configure logging
# logging.basicConfig(
#     level=logging.DEBUG,  # Set to DEBUG for detailed logs
#     format='%(asctime)s - %(levelname)s - %(message)s',
#     handlers=[
#         logging.FileHandler("debug.log"),  # Log to a file
#         logging.StreamHandler()  # Also log to console
#     ]
# )
import logging
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from lib.db.database import DATABASE_URL  # Adjust import based on your structure

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,  # Set to DEBUG for detailed logs
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("debug.log"),  # Log to a file
        logging.StreamHandler()  # Also log to console
    ]
)

def check_database_connection():
    """Check if the database connection is working."""
    try:
        engine = create_engine(DATABASE_URL)
        SessionLocal = sessionmaker(bind=engine)
        session = SessionLocal()
        
        # Execute a simple query to test the connection
        session.execute('SELECT 1')
        session.close()
        logging.info("Database connection successful.")
        print("Database connection successful.")
        
    except Exception as e:
        logging.error("Database connection failed.", exc_info=e)
        print("Database connection failed:", e)

def log_exception(exc):
    """Log an exception with traceback."""
    logging.error("An error occurred", exc_info=exc)

def debug_session(session):
    """Print session state for debugging."""
    print(f"Session ID: {id(session)}")
    print(f"Pending objects: {session.dirty}")
    print(f"New objects: {session.new}")

def check_config(config):
    """Check if the required config values are set."""
    required_keys = ['DATABASE_URL', 'API_KEY']
    for key in required_keys:
        if key not in config:
            logging.warning(f"Missing configuration key: {key}")
