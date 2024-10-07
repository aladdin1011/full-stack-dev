#!/bin/bash
echo "Сегодня" `date`
echo "Текущий пользователь" `whoami`
directory=$(pwd)
total_count=$(find "$directory" | wc -l)
echo "Общее количество файлов и директорий: $total_count"
