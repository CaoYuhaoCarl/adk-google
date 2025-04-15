from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import Session
from google.adk.memory import InMemoryMemoryService
from google.adk.models.lite_llm import LiteLlm
from dotenv import load_dotenv

# Load environment variables
load_dotenv('./.env')

# Initialize models
root_agent_model = LiteLlm(model = "ollama/deepseek-r1:14b")
greeting_agent_model = LiteLlm(model = "ollama/deepseek-r1:14b")
farewell_agent_model = LiteLlm(model = "ollama/deepseek-r1:14b")

# Initialize session service
session_service = InMemoryMemoryService()

APP_NAME = "Carl's Weather App"
USER_ID = "user_1"
SESSION_ID = "session_001"

session = Session(
    app_name = APP_NAME,
    user_id = USER_ID,
    id = SESSION_ID
)

session = session_service.add_session_to_memory(
    session = session
)

# ----------- Define tools -----------

# say_hello tool
def say_hello(name: str = "there") -> str:
    """
   Provides a simple greeting, optionally addressing the user by name.

   Args:
       name (str, optional): The name of the person to greet. Defaults to "there".
   
   Returns:
       str: A greeting message.
   """
    print(f"--- Tool: say_hello called with name: {name} ---")
    return f"Hello {name}!"

# say_goodbye tool
def say_goodbye() -> str:
    """
    Provides a simple farewell message to conclude the conversation.
    """
    print(f"--- Tool: say_goodbye called ---")
    return f"Goodbye! Have a nice day."

# get_weather tool
def get_weather(city: str) -> dict:
    """
    Retrieves the current weather for a specified city.
    
    Args:
        city (str): The name of the city for which to retrieve weather report.
    
    Returns:
        dict: status and result or error msg.
    """
    if city.lower() == "new york":
        return {
            "status": "success",
            "report": {"city": city, "temperature": "22°C", "condition": "sunny"},
        }
    else:
        return {
            "status": "error",
            "error_message": f"City {city} not found.",
        }

# ----------- Initialize agents -----------

# greeting_agent
greeting_agent = Agent(
    name="greeting_agent",
    model=greeting_agent_model,
    instruction="You are a helpful assistant that provides a simple greeting, Your ONLY task is to optionally address the user by name."
                "Use 'say_hello' tool to provide a greeting."
                "If the user provides their name, make sure to pass it to the 'say_hello' tool."
                "Do not engage in any other conversation or tasks.",
    description="Handle simple greeting and hellos using the 'say_hello' tool that provides a simple greeting.",
    tools=[say_hello],
)

# farewell_agent
farewell_agent = Agent(
    name="farewell_agent",
    model=greeting_agent_model,
    instruction="You are a helpful Farewell Agent. Your ONLY task is to provide a simple farewell message."
                "Use 'say_goodbye' tool to provide a farewell message."
                "Do not engage in any other conversation or tasks.",
    description="Handle simple farewells using the 'say_goodbye' tool that provides a simple farewell message.",
    tools=[say_goodbye],
)

# root_agent
root_agent = Agent(
    name="root_agent",
    model=root_agent_model,
    instruction="You are the main Weather Agent coordinating a agent team. Your PRIMARY responsibility is to handle weather requests."
                "Use 'get_weather' tool ONLY to provide weather information."
                "You have specialized sub_agents: "
                "1. 'greeting_agent': Handle simple greetings like 'hello' or 'hi'."
                "2. 'farewell_agent': Handle simple farewells like 'goodbye' or 'see you later'."
                "Analyze the user's query. If it's greeting, delegate to 'greeting_agent'."
                "If it's a weather request, delegate to 'get_weather' tool."
                "For anything else, respond appropriately or state you cannot help.",
    description="The main coordinator agent. Handles weather requests and delegates greetings/farewells to specialized agents.",
    tools=[get_weather],
    sub_agents=[greeting_agent, farewell_agent]
)

# ----------- Initialize runner -----------
runner_root = Runner(
    app_name = APP_NAME,
    session_service = session_service,
    agent = root_agent
)
