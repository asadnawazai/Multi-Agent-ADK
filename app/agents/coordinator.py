import logging
import json

# Import sub-agents
from app.agents.weather_agent import WeatherAgent
from app.agents.math_agent import MathAgent
from app.agents.knowledge_agent import KnowledgeAgent
from app.agents.assistant_agent import AssistantAgent

logger = logging.getLogger(__name__)

class Coordinator:
    """Parent agent that coordinates between specialized sub-agents."""
    
    def __init__(self):
        self.weather_agent = WeatherAgent()
        self.math_agent = MathAgent()
        self.knowledge_agent = KnowledgeAgent()
        self.assistant_agent = AssistantAgent()
        
        # Maintain conversation history
        self.conversation_history = []
        
    def _add_to_history(self, role, content, agent=None):
        """Add message to conversation history with metadata."""
        entry = {
            "role": role,
            "content": content
        }
        if agent:
            entry["agent"] = agent
        
        self.conversation_history.append(entry)
        
        # Limit history size
        if len(self.conversation_history) > 20:
            self.conversation_history = self.conversation_history[-20:]
    
    def _determine_agent(self, user_input):
        """Analyze user input to determine the most appropriate agent."""
        user_input = user_input.lower()
        
        # Check for weather-related keywords
        weather_keywords = ["weather", "temperature", "forecast", "rain", "sunny", "cloudy", "humidity", "wind", "climate"]
        if any(keyword in user_input for keyword in weather_keywords):
            return "weather"
            
        # Check for math-related keywords
        math_keywords = ["calculate", "solve", "equation", "math", "sum", "difference", "product", "quotient", 
                        "divided by", "multiplied by", "plus", "minus", "times", "square root", "percentage", "factorial"]
        math_symbols = ["+", "-", "*", "/", "^", "=", ">", "<", "≥", "≤", "√", "%"]
        
        if any(keyword in user_input for keyword in math_keywords) or any(symbol in user_input for symbol in math_symbols):
            return "math"
            
        # Check for knowledge-related keywords
        knowledge_keywords = ["who", "what", "when", "where", "why", "how", "explain", "define", "history", 
                            "information", "tell me about", "facts", "data"]
        if any(keyword in user_input for keyword in knowledge_keywords):
            return "knowledge"
            
        # Default to assistant agent for general queries
        return "assistant"
    
    def process_query(self, user_input):
        """Process user query by routing to appropriate agent."""
        if not user_input or user_input.strip() == "":
            return {
                "response": "I didn't receive any input. Please provide a question or request.",
                "agent": "coordinator"
            }
            
        # Add user message to history
        self._add_to_history("user", user_input)
        
        # Determine which agent should handle the query
        agent_type = self._determine_agent(user_input)
        logger.info(f"Routing query to {agent_type} agent")
        
        try:
            # Route to appropriate agent
            if agent_type == "weather":
                response = self.weather_agent.process_query(user_input, self.conversation_history)
                agent_name = "Weather Agent"
            elif agent_type == "math":
                response = self.math_agent.process_query(user_input, self.conversation_history)
                agent_name = "Mathematics Agent"
            elif agent_type == "knowledge":
                response = self.knowledge_agent.process_query(user_input, self.conversation_history)
                agent_name = "Knowledge Agent"
            else:
                response = self.assistant_agent.process_query(user_input, self.conversation_history)
                agent_name = "Assistant Agent"
                
            # Add agent response to history
            self._add_to_history("assistant", response, agent_type)
            
            return {
                "response": response,
                "agent": agent_name
            }
            
        except Exception as e:
            logger.error(f"Error processing query: {str(e)}", exc_info=True)
            return {
                "response": f"I encountered an error while processing your request. Please try again later.",
                "agent": "coordinator"
            }
