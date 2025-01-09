# L-LLM Model selection based on service SLOs
# Dr. Anestis Dalgkitsis | v1.34

# Modules
import ollama
import os

# Environ
os.environ['OLLAMA_HOST'] = "http://host.docker.internal:11434"
print(os.environ.get('OLLAMA_HOST'))

# Initialize the Ollama client
client = ollama.Client()

# MAIN
def lllmms(model={}, evaluation_reports={}):
    pass

