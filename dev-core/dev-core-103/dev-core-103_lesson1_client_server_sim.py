import random
def client_request():
    print("Клиент отправляет запрос на сервер")
    internet = random.choice([1,0])
    return internet
def server_response(internet):
    print("Сервер обрабатывает запрос")
    if internet == 1:
        print("Сервер отправляет ответ: Добро пожаловать в интернет!")
    else:
        print("Сервер отправляет ответ: 404")
def main():
    internet = client_request()
    server_response(internet)

main()