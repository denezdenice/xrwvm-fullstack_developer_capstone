# from django.contrib import admin
# from .models import related models


# Register your models here.

# CarModelInline class

# CarModelAdmin class

# CarMakeAdmin class with CarModelInline

# Register models here

# my_app/admin.py
from django.contrib import admin
from .models import CarMake, CarModel # Importe tes modèles

# Enregistre tes modèles ici
admin.site.register(CarMake)
admin.site.register(CarModel)