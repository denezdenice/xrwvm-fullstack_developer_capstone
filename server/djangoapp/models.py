from django.db import models
from django.utils.timezone import now
from django.core.validators import MaxValueValidator, MinValueValidator

# Nouveau modèle pour les concessionnaires
class Dealer(models.Model):
    name = models.CharField(max_length=200)
    # Ajoutez d'autres champs si nécessaire pour un concessionnaire (adresse, ville, etc.)
    # Par exemple, si vous avez un ID externe, vous pouvez le stocker ici aussi :
    # external_id = models.IntegerField(unique=True, null=True, blank=True)

    def __str__(self):
        return self.name

class CarMake(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    country = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name

class CarModel(models.Model):
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)

    # C'est la modification la plus importante : Utiliser une ForeignKey vers le modèle Dealer
    # Si chaque voiture DOIT avoir un concessionnaire:
    dealer = models.ForeignKey(Dealer, on_delete=models.CASCADE)
    # Si une voiture PEUT ne pas avoir de concessionnaire (temporairement ou si l'ID Cloudant n'est pas trouvé):
    # dealer = models.ForeignKey(Dealer, on_delete=models.SET_NULL, null=True, blank=True)

    name = models.CharField(max_length=100)

    CAR_TYPES = [
        ('SEDAN', 'Sedan'),
        ('SUV', 'SUV'),
        ('WAGON', 'Wagon'),
        ('COUPE', 'Coupe'),
        ('HATCHBACK', 'Hatchback'),
        ('MINIVAN', 'Minivan'),
        ('TRUCK', 'Truck'),
        ('SPORTS_CAR', 'Sports Car'),
        ('CONVERTIBLE', 'Convertible'),
    ]
    type = models.CharField(max_length=15, choices=CAR_TYPES, default='SUV')

    year = models.IntegerField(
        default=now().year,
        validators=[
            MinValueValidator(2015, message="L'année doit être au moins 2015."),
            MaxValueValidator(now().year, message=f"L'année ne peut pas dépasser l'année en cours ({now().year}).")
        ]
    )

    def __str__(self):
        return f"{self.car_make.name} {self.name} ({self.year})"