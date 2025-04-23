import logging
from typing import List, Dict, Any
from app.agents.base_agent import BaseAgent

logger = logging.getLogger(__name__)

class KnowledgeAgent(BaseAgent):
    """Agent specialized in answering fact-based questions across domains."""
    
    def __init__(self):
        super().__init__()
        self.agent_type = "knowledge"
    
    def process_query(self, query: str, history: List[Dict[str, Any]] = None) -> str:
        """Process a knowledge-based query and return factual information."""
        # Define a system message that emphasizes factual knowledge
        system_message = """You are a knowledge specialist with expertise across many domains. 
        Provide accurate, factual, and informative answers to questions about:
        - History and historical events
        - Science and scientific concepts
        - Geography and world facts
        - Arts and literature
        - Technology and innovations
        - Famous people and their accomplishments
        - Cultural information and traditions
        
        Base your answers on established facts. If there are multiple perspectives on a topic, 
        acknowledge them fairly. If you're unsure about something, be transparent about limitations 
        rather than providing potentially incorrect information. Cite sources or references when appropriate.
        """
        
        return self._generate_response(query, system_message, history)
