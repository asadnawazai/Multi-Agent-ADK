import logging
from typing import List, Dict, Any
from app.agents.base_agent import BaseAgent

logger = logging.getLogger(__name__)

class AssistantAgent(BaseAgent):
    """Agent specialized in handling general requests and instructions."""
    
    def __init__(self):
        super().__init__()
        self.agent_type = "assistant"
    
    def process_query(self, query: str, history: List[Dict[str, Any]] = None) -> str:
        """Process general requests and provide helpful responses."""
        # Define a system message for general assistance
        system_message = """You are a helpful assistant designed to provide general assistance and engage in conversations.
        Be friendly, polite, and accommodating. Answer questions, provide advice, and assist with tasks to the best of your ability.
        If a request falls outside your capabilities, clearly explain what you can and cannot do.
        Always maintain a helpful and positive tone.
        """
        
        return self._generate_response(query, system_message, history)
