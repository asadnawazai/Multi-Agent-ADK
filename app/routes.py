import os
import logging
from flask import Blueprint, render_template, request, jsonify
from app.agents.coordinator import Coordinator

logger = logging.getLogger(__name__)

# Create a Blueprint for our routes
main_bp = Blueprint('main', __name__)

# Initialize the coordinator agent
coordinator = Coordinator()

@main_bp.route('/')
def index():
    """Render the main chat interface."""
    return render_template('index.html')

@main_bp.route('/api/chat', methods=['POST'])
def chat():
    """API endpoint to process user queries and return responses."""
    data = request.get_json()
    
    if not data or 'message' not in data:
        return jsonify({
            'error': 'No message provided'
        }), 400
    
    user_message = data['message']
    
    # Process the message through the coordinator
    try:
        result = coordinator.process_query(user_message)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}", exc_info=True)
        return jsonify({
            'error': 'An error occurred while processing your request',
            'details': str(e)
        }), 500
