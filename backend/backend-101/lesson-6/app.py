import numpy as np 
import requests
import time
i = 0
numbers = []
for i in range(5):
    
    url = "https://random-data-api.com/api/number/random_number"

    response = requests.get(url)
    
    if response.status_code == 200:
        number = response.json()
        non_zero_number = number.get("non_zero_number")
        
        if non_zero_number is not None:
            numbers.append(non_zero_number)
        else:
            print("Ключ 'non_zero_number' не найден в ответе.")
    else:
        print(f"Ошибка при получение запроса {response.status_code}")        
    time.sleep(1.2)

numbers_array = np.array(numbers)

if numbers_array.size > 0:
    mean_value = np.mean(numbers_array)
    print(f"Полученные числа{numbers_array}")
    print(F"Среднее значение из этих чисел {mean_value}")
else:
    print("Увы")