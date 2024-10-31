from datetime import datetime
loyalty_client = ["ZHAS","KUAT","BOBA","BUBA"]
#Рассчитывает скидку для постоянных клиентов
def apply_bacis_discount(price,discount_rate):
    return price - price * discount_rate
#Рассчитывает скидку для экслюзив клиентов
def apply_loyalty_discount(price,discount_rate):
    return apply_bacis_discount(price,discount_rate) * 0.9
#Вычисляет налог 
def apply_basic_tax(price,tax_rate):
    return price - price*tax_rate
#Определяет четная или нечетная минута
def apply_wildcard_tax(price,tax_rate):
    current_minute =  datetime.now().minute 
    if current_minute % 2 == 0:
        return price 
    else:
        return price+price*tax_rate
#вычисление на кассе 
def calculate_final_price(customer_name,price,discount_rate,tax_rate):
    if customer_name in loyalty_client:
        final_price = apply_loyalty_discount(price,discount_rate)
    else:
        final_price =  apply_bacis_discount(price,discount_rate)
    
    final_price = apply_wildcard_tax(final_price,tax_rate)

    return print(final_price)


customer_name = input("Введит имя клиента: ")
price = 100
discount_rate = 0.1
tax_rate = 0.05
calculate_final_price(customer_name,price,discount_rate,tax_rate)

