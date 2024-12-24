temp = float(input("Введите градус:"))
print(f"Конвертация цельсий в фаренгейт: {temp*9/5+32}")

num = int(input("Введите число:"))

if num%2 == 0:
    print("Четное число")#
else:
    print("Нечетное число")

num1 = int(input("Введите обычное число:"))
if num1 <= 1:
    print(f"{num1} не является простым числом.")
else:
    flag = True
    for i in range (2,int(num1**0.5)+1):
        if num1% i == 0:
            flag = False
            break
    if flag:
        print(f"{num1} простое число")
    else:
        print(f"{num1} не простое число")