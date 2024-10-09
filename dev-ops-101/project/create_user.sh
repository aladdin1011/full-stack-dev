#!/bin/bash

# Запрос имени нового пользователя
read -p "Введите имя нового пользователя: " username

# Запрос, создавать новую группу или добавлять в существующую
read -p "Создать новую группу? (yes/no): " create_group

if [[ "$create_group" == "yes" ]]; then
    # Запрос имени группы
    read -p "Введите имя новой группы: " groupname
    # Создание новой группы
    sudo groupadd "$groupname"
else
    # Запрос имени существующей группы
    read -p "Введите имя существующей группы: " groupname
fi

# Создание нового пользователя и добавление в группу
sudo useradd -m -G "$groupname" "$username"
echo "Пользователь $username успешно создан и добавлен в группу $groupname."

# Установка пароля для нового пользователя
sudo passwd "$username"
