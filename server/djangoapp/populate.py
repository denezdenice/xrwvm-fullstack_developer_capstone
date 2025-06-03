from .models import CarMake, CarModel, Dealer # <-- Importez le modèle Dealer

def initiate():
    # Optionnel mais recommandé pour s'assurer d'un état propre lors du peuplement
    CarModel.objects.all().delete()
    CarMake.objects.all().delete()
    Dealer.objects.all().delete() # Supprimez les concessionnaires aussi si vous les recréez

    # Créez au moins un concessionnaire, car chaque CarModel doit en avoir un
    dealer1 = Dealer.objects.create(name="Premier Concessionnaire")
    dealer2 = Dealer.objects.create(name="Second Concessionnaire")
    # Ajoutez d'autres concessionnaires si vous le souhaitez

    # Données initiales pour les marques de voitures (CarMake)
    car_make_data = [
        {"name":"NISSAN", "description":"Great cars. Japanese technology"},
        {"name":"Mercedes", "description":"Great cars. German technology"},
        {"name":"Audi", "description":"Great cars. German technology"},
        {"name":"Kia", "description":"Great cars. Korean technology"},
        {"name":"Toyota", "description":"Great cars. Japanese technology"},
    ]

    # Crée et stocke les instances de CarMake
    car_make_instances = []
    for data in car_make_data:
        car_make_instances.append(CarMake.objects.create(name=data['name'], description=data['description']))

    # Données initiales pour les modèles de voitures (CarModel)
    car_model_data = [
      {"name":"Pathfinder", "type":"SUV", "year": 2023, "car_make":car_make_instances[0], "dealer": dealer1}, # <-- Ajout de "dealer"
      {"name":"Qashqai", "type":"SUV", "year": 2023, "car_make":car_make_instances[0], "dealer": dealer1},
      {"name":"XTRAIL", "type":"SUV", "year": 2023, "car_make":car_make_instances[0], "dealer": dealer2},
      {"name":"A-Class", "type":"SUV", "year": 2023, "car_make":car_make_instances[1], "dealer": dealer1},
      {"name":"C-Class", "type":"SUV", "year": 2023, "car_make":car_make_instances[1], "dealer": dealer2},
      {"name":"E-Class", "type":"SUV", "year": 2023, "car_make":car_make_instances[1], "dealer": dealer1},
      {"name":"A4", "type":"SUV", "year": 2023, "car_make":car_make_instances[2], "dealer": dealer2},
      {"name":"A5", "type":"SUV", "year": 2023, "car_make":car_make_instances[2], "dealer": dealer1},
      {"name":"A6", "type":"SUV", "year": 2023, "car_make":car_make_instances[2], "dealer": dealer2},
      {"name":"Sorrento", "type":"SUV", "year": 2023, "car_make":car_make_instances[3], "dealer": dealer1},
      {"name":"Carnival", "type":"SUV", "year": 2023, "car_make":car_make_instances[3], "dealer": dealer2},
      {"name":"Cerato", "type":"Sedan", "year": 2023, "car_make":car_make_instances[3], "dealer": dealer1},
      {"name":"Corolla", "type":"Sedan", "year": 2023, "car_make":car_make_instances[4], "dealer": dealer2},
      {"name":"Camry", "type":"Sedan", "year": 2023, "car_make":car_make_instances[4], "dealer": dealer1},
      {"name":"Kluger", "type":"SUV", "year": 2023, "car_make":car_make_instances[4], "dealer": dealer2},
    ]

    # Crée les instances de CarModel en passant le concessionnaire
    for data in car_model_data:
        CarModel.objects.create(
            name=data['name'],
            car_make=data['car_make'],
            type=data['type'],
            year=data['year'],
            dealer=data['dealer'] # <-- Assurez-vous que cette ligne est présente
        )
    print("Base de données populée avec succès !")