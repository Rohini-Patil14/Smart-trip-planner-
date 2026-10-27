from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def index(request):
    return render(request, "index.html")

# def destinations(request):
#     return render(request, "destinations.html")
def destination_list(request):
    return render(request, 'destination2.html')

def plan_trip(request):
    return render(request, "plan_trip.html")

def plan_trip1(request):
    return render(request, "plan_trip1.html")

def itinerary(request):
    return render(request, "itinerary.html")

def auth(request):
    return render(request, "auth.html")

def register_user(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=email).exists():
            messages.error(request, "Email already exists")
            return redirect('auth')

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=name
        )
        user.save()

        messages.success(request, "Registration Successful")
        return redirect('auth')


# LOGIN
# def login_user(request):
#     if request.method == "POST":
#         email = request.POST.get('email')
#         password = request.POST.get('password')

#         user = authenticate(request, username=email, password=password)

#         if user is not None:
#             login(request, user)
#             return redirect('index')   # homepage
#         else:
#             messages.error(request, "Invalid credentials")
#             return redirect('auth')


# LOGOUT
def logout_user(request):
    logout(request)
    return redirect('auth')

def transport(request):
    return render(request, 'transport.html')

# def hotels(request):
#     return render(request, 'hotels.html')

def hotels(request):
    place = request.GET.get('place')

    hotel_data = {
        "Goa": [
            {"name": "Sea View Resort", "price": 3000, "img": "images/goa_hotel1.jpg"},
            {"name": "Beach Paradise", "price": 4500, "img": "images/goa_hotel2.jpg"},
        ],
        "Manali": [
            {"name": "Snow Valley Hotel", "price": 2500, "img": "images/manali_hotel1.jpg"},
            {"name": "Hill Top Resort", "price": 3500, "img": "images/manali_hotel2.jpg"},
        ],
        "Kashmir": [
            {"name": "Dal Lake View", "price": 4000, "img": "images/kashmir_hotel1.jpg"},
            {"name": "Heaven Stay", "price": 5000, "img": "images/kashmir_hotel2.jpg"},
        ],
        "Jaipur": [
            {"name": "Royal Palace Hotel", "price": 3200, "img": "images/jaipur_hotel1.jpg"},
            {"name": "Pink City Stay", "price": 2800, "img": "images/jaipur_hotel2.jpg"},
        ],
    }

    hotels = hotel_data.get(place, [])

    return render(request, 'hotels.html', {'hotels': hotels, 'place': place})

def places(request):
    place = request.GET.get('place')

    places_data = {
        "Goa": [
            {"name": "Baga Beach", "img": "images/goa1.jpg"},
            {"name": "Calangute Beach", "img": "images/goa2.jpg"},
            {"name": "Fort Aguada", "img": "images/goa3.jpg"},
        ],
        "Manali": [
            {"name": "Solang Valley", "img": "images/manali1.jpg"},
            {"name": "Rohtang Pass", "img": "images/manali2.jpg"},
        ],
        "Kashmir": [
            {"name": "Dal Lake", "img": "images/kashmir1.jpg"},
            {"name": "Gulmarg", "img": "images/kashmir2.jpg"},
        ],
        "Jaipur": [
            {"name": "Hawa Mahal", "img": "images/jaipur1.jpg"},
            {"name": "Amber Fort", "img": "images/jaipur2.jpg"},
        ],
    }

    tourist_places = places_data.get(place, [])

    return render(request, 'places.html', {
        'places': tourist_places,
        'place': place
    })

def guides(request):
    return render(request, 'guides.html')

def feedback(request):
    return render(request, 'feedback.html')


# def itinerary(request):

#     source = request.GET.get('source')
#     destination = request.GET.get('destination')
#     date = request.GET.get('date')
#     travelers = request.GET.get('travelers')
#     budget = request.GET.get('budget')

#     context = {
#         "source": source,
#         "destination": destination,
#         "date": date,
#         "travelers": travelers,
#         "budget": budget
#     }

#     return render(request, "itinerary.html", context)

def packages(request):
    return render(request, "packages.html")

def about(request):
    return render(request, "about.html")

def contact(request):
    return render(request, "contact.html")