import os
import requests
import logging
from typing import List, Dict, Any
from app.agents.base_agent import BaseAgent

logger = logging.getLogger(__name__)

class WeatherAgent(BaseAgent):
    """Agent specialized in providing weather information."""
    
    def __init__(self):
        super().__init__()
        self.agent_type = "weather"
        self.api_key = os.getenv("WEATHER_API_KEY")
        self.weather_api_url = "https://api.openweathermap.org/data/2.5/weather"
        
    def _get_weather_data(self, location):
        """Fetch weather data for a given location using OpenWeatherMap API."""
        try:
            params = {
                "q": location,
                "appid": self.api_key,
                "units": "metric"  # Use metric units (Celsius)
            }
            
            response = requests.get(self.weather_api_url, params=params)
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Weather API error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Error fetching weather data: {str(e)}", exc_info=True)
            return None
    
    def _extract_location(self, query):
        """Extract location information from user query."""
        # Use GPT to extract location from user query
        system_message = """You are a location extractor. Extract the city or country name from the user's weather-related query. 
        Return ONLY the location name without any additional text or explanation. If no location is found, return 'Unknown'."""
        
        location = self._generate_response(query, system_message)
        return location if location.lower() != "unknown" else None
    
    def process_query(self, query: str, history: List[Dict[str, Any]] = None) -> str:
        """Process a weather-related query and return information."""
        # Extract location from the query
        location = self._extract_location(query)
        
        if not location:
            return "I couldn't determine which location you're asking about. Could you please specify a city or country?"
        
        # Fetch weather data
        weather_data = self._get_weather_data(location)
        
        if not weather_data:
            return f"I'm sorry, I couldn't retrieve weather information for {location}. Please check the location name and try again."
        
        # Generate a response based on the weather data
        system_message = f"""You are a weather information specialist. Provide helpful, accurate, and concise weather information based on the following data. 
        Be conversational but focus on the weather details.
        
        Weather data: {weather_data}
        """
        
        return self._generate_response(query, system_message, history)
