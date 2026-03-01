# Работаем с классными авто и методами их покраски

# Создаём класс "Автомобиль" и инициализируем его атрибуты
class Auto:
    def __init__(self, brand, model, color, year):
        self.brand = brand
        self.model = model
        self.color = color
        self.year = year

    # Методы для получения значений атрибутов
    def get_brand(self):
        return self.brand

    def get_model(self):
        return self.model

    def get_color(self):
        return self.color

    def get_year(self):
        return self.year

    # Методы для изменения значений атрибутов
    def set_brand(self, new_brand):
        self.brand = new_brand

    def set_model(self, new_model):
        self.model = new_model

    def set_color(self, new_color):
        self.color = new_color

    def set_year(self, new_year):
        self.year = new_year

    # Метод для вывода информации об автомобиле
    def info(self):
        return f"Автомобиль: {self.brand} {self.model}, цвет — {self.color}, год выпуска — {self.year}"


# Создаём несколько объектов класса "Автомобиль"
auto1 = Auto("GM", "Vectra", "красный", 1999)
auto2 = Auto("Hyundai", "Sonata", "белый", 2011)
auto3 = Auto("Ford", "Kuga", "черный", 2014)
auto4 = Auto("Subaru", "Forester", "серый", 2019)

# Вызываем методы для каждого объекта
print("Исходная информация:")
print(auto1.info())
print(auto2.info())
print(auto3.info())
print(auto4.info())

# Изменяем атрибуты с помощью методов set_
auto1.set_brand("Opel")
auto2.set_model("Elantra")
auto3.set_color("белый")
auto4.set_year(2018)


print("\nИнформация после изменения атрибутов:")
print(auto1.info())
print(auto2.info())
print(auto3.info())
print(auto4.info())

# Получаем атрибуты с помощью методов get_
print(f"\nМарка первого автомобиля: {auto1.get_brand()}")
print(f"Модель второго автомобиля: {auto2.get_model()}")
print(f"Цвет третьего автомобиля: {auto3.get_color()}")
print(f"Год выпуска червертого автомобиля: {auto4.get_year()}")
