import os
import logging
from dotenv import load_dotenv
from waitress import serve
from app import create_app

# Load environment variables from .env file
load_dotenv()

# Set up logging
log_level = os.getenv('LOG_LEVEL', 'INFO')
numeric_level = getattr(logging, log_level.upper(), None)
if not isinstance(numeric_level, int):
    numeric_level = logging.INFO

logging.basicConfig(
    level=numeric_level,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Configuration
HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', 5000))
DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() in ('true', '1', 't')

# Create the Flask application
app = create_app()

if __name__ == '__main__':
    logger.info(f"Starting server on {HOST}:{PORT}")
    if DEBUG:
        # Use Flask's built-in server for development
        logger.info("Running in development mode with Flask server")
        app.run(host=HOST, port=PORT, debug=DEBUG)
    else:
        # Use Waitress for production
        logger.info("Running in production mode with Waitress WSGI server")
        serve(app, host=HOST, port=PORT)
