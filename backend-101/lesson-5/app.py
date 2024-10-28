import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("API_KEY")
debug_mode = os.environ.get("DEBUG_MODR")

print(f"API_KEY {api_key}")
print(f"debug_mode {debug_mode}")

if debug_mode == True:
    print("Приложение запущенно в режиме откладки")
else:
    print("Приложение запущено в обычном режиме")