import requests
import json

# URL для получения списка постов
url = "https://jsonplaceholder.typicode.com/posts"

# Попытка отправить GET-запрос для получения списка постов
try:
    response = requests.get(url)
    # Проверка, что запрос прошел успешно (статус-код 200)
    response.raise_for_status()  # Генерирует исключение для неверных ответов
    posts = response.json()  # Преобразуем ответ в JSON

    # Сохраняем данные в файл
    with open(r'C:\Users\zhas\Desktop\full-stack-dev\dev-core-103\lesson4\posts_data.json', 'w') as file:
        json.dump(posts, file, indent=4)  # Записываем JSON с отступами для читаемости
    print("Данные успешно сохранены в posts_data.json")

    # Выбираем один пост по ID, например, ID = 1
    post_id = 1
    post_url = f"https://jsonplaceholder.typicode.com/posts/{post_id}"
    
    # Попытка отправить GET-запрос для получения информации о выбранном посте
    post_response = requests.get(post_url)
    post_response.raise_for_status()  # Проверка успешности ответа
    post_details = post_response.json()
    print("Информация о посте:", post_details)

    # Реализуем POST-запрос для создания нового поста
    new_post_data = {
        "title": "Новый пост",
        "body": "Это тело нового поста.",
        "userId": 1
    }

    post_creation_url = "https://jsonplaceholder.typicode.com/posts"
    
    # Попытка отправить POST-запрос
    create_response = requests.post(post_creation_url, json=new_post_data)
    create_response.raise_for_status()  # Проверка успешности ответа
    created_post = create_response.json()
    print("Новый пост создан:", created_post)

except requests.exceptions.RequestException as e:
    # Обработка ошибок, связанных с запросами
    print(f"Произошла ошибка при выполнении запроса: {e}")
