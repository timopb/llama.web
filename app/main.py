"""Main entrypoint for the app."""
import psutil
import json
import logging
import os
import multiprocessing
import resources as res;
from importlib import import_module
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates
from llama_cpp import Llama
from schemas import WSMessage
from sysinfo import get_html_system_state

# Port to bind to
DEFAULT_PORT=8123

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.INFO)

config_module = os.getenv("CONFIGURATION") if os.getenv("CONFIGURATION") != None else "default"
logger.info("Configuration: %s " % config_module)
conf = import_module("configuration." + config_module)

max_threads = multiprocessing.cpu_count() - 1
models_folder = os.getenv("MODELS_FOLDER") if os.getenv("MODELS_FOLDER") != None else "../models"

async def send(ws, msg: str, type: str):
    message = WSMessage(sender="bot", message=msg, type = type)
    await ws.send_json(message.dict())

@app.on_event("startup")
async def startup_event():
    global llm
    global model_name
    global stop_words
    model_name = conf.MODEL
    stop_words = conf.STOP_WORDS
    llm = Llama(model_path=os.path.join(models_folder, model_name), n_ctx=conf.CONTEXT_TOKENS, n_threads=max_threads, use_mlock=True)
    logging.info("Server started")

@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse("static/favicon.ico")

@app.get("/")
async def get(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "res": res,
        "conf": conf
    })

@app.get("/inference.js")
async def get(request: Request):
    return templates.TemplateResponse("inference.js", {
        "request": request,
        "wsurl": os.getenv("WSURL") if os.getenv("WSURL") != None else "ws://localhost:%s" % DEFAULT_PORT, 
        "res": res,
        "conf": conf
    })

async def parseCommands(websocket, query: str):
    global llm
    global model_name
    global stop_words

    if query.startswith("!model"):
        model_args=query.strip().split(" ")
        if len(model_args) == 2:
            await send(websocket, "Loading: %s..." % model_args[1], "info")
            try:
                logger.info("Switching model to: %s" % model_args[1])
                llm = Llama(model_path=os.path.join(models_folder, model_args[1]), n_ctx=conf.CONTEXT_TOKENS, n_threads=max_threads, use_mlock=True)
                model_name = model_args[1]
            except:
                logger.error ("failed to load model: %s " % model_args[1])
                await send(websocket, "Failed to load model: %s" % model_args[1], "error")
                return True
            await send(websocket, "Model loaded: %s" % model_name, "system")
        else:
            await send(websocket, "Current model: %s" % model_name, "system")
        return True

    if query == "!system":
        await send(websocket, get_html_system_state(), "system")
        return True

    if query.startswith("!stop"):
        stop_args=query.strip().split(" ")
        if len(stop_args) > 1:
            stop_arg = "".join(stop_args[1:])
            stop_words = stop_arg
            await send(websocket, "Stop words set: %s" % stop_words, "system")
        else:
            await send(websocket, "Current stop words: %s" % stop_words, "system")
        return True

    return False

@app.websocket("/inference")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await send(websocket, "Welcome to the LLaMa inference web client!", "info")

    while True:
        try:
            response_complete = ""
            start_type = ""

            received_text = await websocket.receive_text()
            payload = json.loads(received_text);

            # parse query for commands. Skip chat if a command was executed
            if await parseCommands(websocket, payload["query"]):
                continue

            prompt = payload["query"]
            start_type="start"
            logger.info("Temperature: %s " % payload["temperature"])
            logger.info("Prompt: %s " % prompt)

            await send(websocket, "Analyzing prompt...", "info")
            for i in llm(prompt,
                         echo=False,
                         stream=True,
                         temperature=payload["temperature"],
                         top_k=conf.TOP_K,
                         top_p=conf.TOP_P,
                         repeat_penalty=conf.REPETATION_PENALTY,
                         max_tokens=conf.MAX_RESPONSE_TOKENS,
                         stop=stop_words):
                response_text = i.get("choices", [])[0].get("text", "")
                if response_text != "":
                    answer_type = start_type if response_complete == "" else "stream"
                    response_complete += response_text
                    await send(websocket, response_text, answer_type)

            await send(websocket, "", "end")
        except WebSocketDisconnect:
            logging.info("websocket disconnect")
            break
        except Exception as e:
            logging.error(e)
            await send(websocket, "Sorry, something went wrong. Try again.", "error")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=DEFAULT_PORT)
