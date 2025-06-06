from fastapi import FastAPI, Request, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from openai import OpenAI
import os
from typing import List

app = FastAPI()

app.mount('/static', StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key="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"
)



class ChatMessage(BaseModel):
    message: str

@app.get("/", responce_class = HTMLResponse)
async def read_root(request : Request):
    templates.TemplateResponce("/index", {"request":request})

@app.get("/camera", responce_class =  HTMLResponce)
async def read_root("request": Request):
    templates.TemplateResponce("/camera", {"request" : request})

@app.get("/AIimg", responce_class = HTMLResponce)
async def read_root("request" : Request):
    templates.TemplateResponce("/imagegenAI", {"request": request})

@app.get("/material", responce_class = HTMLResponce)
async def read_root("request":Request):
    templates.TemplateResponce("/material", {"request":request})

@app.get("/shorts", responce_class = HTMLResponce)
async def ("request": Request):
    templates.TemplateResponce("/shorts", {"request": request})

@app.post("/chat")
async def chat(chat_message: ChatMessage):
JSONResponceForm = """const AnyTitleOfTheContent = [
            {
                id: 1,
                title: "The Quantum Revolution",
                prompt:"In the early 20th century, physicists discovered that light behaves both as particles and waves. This dual nature sparked the quantum revolution.",
            },
            {
                id: 2,
                title: "Schrödinger's Equation",
                prompt: "Erwin Schrödinger formulated an equation that describes how quantum systems evolve over time. The wave function ψ contains all information about a quantum system."
            },
            {
                id: 3,
                title: "The Uncertainty Principle",
                prompt: "Heisenberg showed that we cannot simultaneously know both the position and momentum of a particle with perfect accuracy. This fundamental limit is known as the uncertainty principle."
            },
            {
                id: 4,
                title: "Quantum Superposition",
                prompt:"Quantum particles can exist in multiple states simultaneously. Schrödinger's famous cat thought experiment illustrates this paradoxical behavior."
            },
            {
                id: 5,
                title: "Quantum Entanglement",
                prompt: "When particles become entangled, they share a quantum connection. Measuring one instantly affects the other, no matter how far apart they are."
            }
        ];"""
    if not hasattr(app, 'conversation'):
        app.conversation = Conversation()
    manipulated_prompt = f"you have to gerate the resonce in json formate alone. you have to reply in this formate '' "

    app.conversation.messages.append({"role": "user", "content": manipulated_prompt})
    append_to_aboutme(f"User: {chat_message.message}")

    completion = client.chat.completions.create(
        model="nvidia/llama-3.1-nemotron-70b-instruct",
        messages=app.conversation.messages,
        temperature=1,
        top_p=1,
        max_tokens=2000,
        stream=True
    )

    response = ""
    for chunk in completion:
        if chunk.choices and chunk.choices[0].delta and chunk.choices[0].delta.content is not None:
            response += chunk.choices[0].delta.content
    app.conversation.messages.append({"role": "assistant", "content": response})

    append_to_aboutme(f"AI: {response}")

    return {"response": response}
