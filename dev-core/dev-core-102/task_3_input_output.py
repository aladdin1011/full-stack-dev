import os
file_path = "C:\\Users\\zhas\\Desktop\\full-stack-dev\\dev-core-102\\user_info.txt"

def add_info():
    name = input("Введите ваше имя: ")
    try:
        age = int(input("Введите ваш возраст: "))
    except ValueError:
        print("Ошибка: пожалуйста, введите число ")
        return
    color = input("Введите ваш любимый цвет: ")
    return f"Имя: {name}, Возраст: {age}, Любимый цвет: {color}\n"

def save_info():
    with open(file_path,"a",encoding="utf-8") as file:
        user_info = add_info()
        if user_info:
            file.write(user_info)

def read_info():
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
            print("Содержимое файла:")
            print(content)
    except FileNotFoundError:
        print("Файл не найден. Возможно, вы еще не добавили никакой информации.")

def main():
    print("Добро пожаловать!")
    while True:
        print("\nМеню:")
        print("1. Добавить данные")
        print("2. Показать информацию")
        print("3. Выход")
        action = input("Выберите действия (1-3): ")
    
        if action == "1":
            save_info()
        elif action == "2":
            read_info()
        elif action == "3":
            break
        else:
            print("Некорректный ввод. Пожалуйста, выберите 1, 2 или 3.")

main()