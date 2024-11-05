conference = ["Zhaskairat","Kuat","Adlet","Sanzar"]
coordinates = (43,76)
user_info = {
    "Zhaskarat":{
        "age":"20",
        "email":"zhas@gmail.com"
    },
    "Kuat":{
        "age":"19",
        "email":"kuat@gmail.com"
    },
    "Adlet":{
        "age":"20",
        "email":"adlet@gmail.com"
    },
    "Sanzar":{
        "age":"20",
        "email":"sanzar@gmail.com"
    }
}

def add_user():
    name = input("Введите имя пользователя: ")
    if name in user_info:
        print(f"Пользователь {name} уже существует")
        return
    age = input("Введите возраст пользователя: ")
    email = input("Введите почту пользователя: ")
    
    user_info[name] = {
        "age": age,
        "email": email
    }
    print(f"Пользователь {name}, успешно добавлен")

def remove_user():
    name = input("Введите имя пользователя: ")
    if name in user_info:
        del user_info[name]
        print(f"Пользователь удален {name}!")
    else:
        print(f"Пользователь {name}, не найден.")

def display_user():
    name = input("Введите имя пользователя: ")
    if name in user_info:
        info = user_info[name]
        print(f"Имя:{name}")
        print(f"Возраст:{info['age']}")
        print(f"Почта:{info["email"]}")
    else:
        print(f"Пользователь {name}, не найден")

add_user()
display_user()
print(user_info)
remove_user()
print(user_info)