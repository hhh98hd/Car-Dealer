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


# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

# Create a `login_request` view to handle sign in request
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

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    data = {"userName": ""}

    return JsonResponse(data)

# Create a `registration` view to handle sign up request
@csrf_exempt
def registration(request):
    req_data = json.loads(request.body)
    
    username = req_data['userName']
    password = req_data['password']
    first_name = req_data['firstName']
    last_name = req_data['lastName']
    email = req_data['email']
    
    user_exists = User.objects.filter(username=username).exists()
    if user_exists:
        data = {"userName":username,"error":"Already Registered"}
        return JsonResponse(data)
    else:
        new_user = User.objects.create_user(username=username,
                                            first_name=first_name,
                                            last_name=last_name,
                                            password=password,
                                            email=email)
        login(request, new_user)
        data = {"userName":username,"status":"Authenticated"}
        return JsonResponse(data)
        
def get_cars(request):    
    manifacturer_num = CarMake.objects.filter().count()
    
    if 0 == manifacturer_num:
        initiate()
    
    car_models = CarModel.objects.select_related('car_make')
    
    cars = []
    for car_model in car_models:
        cars.append({"CarModel": car_model.name, "CarMake": car_model.car_make.name})
        
    return JsonResponse({"CarModels": cars})
