# llama.web
A simple inference web UI for llama.cpp / lama-cpp-python

![Screenshot](https://github.com/timopb/llama.web/assets/3785547/01a94b0c-5706-4c51-acdf-a3694a9e6bfb)

# What it is
This web frontend is intended to run inferences against quantized ggml language models. It's very simple and intended to run locally without authentication or authorization for administrative activities. Use at own risk.

# How it works
1. Get a model from huggingface and convert it appropriately
2. Install Python packages with `pip install -r requirements.txt`
3. Modify /app/configuration/default.py to your needs
4. Set Enviornment variables if needed (see below)
5. go to the app folder and run `make start`
6. Open Web-Browser and navigate to http://localhost:8123

# Environment variables
 Name         | Purpose
--------------|---------------------------------------------------------------
CONFIGURATION | Specifies which configuration file from the configuration folder will be loaded (default.py if not set)
MODELS_FOLDER | Path to your LLMs. By default it will use "models" in the root folder of the project
WSURL         | external URL for websocket connection. Will be rendered into the HTML/Javascript. Default ws://localhost. Overwrite if running behind a reverse proxy 

# Builtin Chat Commands
As I am to lazy to build a sophisticated UI some options can only be accessed by chat commands. Type in `!help` to get a list of available commands

 Command            | Purpose
--------------------|---------------------------------------------------------------
!models             |	List available models. Click a model to load it. Due to RAM constraints changing the model will apply for all current connections
!model              |	Show currently loaded model
!model (filename)	  | Load a different model
!stop               |	List of currenlty set stop words
!stop ['word1',...] |	Assign new stopwords. Format Stopwords as Python/JSON Array 
!system	            | System State (used/free CPU and RAM)

**Tip:** Server commands (and chat messages alike) can be sent by either pressing the "Ask the LLaMa" button or pressing ctrl + enter

# Quick Prompt Templates
The web comes with three pre-defined prompt templates which can be auto-completed via a specific shortcut text and either pressing tab or ctrl + enter

Shortcut | Description
---------|-----------------------------------
#vic     |	Helpful AI Vicuna 1.1 prompt template
#story 	 | Storyteller Vicuna 1.1 prompt template
\#\#\#   |	Instruct/Response prompt template

You can define own templates in your configuration file:
```python
PROMPT_TEMPLATES = [
    ["vic",   "You are a helpful AI assistant.\\n\\nUSER: \\n\\nASSISTANT:", 39],
    ["##",    "\\n\\n### RESPONSE:", 0],
    ["story", "You are a storyteller. Your writing is vivid, exentive and very detailed. Extract the character traits from the user's input but don't name them in your story directly. Instead weave them into the story.\\n\\nUSER: Write a story about \\n\\nASSISTANT:",  231]
]
```
Each Template consists of an arry with three items:
1. The chat shortcut (without the leading \#)
2. The Template. Note: Since this is python code that is rendered into javascript code, escaped characters need to have their escape prefix escaped too (ie \\n -> \\\\n)
3. Location of the curor inside the template after auto completion

