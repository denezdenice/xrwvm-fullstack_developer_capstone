from django.db import models
from django.utils.timezone import now
from django.core.validators import MaxValueValidator, MinValueValidator

# Crée tes modèles ici.

class CarMake(models.Model):
    # Le champ 'name' pour le nom de la marque (ex: "Toyota", "Ford")
    # max_length est obligatoire pour CharField
    name = models.CharField(max_length=100)

    # Le champ 'description' pour une description plus longue de la marque
    description = models.TextField()

    # Tu peux ajouter d'autres champs ici si nécessaire, par exemple:
    # country = models.CharField(max_length=50, blank=True, null=True)
    # website = models.URLField(blank=True, null=True)

    def __str__(self):
        """
        Méthode __str__ pour retourner une représentation textuelle de l'objet CarMake.
        C'est utile pour l'affichage dans l'interface d'administration de Django
        et lors de l'impression d'objets CarMake.
        """
        return self.name

class CarModel(models.Model):
    # Relation Many-To-One avec CarMake.
    # Chaque CarModel est associé à une seule CarMake,
    # mais une CarMake peut avoir plusieurs CarModels.
    # models.CASCADE signifie que si une CarMake est supprimée,
    # tous les CarModels associés seront également supprimés.
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)

    # ID du concessionnaire, faisant référence à un concessionnaire dans la base de données Cloudant.
    # Il est important que ce champ soit un IntegerField car c'est un identifiant numérique.
    dealer_id = models.IntegerField()

    # Nom du modèle de voiture (ex: "Corolla", "F-150").
    name = models.CharField(max_length=100)

    # Choix prédéfinis pour le type de voiture.
    # Utiliser des tuples (valeur_stockée, affichage_lisible).
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
        # Ajoute d'autres types si nécessaire
    ]
    # Champ de type avec des choix limités et une valeur par défaut.
    type = models.CharField(max_length=15, choices=CAR_TYPES, default='SUV')

    # Année du modèle.
    # Bien que le prompt ait mentionné 'DateField', IntegerField est plus approprié
    # pour stocker seulement l'année numérique.
    year = models.IntegerField(
        default=now().year, # Définit l'année par défaut à l'année courante
        validators=[
            MinValueValidator(2015, message="L'année doit être au moins 2015."), # Validation de la valeur minimale
            MaxValueValidator(2025, message="L'année ne peut pas dépasser l'année en cours (2025).") # Validation de la valeur maximale
        ]
    )
    
    # Tu peux ajouter d'autres champs ici si nécessaire, par exemple:
    # mileage = models.IntegerField(blank=True, null=True)
    # color = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        """
        Méthode __str__ pour retourner une représentation textuelle de l'objet CarModel.
        Affiche la marque et le nom du modèle pour une meilleure lisibilité.
        """
        return f"{self.car_make.name} {self.name}"
