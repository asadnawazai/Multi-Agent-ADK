import os
import logging
from flask import Flask
from logging.handlers import RotatingFileHandler

def create_app():
    # Create and configure the app
    app = Flask(__name__)
    
    # Configure logging
    log_level = os.getenv('LOG_LEVEL', 'INFO')
    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        numeric_level = logging.INFO
    
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.mkdir('logs')
    
    # Configure file handler
    file_handler = RotatingFileHandler('logs/multiagent_system.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(numeric_level)
    
    # Configure stream handler for console output
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(numeric_level)
    
    # Apply configuration to app logger
    app.logger.addHandler(file_handler)
    app.logger.addHandler(stream_handler)
    app.logger.setLevel(numeric_level)
    
    # Configure root logger as well
    logging.basicConfig(
        level=numeric_level,
        handlers=[file_handler, stream_handler],
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Import routes Blueprint and register it with the app
    from app.routes import main_bp
    app.register_blueprint(main_bp)
    
    app.logger.info('Multiagent System started')
    return app
