#!/bin/bash
read -p "Введите имя нового пользователя: " username

# Проверка существования пользователя
if getent passwd "$username" &>/dev/null; then
    echo "Пользователь '$username' уже существует."
    exit 1
fi

read -p "Создать новую группу для пользователя? (y/n): " create_group

if [[ "$create_group" == "y" ]]; then
    read -p "Введите имя новой группы: " groupname

    # Проверка существования группы
    if getent group "$groupname" &>/dev/null; then
        echo "Группа '$groupname' уже существует."
        exit 1
    fi

    sudo groupadd "$groupname"
    echo "Группа '$groupname' создана."

else
    read -p "Введите имя существующей группы: " groupname

    if ! getent group "$groupname" &>/dev/null; then
        echo "Группа '$groupname' не существует."
        exit 1
    fi
fi

# Создание пользователя
echo "Создаем пользователя: $username в группе: $groupname"
sudo useradd -m -g "$groupname" "$username" || { echo "Ошибка при создании пользователя."; exit 1; }
echo "Пользователь '$username' создан и добавлен в группу '$groupname'."

read -p "Хотите установить пароль для пользователя? (y/n): " set_password

if [[ "$set_password" == "y" ]]; then
    sudo passwd "$username"
fi

echo "Настройка пользователя завершена."

