# To-Do List Application

Это простое приложение для управления списком задач с использованием Python. Вы можете добавлять, обновлять, удалять и завершать задачи.


# Использование 

## Добавить задачу:
```bash
    python app.py add "Описание вашей задачи"
```
## Список задач:
```bash
    python app.py list
```

## Обновить задачу:
```bash
    python app.py update <ID_задачи> "Новое описание"
```

## Удалить задачу:
```bash
     python app.py delete <ID_задачи>
```
## Завершить задачу:
```bash
    python app.py complete <ID_задачи> 
```

# Пример использования
```bash
    python app.py add "Купить продукты"
    python app.py list
    python app.py complete 1
    python app.py update 1 "Купить продукты и воду"
    python app.py delete 1
```