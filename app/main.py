
"""Main entrypoint for the app."""
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
from schemas import ChatResponse

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

@app.on_event("startup")
async def startup_event():
    global llm
    max_threads = multiprocessing.cpu_count() - 1
    models_folder = os.getenv("MODELS_FOLDER") if os.getenv("MODELS_FOLDER") != None else "../models"
    llm = Llama(model_path= models_folder + "/" + conf.MODEL, n_ctx=conf.CONTEXT_TOKENS, n_threads=max_threads, use_mlock=True)
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

def cleanup_message(message):
    result = message.strip();
    result = result.replace('\n', ' ').replace('\r', '')
    result += "\n"
    return result

@app.websocket("/inference")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    welcome_resp = ChatResponse(sender="bot", message="Welcome to the LLaMa inference web client!<br>Model used: %s" % conf.MODEL, type="info")
    await websocket.send_json(welcome_resp.dict())

    while True:
        try:
            response_complete = ""
            start_type=""

            # Receive and send back the client message
            received_text = await websocket.receive_text()
            payload = json.loads(received_text);
            prompt = payload["query"] + "\n\n" + "### response:"
            start_type="start"
            logger.info("Temperature: %s " % payload["temperature"])
            logger.info("Prompt: %s " % prompt)
            info_resp = ChatResponse(sender="bot", message="Analyzing prompt...", type="info")
            await websocket.send_json(info_resp.dict())

            for i in llm(prompt, 
                         echo=False, 
                         stream=True, 
                         temperature=payload["temperature"], 
                         top_k=conf.TOP_K, 
                         top_p=conf.TOP_P, 
                         repeat_penalty=conf.REPETATION_PENALTY, 
                         max_tokens=conf.MAX_RESPONSE_TOKENS,
                         stop=["### response:"]):
                response_text = i.get("choices", [])[0].get("text", "")
                if response_text != "":
                    answer_type = start_type if response_complete == "" else "stream"
                    response_complete += response_text
                    end_resp = ChatResponse(sender="bot", message=response_text, type=answer_type)
                    await websocket.send_json(end_resp.dict())
         
            end_resp = ChatResponse(sender="bot", message="", type="end")
            await websocket.send_json(end_resp.dict())

        except WebSocketDisconnect:
            logging.info("websocket disconnect")
            break

        except Exception as e:
            logging.error(e)
            resp = ChatResponse(
                sender="bot",
                message="Sorry, something went wrong. Try again.",
                type="error",
            )
            await websocket.send_json(resp.dict())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=DEFAULT_PORT)
