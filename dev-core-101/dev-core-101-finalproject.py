def add (x,y):
    return x+y
def subtract(x,y):
    return x-y
def multiply(x,y):
    return x*y
def divide (x,y):
    if y == 0:
        return "Деление на ноль невозможно"
    return x/y
def math ():
    x = int(input("Введите первое число:"))
    y = int(input("Введите второе число:"))
    print("Введите желаемую операцию в форме (+,-,*,/)")
    z = input("")
    if z == "+":
            result = add(x, y)
            print(f"Результат: {result}")
    elif z == "-":
        result = subtract(x, y)
        print(f"Результат: {result}")
    elif z == "/":
        result = divide(x, y)
        print(f"Результат: {result}")
    elif z == "*":
        result = multiply(x, y)
        print(f"Результат: {result}")
    else:
        print("Неверная операция")

math()