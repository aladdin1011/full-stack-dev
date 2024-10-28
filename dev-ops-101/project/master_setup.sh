#!/bin/bash
# Запуск скриптов по порядку
sh update_pack.sh
echo "Сервер обновлен!"

sh install_Nginx.sh
echo "Nginx установлен!"

sh create_user.sh
echo "Пользователь создан!"

sh backup_configs.sh
echo "Резервное копирование завершено!"
