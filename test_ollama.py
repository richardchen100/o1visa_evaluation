from ollama import Client
from dotenv import load_dotenv

load_dotenv()
ollama_client = Client(host="http://localhost:11434")

try:
    # Attempt to list models
    models = ollama_client.list()
    print("Ollama is running. Available models:", models)
except Exception as e:
    print("Failed to connect to Ollama:", str(e))
