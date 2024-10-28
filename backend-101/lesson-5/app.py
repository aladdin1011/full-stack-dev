import os
from dotenv import load_dotenv

load_dotenv()

#Получение значений переменных окружения os.environ.get("API_KEY")
api_key = os.environ.get("API_KEY")
debug_mode = os.environ.get("DEBUG_MODE")

#Проверка значений
print (f"API_KEY: {api_key}")
print(f"DEBUG_MODE: {debug_mode}")

if debug_mode == "True":
    print("Приложение запущено в режиме отладки.")
else:
    print("Приложение запущено в обычном режиме.")  