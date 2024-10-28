import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("API_KEY")
debug_mode = os.environ.get("DEBUG_MODE")

print(f"API_KEY: {api_key}")
print(f"DEBUG_MODE: {debug_mode}")


if debug_mode == "True":
    print("Приложение запущено в режиме откладки")
else:
    print("Приложение запущено в обычном режиме")
