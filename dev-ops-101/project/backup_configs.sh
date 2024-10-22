#!/bin/bash

# Запрашиваем у пользователя имя файла, который нужно сохранить
read -p "Введите имя файла для резервного копирования: " filename

# Проверяем, существует ли файл
if [[ ! -f "$filename" ]]; then
    echo "Ошибка: файл '$filename' не существует."
    exit 1
fi

# Создаем директорию backup_configs в домашнем каталоге, если она не существует
backup_dir="$HOME/backup_configs"
mkdir -p "$backup_dir"

# Создаем резервную директорию с датой в названии
date_suffix=$(date +%Y%m%d)
backup_subdir="$backup_dir/backup_configs_$date_suffix"
mkdir -p "$backup_subdir"

# Копируем файл в резервную директорию
cp "$filename" "$backup_subdir/"

# Сообщение о завершении
echo "Резервное копирование файла '$filename' завершено в '$backup_subdir'."

