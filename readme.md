# Multistep Agent

## Step1: Setup

### Create & Activate Virtual Environment (Recommended)

```bash
# Create
python -m venv .venv
# Activate (each new terminal)
# macOS/Linux: source .venv/bin/activate
# Windows CMD: .venv\Scripts\activate.bat
# Windows PowerShell: .venv\Scripts\Activate.ps1

source .venv/bin/activate
```

### Install dependencies

```bash
pip install google-adk litellm dotenv
```

### Create .env file

```bash
GOOGLE_GENAI_USE_VERTEXAI="False"
GOOGLE_API_KEY="your google api key"
OPENAI_API_KEY="your openai api key"
```

## Step2: Setup Models

### openai gpt-4o-mini

```python
load_dotenv('./.env')

root_agent_model = LiteLlm(model = "gpt-4o-mini")
greeting_agent_model = LiteLlm(model = "gpt-4o-mini")
farewell_agent_model = LiteLlm(model = "gpt-4o-mini")
```

### google genai

```python
load_dotenv('./.env')

root_agent_model = "gemini-2.0-flash-exp"
greeting_agent_model = "gemini-2.0-flash"
farewell_agent_model = "gemini-2.0-flash"
```

### ollama deepseek-r1:14b 本地大模型

```python
load_dotenv('./.env')

root_agent_model = LiteLlm(model = "ollama/deepseek-r1:14b")
greeting_agent_model = LiteLlm(model = "ollama/deepseek-r1:14b")
farewell_agent_model = LiteLlm(model = "ollama/deepseek-r1:14b")
```

## references

[1] https://google.github.io/adk-docs/get-started/quickstart/#set-up-the-model
[2] https://www.youtube.com/watch?v=SjZG-QKrw5o
