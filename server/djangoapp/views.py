from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from datetime import datetime

from django.http import JsonResponse
from django.contrib.auth import login, authenticate
import logging
import json
from django.views.decorators.csrf import csrf_exempt
from .populate import initiate
from .models import CarMake, CarModel
# Importation nécessaire pour get_request, analyze_review_sentiments, post_review
from .restapis import get_request, analyze_review_sentiments, post_review

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

@csrf_exempt
def login_user(request):
    # Get username and password from request.POST dictionary
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    # Try to check if provide credential can be authenticated
    user = authenticate(username=username, password=password)
    data = {"userName": username}
    if user is not None:
        # If user is valid, call login method to login current user
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
    return JsonResponse(data)


def logout_request(request):
    logout(request)  # Terminate user session
    data = {"userName": ""}  # Return empty username
    return JsonResponse(data)


@csrf_exempt
def registration(request):
    context = {}

    # Load JSON data from the request body
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    first_name = data['firstName']
    last_name = data['lastName']
    email = data['email']
    username_exist = False
    email_exist = False
    try:
        # Check if user already exists
        User.objects.get(username=username)
        username_exist = True
    except:
        # If not, simply log this is a new user
        logger.debug("{} is new user".format(username))

    # If it is a new user
    if not username_exist:
        # Create user in auth_user table
        user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, password=password, email=email)
        # Login the user and redirect to list page
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
        return JsonResponse(data)
    else:
        data = {"userName": username, "error": "Already Registered"}
        return JsonResponse(data)


def get_cars(request):
    # Compte le nombre d'objets CarMake dans la base de données.
    count = CarMake.objects.filter().count()
    print(count)  # Affiche le compte dans la console du serveur

    # Si aucune marque de voiture n'existe (count est 0),
    # appelle la fonction initiate() pour peupler la base de données.
    if (count == 0):
        initiate()

    # Récupère tous les objets CarModel et optimise la requête
    # en préchargeant les objets CarMake liés (select_related).
    car_models = CarModel.objects.select_related('car_make')

    # Crée une liste vide pour stocker les données des voitures.
    cars = []

    # Parcourt chaque CarModel récupéré.
    for car_model in car_models:
        # Pour chaque CarModel, ajoute un dictionnaire à la liste 'cars'.
        # Ce dictionnaire contient le nom du modèle de voiture et le nom de sa marque.
        cars.append({"CarModel": car_model.name, "CarMake": car_model.car_make.name})

    # Retourne la liste des voitures sous forme de réponse JSON.
    return JsonResponse({"CarModels": cars})


def get_dealerships(request, state="All"):
    if (state == "All"):
        endpoint = "/fetchDealers"
    else:
        endpoint = "/fetchDealers/" + str(state)
    dealerships = get_request(endpoint)
    return JsonResponse({"status": 200, "dealers": dealerships})


# Create a `get_dealer_details` view to render the dealer details
def get_dealer_details(request, dealer_id):
    # Si un dealer_id est fourni dans la requête
    if (dealer_id):
        # Construit le endpoint pour l'API externe
        endpoint = "/fetchDealer/" + str(dealer_id)
        # Utilise get_request de restapis.py pour récupérer les détails du concessionnaire
        dealership = get_request(endpoint)
        # Retourne les détails du concessionnaire en JSON
        return JsonResponse({"status": 200, "dealer": dealership})
    else:
        # Si aucun dealer_id n'est fourni, retourne une erreur
        return JsonResponse({"status": 400, "message": "Bad Request - Dealer ID is missing"})


# Create a `get_dealer_reviews` view to render the reviews of a dealer
def get_dealer_reviews(request, dealer_id):
    # if dealer id has been provided
    if (dealer_id):
        endpoint = "/fetchReviews/dealer/" + str(dealer_id)
        reviews = get_request(endpoint)
        for review_detail in reviews:
            # Assurez-vous que 'review' est la clé correcte pour le texte de l'avis
            if 'review' in review_detail:
                response = analyze_review_sentiments(review_detail['review'])
                print(response)
                # Assurez-vous que 'sentiment' est la clé attendue du service d'analyse
                if response and 'sentiment' in response:
                    review_detail['sentiment'] = response['sentiment']
                else:
                    review_detail['sentiment'] = "N/A" # Gérer les cas où le sentiment n'est pas trouvé
            else:
                review_detail['sentiment'] = "No review text" # Gérer les cas où il n'y a pas de texte d'avis
        return JsonResponse({"status": 200, "reviews": reviews})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request - Dealer ID is missing"})


@csrf_exempt # Nécessaire pour les requêtes POST
def add_review(request):
    if (request.user.is_anonymous == False):
        data = json.loads(request.body)
        try:
            response = post_review(data) # Assurez-vous que 'post_review' est correctement implémenté dans restapis.py
            return JsonResponse({"status": 200, "message": "Review posted successfully"})
        except Exception as e: # Capturer l'exception pour un meilleur débogage
            return JsonResponse({"status": 401, "message": f"Error in posting review: {e}"})
    else:
        return JsonResponse({"status": 403, "message": "Unauthorized - User is anonymous"})