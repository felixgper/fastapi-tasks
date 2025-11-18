from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title= "API PARA LA REALIZACION DE TAREAS")

class Tasks(BaseModel):
    id: int
    name: str
    place: str

tasks_list = []

@app.get("/tasks")
async def get_tasks():
    if not tasks_list:
        return {"message" : "La lista está vacía"}
    return tasks_list

@app.get("/tasks/{id}")
async def get_tasks(id: int):
    task = search_id(id)
    if task is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return task

@app.post("/tasks")
async def post_tasks(task: Tasks):
    existing = search_id(task.id)
    if existing is not None:
        raise HTTPException(status_code=404, detail="Id de Tarea ya en uso")
    tasks_list.append(task)
    return task

@app.put("/tasks/{id}")
async def put_tasks(id: int, task: Tasks):
    found = False
    for index, value in enumerate(tasks_list):
        if value.id == id:
            tasks_list[index] = task 
            found = True
            return {"message": "Tarea Actualizada",
                    "Task updated": task}
        
    if not found:
        return {"error" : "No se encontro el usuario"}

@app.delete("/tasks/{id}")
async def delete_tasks(id: int):
    found = False
    for index, value in enumerate(tasks_list):
        if value.id == id:
            del tasks_list[index]
            found = True
            return {"message": "Task deleted"}
        
    if not found:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

def search_id(id: int):
    for task in tasks_list:
        if task.id == id:
            return task
    return None