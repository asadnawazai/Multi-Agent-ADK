# Multi-Agent System with Hierarchical Structure

A comprehensive multi-agent system featuring a hierarchical structure with a coordinator (parent agent) and specialized sub-agents. The system provides a cohesive user experience through a Flask-based web interface.

## System Architecture

### Parent Agent (Coordinator)

The coordinator agent analyzes user prompts to determine the most appropriate sub-agent, routes queries accordingly, and handles response aggregation and presentation.

### Sub-Agents

1. **Weather Agent**: Provides real-time weather information for cities and countries
2. **Mathematics Agent**: Handles calculations, mathematical problems, and related queries
3. **General Knowledge Agent**: Answers fact-based questions across various domains
4. **Assistant Agent**: Handles general requests, instructions, and conversations

### Agent Communication Framework

The system implements a robust communication protocol between the parent agent and sub-agents, with context preservation for multi-turn conversations and metadata indicating which agent generated the content.

## Technical Implementation

- Utilizes GPT-4.1-mini API for all agents
- Flask-based web application with a clean, intuitive chat interface
- Visual indication of which agent is responding
- Responsive design for multiple devices
- Error handling and logging
- Structured codebase for maintainability and scalability

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- OpenAI API key (for GPT-4.1-mini)
- OpenWeatherMap API key (for Weather Agent)

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/asadnawazai/Multi-Agent-ADK.git
   cd Multi-Agent-ADK
   ```

2. Create and activate a virtual environment (optional but recommended):
   ```
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   - Copy the `.env.example` file to `.env`
   - Add your OpenAI API key and OpenWeatherMap API key to the `.env` file

### Running the Application

1. Start the Flask app:
   ```
   python app.py
   ```

2. Access the web interface at [http://localhost:5000](http://localhost:5000)

## Usage

1. Type your question or request in the chat input field
2. The system will automatically determine which agent should respond
3. The response will include a visual indicator showing which agent handled your query
4. Continue the conversation with follow-up questions

## Development

### Project Structure

```
├── app/
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── base_agent.py
│   │   ├── coordinator.py
│   │   ├── weather_agent.py
│   │   ├── math_agent.py
│   │   ├── knowledge_agent.py
│   │   └── assistant_agent.py
│   ├── static/
│   │   ├── css/
│   │   │   └── styles.css
│   │   └── js/
│   │       └── chat.js
│   ├── templates/
│   │   └── index.html
│   ├── __init__.py
│   └── routes.py
├── .env
├── app.py
├── requirements.txt
└── README.md
```

This multi-agent system demonstrates a scalable approach to AI agent architectures with specialized capabilities while maintaining a unified user experience.
