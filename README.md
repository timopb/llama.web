# llama.web
A simple inference web UI for llama.cpp / lama-cpp-python

![Screenshot](https://github.com/timopb/llama.web/assets/3785547/01a94b0c-5706-4c51-acdf-a3694a9e6bfb)

# What it is
This web frontend is intended to run quantized ggml language models locally.

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
MODEL_FOLDER  | Path to your LLMs. By default it will use "models" in the root folder of the project
WS_URL        | external URL for websocket connection. Will be rendered into the HTML/Javascript. Default ws://localhost. Overwrite if running behind a reverse proxy 
