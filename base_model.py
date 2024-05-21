from django.db import models
from django_countries import Countries


class BaseModel(models.Model):
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class G8Countries(Countries):
    only = ["CA", "FR", "DE", "IT", "JP", "RU", "GB", "CN"]


def default_car():
    return {
        'car_model': None,
        'car_year': None,
        'car_color': None,
        'number_of_doors': 2,
        'body_type': None,
        'type_drive': None,
        'country': None,
        'volume_fuel_tank': None
    }


class Colors(models.TextChoices):
    YELLOW = "Желтый"
    BLACK = "Черный"
    WHITE = "Белый"
    RED = "Красный"
    BLUE = "Синий"
    GREY = "Серый"
    GREEN = "Зеленый"
    BROWN = "Коричневый"


class BodyTypes(models.TextChoices):
    SEDAN = "Sedan"
    HATCHBACK = "Hatchback"
    CROSSOVER = "SUV"
    COUPE = "Coupe"
    MINIVAN = "Minivan"
    PICKUP = "Pickup"
    CONVERTIBLE = "Convertible"


class DriveTypes(models.TextChoices):
    FRONT = "Front"
    REAR = "Rear"
    ALL = "All"


class PeriodCredit(models.TextChoices):
    VALUE1 = '6 месяцев'
    VALUE2 = '12 месяцев'
    VALUE3 = '18 месяцев'
    VALUE4 = '24 месяцев'
