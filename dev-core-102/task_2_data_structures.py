import os
import json

file_path = "C:\\Users\\zhas\\Desktop\\full-stack-dev\\dev-core-102\\user_info.json"

# Загружаем предыдущие данные, если файл уже существует

if os.path.exists(file_path):
    with open(file_path, "r") as file:
        user_info = json.load(file)
else:
    user_info = []

def user_info_add():
    name = input("Введите имя: ")
    age = input("Введите возраст: ")
    email = input("Введите почту: ")

    # Добавляем новый словарь с данными пользователя в список
    user_info.append({"name": name, "age": age, "email": email})

    # Сохраняем обновленные данные в файл
    with open(file_path, "w") as file:
        json.dump(user_info, file)
    print("Данные сохранены!")


def user_info_remove(index):
    try:
        remove_user = user_info.pop(index)
        print(f"Пользователь{remove_user["name"]} удален.")

        with open(file_path,'w') as f:
            json.dump(user_info,f)
        print("Данные обновлены и сохранены!")
    except IndexError:
        print("Некорретный имя пользователя")
    
user_info_add()
print("Список пользователей: ",user_info)

index_to_remove = int(input("Введите индекс пользователя для удаления: "))

user_info_remove(index_to_remove)
print("Обновленный список пользователей: " , user_info)