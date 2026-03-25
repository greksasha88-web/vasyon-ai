from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from agent_v2 import run_agent

app = FastAPI()


class Task(BaseModel):
    text: str


@app.post("/run")
def run(task: Task):
    result = run_agent(task.text)

    # если агент вернул словарь
    if isinstance(result, dict):
        return result

    # если просто текст
    return {
        "type": "text",
        "result": result
    }


@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
        <head>
            <title>Vasya AI 🚀</title>
        </head>
        <body style="background:black;color:white;text-align:center;padding-top:50px;">
            <h1>🔥 Vasya AI запущен</h1>
            <p>Сервер работает</p>
            <a href="/docs" style="color:cyan;">Открыть API</a>
        </body>
    </html>
    """
