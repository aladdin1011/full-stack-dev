def get_rest():
    print("Добро пожаловать! Выберите: активный отдых (1) или расслабляющий отдых(2)")
    try: 
        save = int(input("Введите (1 или 2): "))
        return save
    except ValueError:
        print("Введите (1-2)")
        return

def rest(save):
    if save == 1:
        activity = int(input("Выберите активный отдых: Горы (1), Лес (2), Пустыня (3): "))
        if activity == 1:
            print("Вы выбрали отдых в Горах. Возьмите дождевик.")
        elif activity == 2:
            print("Вы выбрали отдых в Лесу. Возьмите с собой палатку.") 
        elif activity == 3:
            print("Вы выбрали отдых в Пустыне. Не забудьте взять с собой спички.")
        else:
            print("Неправильный выбор. Введите 1, 2 или 3.")

    elif save == 2:
        relaxation = int(input("Выберите расслабляющий отдых: Пляж (1), SPA (2), Гостиница (3): "))
        if relaxation == 1:
            print("Вы выбрали отдых на пляже. Не забудьте взять солнцезащитный крем!")
        elif relaxation == 2:
            print("Вы выбрали отдых в SPA. Не забудьте взять полотенце.")
        elif relaxation == 3:
            print("Вы выбрали отдых в Гостинице. Не забудьте взять средства личной гигиены.")
        else:
            print("Неправильный выбор. Введите 1, 2 или 3.")
def main():
    save = get_rest()
    if save is not None:
        rest(save)



main()
