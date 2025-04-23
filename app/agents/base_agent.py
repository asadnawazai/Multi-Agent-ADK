import os
import openai
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class BaseAgent:
    """Base class for all agents in the system."""
    
    def __init__(self):
        # Initialize OpenAI API key
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.model = "gpt-4.1-mini"
        
    def _generate_response(self, prompt: str, system_message: str, history: List[Dict[str, Any]] = None) -> str:
        """Generate a response using the OpenAI API.
        
        Args:
            prompt: The user's input prompt
            system_message: The system message defining the agent's role
            history: Optional conversation history
            
        Returns:
            str: The generated response
        """
        try:
            messages = [{
                "role": "system",
                "content": system_message
            }]
            
            # Add relevant conversation history if provided
            if history:
                # Filter history to only include relevant exchanges for this agent type
                filtered_history = []
                for entry in history[-10:]:  # Only use last 10 messages for context
                    if entry["role"] in ["user", "assistant"]:
                        # Only include history entries for this specific agent or user messages
                        if entry["role"] == "user" or ("agent" in entry and entry["agent"] == self.agent_type):
                            filtered_history.append({
                                "role": entry["role"],
                                "content": entry["content"]
                            })
                
                messages.extend(filtered_history)
            
            # Add the current user prompt
            messages.append({
                "role": "user",
                "content": prompt
            })
            
            # Call the OpenAI API using v0.28 syntax
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=messages,
                max_tokens=1000,
                temperature=0.7
            )
            
            return response.choices[0].message["content"].strip()
            
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}", exc_info=True)
            return "I'm sorry, I encountered an error while processing your request. Please try again later."
    
    def process_query(self, query: str, history: List[Dict[str, Any]] = None) -> str:
        """Process a user query and return a response.
        
        This method should be overridden by subclasses.
        """
        raise NotImplementedError("Subclasses must implement process_query method.")
