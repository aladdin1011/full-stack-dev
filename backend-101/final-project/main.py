from fastapi import FastAPI, HTTPException

# Объявление переменной tasks
tasks = []

app = FastAPI()

@app.get("/tasks/")
def get_tasks():
    return tasks

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    if task_id >= len(tasks) or task_id < 0:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    return tasks[task_id]

@app.post("/tasks/")
def create_task(name: str):
    task = {"id": len(tasks), "name": name}
    tasks.append(task)
    return task

@app.put("/tasks/{task_id}")
def update_task(task_id: int, name: str):
    if task_id >= len(tasks) or task_id < 0:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    tasks[task_id]["name"] = name
    return tasks[task_id]

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    if task_id >= len(tasks) or task_id < 0:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    return tasks.pop(task_id)
