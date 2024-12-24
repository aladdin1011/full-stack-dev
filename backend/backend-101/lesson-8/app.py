import argparse
import os
import json

DATA_DIR = "data"
FILE_NAME = os.path.join(DATA_DIR,"tasks.json")

# Создаём парсер и подкоманды
parser = argparse.ArgumentParser(description="To-do List")
subparsers = parser.add_subparsers(dest="command")

# Add command
add_parser = subparsers.add_parser("add", help="Add a new task")
add_parser.add_argument("description", type=str, help="Description of the task")

# List command
list_parser = subparsers.add_parser("list", help="List all tasks")

# Update command
update_parser = subparsers.add_parser("update", help="Update an existing task")
update_parser.add_argument("task_id", type=int, help="ID of the task to update")
update_parser.add_argument("description", type=str, help="New description")

# Delete command
delete_parser = subparsers.add_parser("delete", help="Delete a task")
delete_parser.add_argument("task_id", type=int, help="ID of the task to delete")

#Complete command
complete_parser = subparsers.add_parser("complete",help="Complete a task")
complete_parser.add_argument("task_id",type=int,help="ID of the task to complete")

args = parser.parse_args()

# Функции для загрузки и сохранения задач
def load_tasks():
    os.makedirs(DATA_DIR,exist_ok=True)
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r",encoding="utf-8") as file:
                return json.load(file)["tasks"]
        except (json.JSONDecodeError,KeyError):
            print("Ошибка: файл данных повреждён. Попробуйте удалить его и занова создаьть.")
            return []
    return []

def save_tasks(tasks):
    os.makedirs(DATA_DIR,exist_ok=True)
    with open(FILE_NAME, "w",encoding="utf-8") as file:
        json.dump({"tasks": tasks}, file, indent=4, ensure_ascii=False)

# Функция для добавления задачи
def add_task(description):
    tasks = load_tasks()
    new_task_id = max([task["id"] for task in tasks], default=0) + 1
    tasks.append({"id": new_task_id, "description": description, "completed": False})
    save_tasks(tasks)
    print(f"Task added with ID: {new_task_id}")

# Функция для вывода списка задач
def list_tasks():
    tasks = load_tasks()
    if not tasks:
        print("No tasks found.")
    else:
        for task in tasks:
            status = "✔" if task["completed"] else "✘"
            print(f"{task['id']}: {task['description']} [{status}]")

# Функция для обновления задачи
def update_task(task_id, description):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["description"] = description
            save_tasks(tasks)
            print(f"Task {task_id} updated.")
            return
    print("Task not found.")

# Функция для удаления задачи
def delete_task(task_id):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            save_tasks(tasks)
            print(f"Task {task_id} deleted.")
            return
    print("Task not found.")

def complete_task(task_id):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = True
            save_tasks(tasks)
            print(f"Task {task_id} completed")
            return
    print("Task not found.")
# Выполнение команды на основе аргументов
if args.command == "add":
    add_task(args.description)
elif args.command == "list":
    list_tasks()
elif args.command == "update":
    update_task(args.task_id, args.description)
elif args.command == "delete":
    delete_task(args.task_id)
elif args.command == "complete":
    complete_task(args.task_id)
else:
    parser.print_help()