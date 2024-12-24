def get_products():
    print("Добро пожаловать!")
    try:
        quantity_products = int(input("Введите количество продуктов: "))
    except ValueError:
        print("Ошибка ввода, пожалуйста, введите целое число.")
        return None
    
    prices = []
    
    print("Введите цену для каждого продукта (или введите 'стоп' для завершения ввода): ")

    for i in range(quantity_products):
        price_input = input(f"цена продукта {i + 1}: ")
        if price_input.lower() == "стоп":
            break
        try:
            price = float(price_input)
            prices.append(price)
        except ValueError:
            print("Некорренктный ввод, пожалуйста, введите число.")
            continue
    return prices

def discount(prices):
    discount_items = list(filter(lambda x: x>100,prices))
    non_discount_prices = list(filter(lambda x: x<=100,prices))
    discount_prices = list(map(lambda x: x*0.9,discount_items))
    finish_prices = discount_prices + non_discount_prices 
    total_sum = sum(finish_prices)
    print("Цены со скидкой:", finish_prices)
    print("Итоговая сумма с учётом скидок:", total_sum)
def main():
    prices = get_products()                   
    discount(prices)
main()
