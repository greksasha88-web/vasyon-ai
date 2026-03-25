from fastapi import FastAPI
from pydantic import BaseModel
from agent_v2 import run_agent

app = FastAPI()

class Task(BaseModel):
    text: str

@app.post("/run")
def run(task: Task):
    result = run_agent(task.text)
    return {
        "result": result.get("result", ""),
        "files": result.get("files", [])
    }