from datetime import datetime

def get_sum():
    try:
        price =  int(input("Введите сумму заказа: "))
        return price
    except ValueError:
        print("Попробуйте еще раз.")
        return None 

def apply_basic_discount(price):
    save = input("Вы являетесь участником программы лояльности или нет? (ДА), (НЕТ): ")
    if save == "ДА":
        price -= price * 0.10
    elif save == "НЕТ":
        return price- price * 0.10
    else:
        print("Некорректный ввод. Пожалуйста, введите 'ДА' или 'НЕТ'.")
        return price
def apply_basic_discount(price):
    save = input("Вы являетесь участником программы лояльности? (ДА/НЕТ): ").strip().upper()
    if save == "ДА":
        # Применяем скидку 10% для участников программы лояльности
        return price - price * 0.10
        print("Применена скидка 10% для участников программы лояльности.")
    elif price > 1000:
        # Если сумма больше 1000, применяем дополнительную скидку 5%
        return price - price * 0.05
        print("Применена дополнительная скидка 5% (сумма заказа больше 1000).")
    return price
def apply_wildcard_tax(price):
    current_minute =  datetime.now().minute 
    if current_minute % 2 == 0:
        return price 
    else:
        return price+price*0.05

def promo_code(price):
    promo = input("Введите промокод: ")
    if promo == "DISCOUNT2024":
        return price-price * 0.05
    else:
        print("Некоретный промокод")
        return price 

def main():
    price = get_sum()
    if price is not None:
            price = apply_basic_discount(price)
            price = apply_wildcard_tax(price)
            price = promo_code(price)
            print(f"Итоговая сумма после всех примененных скидок и налогов: {price:.2f}")

main()