from django.db import models


class BaseModel(models.Model):
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Countries(models.TextChoices):
    Канада = "Канада"
    Франция = "Франция"
    Германия = "Германия"
    Италия  = "Италия"
    Япония = "Япония"
    Россия = "Россия"
    Великобритания = "Великобритания"
    Китай = "Китай"


def default_car():
    return {
        'name': None,
        'car_model': None,
        'car_year': None,
        'car_color': None,
        'number_of_doors': 2,
        'body_type': None,
        'type_drive': None,
        'country': None,
        'car_number': None,
        'car_class': None, 
        'transmission': None,
        'type_fuel': None
    }


class Colors(models.TextChoices):
    Желтый = "Желтый"
    Черный = "Черный"
    Белый = "Белый"
    Красный = "Красный"
    Синий = "Синий"
    Серый = "Серый"
    Зеленый = "Зеленый"
    Коричневый = "Коричневый"


class BodyTypes(models.TextChoices):
    Седан = "Седан"
    Хэтчбек = "Хэтчбек"
    Внедорожник = "Внедорожник"
    Купе = "Купе"
    Минивэн = "Минивэн"
    Пикап = "Пикап"
    Кабриолет = "Кабриолет"


class DriveTypes(models.TextChoices):
    Передний = "Передний"
    Задний = "Задний"
    Полный = "Полный"


class Transmission(models.TextChoices):
    Механическая = "Механическая"
    Автоматическая = "Автоматическая"
    Триптроник = "Триптроник"


class ConfigurationType(models.TextChoices):
    Классика = "Классика"
    Комфорт = "Комфорт"
    Премиум = "Премиум"


class FuelType(models.TextChoices):
    Бензин = "Бензин"
    Дизель = "Дизель"
    Гибрид = "Гибрид"
    Электричество = "Электричество"


class PeriodCredit(models.TextChoices):
    Шесть_месяцев = '6 месяцев'
    Двенадцать_месяцев = '12 месяцев'
    Восемнадцать_месяцев = '18 месяцев'
    Двадцать_четыре_месяца = '24 месяцев'


class Payment(models.TextChoices):
    Наличные = 'Наличные'
    Кредит = 'Кредит'
    Банковская_карта = 'Банковская карта'
