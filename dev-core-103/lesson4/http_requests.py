import requests

# URL для получения списка постов
url = "https://jsonplaceholder.typicode.com/posts"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()

    # Вывод списка постов
    for item in data:
        id_ = item.get("id")
        title = item.get("title")
        print(f"ID: {id_}, Title: {title}")

    # Ввод ID поста
    try:
        get_id = int(input("\nВведите ID поста для получения подробной информации: "))
        if get_id < 1 or get_id > len(data):
            print("Ошибка: ID поста вне диапазона.")
        else:
            post_id = data[get_id - 1]["id"]
            print(f"\nВыбранный пост ID: {post_id}")

            # Получение подробной информации о посте
            post_url = f"{url}/{post_id}"
            detailed_response = requests.get(post_url)

            if detailed_response.status_code == 200:
                detailed_post = detailed_response.json()

                # Структурированный вывод подробной информации
                print(f"\nПодробная информация о посте ID {post_id}:")
                print(f"Заголовок: {detailed_post.get('title')}")
                print("Тело:")
                print(detailed_post.get('body'))
                print(f"Пользователь: {detailed_post.get('userId')}")
            else:
                print(f"Ошибка при запросе поста: {detailed_response.status_code}")
    except ValueError:
        print("Ошибка: Введите числовое значение для ID.")
else:
    print(f"Ошибка при запросе списка постов: {response.status_code}")

#Отправка post запроса
data = {
    "title": "Тестовый пост",
    "body": "Содержания крутого поста",
    "userId": 1
}

# POST-запрос для создания нового поста
response = requests.post(url, json=data)

if response.status_code == 201:
    print("\nПост успешно создан!")
    print(response.json())
else:
    print("\nОшибка при отправке поста:", response.status_code)
    