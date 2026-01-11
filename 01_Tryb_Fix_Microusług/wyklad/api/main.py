from fastapi import FastAPI
from celery import Celery
from celery.result import AsyncResult
from pydantic import BaseModel

app = FastAPI()

class TextIn(BaseModel):
    text: str

# Celery z Redisem
celery = Celery("tasks", broker="redis://redis:6379/0",
 backend="redis://redis:6379/0")

@app.post("/translate")
def translate(req: TextIn):
   task = celery.send_task("tasks.translate_text", args=[req.text])
   return {"task_id": task.id, "status": "processing"}

@app.get("/task/{task_id}")
def get_task_status(task_id: str):
   task = AsyncResult(task_id, app=celery)
   if task.status == "PENDING":
      return {"status": task.status, "result": None}
   elif task.status == "SUCCESS":
      return {"status": task.status, "result": task.result}
   else:
      return {"status": task.status, "result": None}

@app.post("/audio")
def generate_audio(req: TextIn):
   task = celery.send_task("tasks.generate_audio", args=[req.text])
   return {"task_id": task.id, "status": "processing"}
