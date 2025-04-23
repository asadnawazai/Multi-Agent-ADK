import logging
from typing import List, Dict, Any
import re
from app.agents.base_agent import BaseAgent

logger = logging.getLogger(__name__)

class MathAgent(BaseAgent):
    """Agent specialized in solving mathematical problems and calculations."""
    
    def __init__(self):
        super().__init__()
        self.agent_type = "math"
    
    def process_query(self, query: str, history: List[Dict[str, Any]] = None) -> str:
        """Process a mathematics-related query and return the solution."""
        # Define a system message that emphasizes mathematical expertise
        system_message = """You are a mathematics specialist. Solve mathematical problems, equations, and calculations accurately.
        Show your work step by step when appropriate. For complex problems, explain the methodology and reasoning.
        You can handle:
        - Arithmetic calculations
        - Algebraic equations
        - Geometry problems
        - Calculus problems
        - Statistics and probability
        - Number theory
        
        Be precise in your answers and include units where applicable. If the query isn't clear, ask for clarification.
        """
        
        # Check if the query contains a simple arithmetic calculation that can be directly computed
        basic_calculation = self._extract_basic_calculation(query)
        if basic_calculation:
            try:
                # Safely evaluate the expression
                result = eval(basic_calculation)
                # Generate a comprehensive response that includes the calculation
                context_query = f"The calculation {basic_calculation} = {result}. Please explain this result in the context of: {query}"
                return self._generate_response(context_query, system_message, history)
            except Exception as e:
                logger.debug(f"Could not evaluate expression: {basic_calculation}, error: {str(e)}")
                # Fall back to GPT for more complex expressions
                pass
        
        # For more complex mathematical queries, rely on GPT
        return self._generate_response(query, system_message, history)
    
    def _extract_basic_calculation(self, query):
        """Extract a basic arithmetic calculation from the query if present."""
        # Remove any text within parentheses that might confuse the regex
        cleaned_query = re.sub(r'\([^)]*\)', '', query)
        
        # Look for arithmetic expressions with common operators
        pattern = r'\d+\s*[+\-*/]\s*\d+(?:\s*[+\-*/]\s*\d+)*'
        matches = re.findall(pattern, cleaned_query)
        
        if matches:
            # Get the longest match (most complete expression)
            expression = max(matches, key=len)
            # Clean up the expression
            expression = re.sub(r'[^0-9+\-*/.]', '', expression)
            return expression
        
        return None
