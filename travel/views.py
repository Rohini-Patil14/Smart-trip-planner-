from django.shortcuts import render
from django.shortcuts import render, redirect
from .models import AdminUser1, Destination1, DestinationImage1, Feedback,Hotel,Vehicle,Booking1
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
import random
from datetime import datetime
from django.db.models import Count, Sum
# 🔐 ADMIN LOGIN
from django.shortcuts import render, redirect
from .models import AdminUser1
from functools import wraps

from .models import Destination1, DestinationImage1, PlaceToVisit
# 🔐 LOGIN VIEW
def admin_login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('admin_logged_in'):
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper


# 🔐 LOGIN
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = AdminUser1.objects.get(username=username, password=password)

            request.session['admin_logged_in'] = True
            request.session['admin_name'] = user.username  # 👈 store name

            return redirect('admin_panel')

        except AdminUser1.DoesNotExist:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')


# 📊 DASHBOARD
from django.db.models import Avg, Sum
from django.contrib.auth.models import User

@admin_login_required
def admin_panel(request):

    total_destinations = Destination1.objects.count()
    total_feedback = Feedback.objects.count()
    avg_rating = Feedback.objects.aggregate(Avg('rating'))['rating__avg'] or 0

    # ✅ ADD THIS
    recent_bookings = Booking1.objects.select_related(
        'user', 'destination', 'vehicle'
    ).order_by('-id')[:5]

    return render(request, 'admin_panel.html', {
        'total_destinations': total_destinations,
        'total_feedback': total_feedback,
        'avg_rating': round(avg_rating, 1),
        'recent_bookings': recent_bookings   # 👈 IMPORTANT
    })

# 🚪 LOGOUT
def admin_logout(request):
    request.session.flush()
    return redirect('login')
# 
from django.db.models import Avg



def admin_logout(request):
    request.session.flush()   # clears session
    return redirect('login')

# def admin_panel(request):

#     if not request.session.get('admin_logged_in'):
#         return redirect('login')

#     # ADD DESTINATION
#     if request.method == 'POST':

#         destination = Destination1.objects.create(
#             name=request.POST.get('name'),
#             location=request.POST.get('location'),
#             description=request.POST.get('description'),
#             price=request.POST.get('price'),
#             rating=request.POST.get('rating'),
#             type=request.POST.get('type')
#         )

#         images = request.FILES.getlist('images')
#         for img in images:
#             DestinationImage1.objects.create(destination=destination, image=img)

#         return redirect('admin_panel')

    # FETCH FEEDBACK
   
def destinations(request):
    data = Destination1.objects.all()

    return render(request, 'destination2.html', {
        'destinations': data
    })

    
@admin_login_required


def add_destination(request):
    if request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('description')
        distance = request.POST.get('distance')
        type = request.POST.get('type')

        # ✅ Save Destination
        destination = Destination1.objects.create(
            name=name,
            description=description,
            distance=distance,
            type=type
        )

        # 🔥 Save Multiple Images
        images = request.FILES.getlist('images')
        for img in images:
            DestinationImage1.objects.create(
                destination=destination,
                image=img
            )

        # 🔥 Save Multiple Places
        places = request.POST.getlist('places')   # input name="places"
        for place in places:
            if place.strip():  # avoid empty values
                PlaceToVisit.objects.create(
                    destination=destination,
                    place_name=place
                )

        return render(request, 'add_destination.html', {'success': 'Added Successfully!'})

    return render(request, 'add_destination.html')

def destination_detail(request, id):
    destination = get_object_or_404(Destination1, id=id)

    return render(request, 'destination_detail.html', {
        'd': destination,
        'places': destination.places.all()   # ✅ fetch places
    })

def add_hotel(request):

    if not request.session.get('admin_logged_in'):
        return redirect('login')

    destinations = Destination1.objects.all()

    if request.method == 'POST':
        destination_id = request.POST.get('destination')

        Hotel.objects.create(
            destination_id=destination_id,
            name=request.POST.get('name'),
            total_rooms=request.POST.get('total_rooms'),
            price=request.POST.get('price'),
            image=request.FILES.get('image')
        )

        return redirect('admin_panel')

    return render(request, 'add_hotel.html', {
        'destinations': destinations
    })
from django.db.models import Sum
from datetime import datetime
from django.db.models import Q

def hotel_list(request):

    dest_id = request.GET.get('dest_id')
    vehicle_id = request.GET.get('vehicle_id')
    v_from = request.GET.get('v_from')
    v_to = request.GET.get('v_to')

    hotels = Hotel.objects.filter(destination_id=dest_id)

    if v_from and v_to:

        v_from_d = datetime.strptime(v_from, "%Y-%m-%d").date()
        v_to_d = datetime.strptime(v_to, "%Y-%m-%d").date()

        for h in hotels:

            # 🔥 total booked rooms in selected dates
            booked_rooms = Booking1.objects.filter(
                hotel=h
            ).filter(
                Q(h_from__lte=v_to_d) & Q(h_to__gte=v_from_d)
            ).aggregate(total=Sum('rooms_booked'))['total'] or 0

            # ✅ remaining rooms
            h.remaining_rooms = h.total_rooms - booked_rooms

    else:
        for h in hotels:
            h.remaining_rooms = h.total_rooms

    return render(request, 'hotels.html', {
        'hotels': hotels,
        'dest_id': dest_id,
        'vehicle_id': vehicle_id,
        'v_from': v_from,
        'v_to': v_to
    })
# views.py

from django.shortcuts import render, redirect
from .models import Vehicle
@admin_login_required
def add_vehicle(request):

    if request.method == "POST":
        name = request.POST.get('name')
        type = request.POST.get('type')
        seats = request.POST.get('seats')
        price = request.POST.get('price')
        description = request.POST.get('description')
        image = request.FILES.get('image')

        Vehicle.objects.create(
            name=name,
            type=type,
            seats=seats,
            price_per_km=price,
            description=description,
            image=image
        )

        return render(request, 'add_vehicle.html', {'success': "Vehicle Added Successfully ✅"})

    return render(request, 'add_vehicle.html')

from datetime import date, timedelta
from django.shortcuts import render
from .models import Vehicle, Booking,  Booking1,Destination1, Hotel


# 🔹 VEHICLE LIST
from datetime import date, timedelta
from django.shortcuts import render
from django.http import HttpResponse

from datetime import timedelta
from django.db.models import Q
from datetime import datetime, timedelta
from django.db.models import Q
from datetime import datetime, timedelta

from datetime import datetime, timedelta
from datetime import datetime, timedelta
from django.db.models import Q

# 🚗 VEHICLE LIST
def vehicle_list(request, dest_id):

    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')

    destination = Destination1.objects.get(id=dest_id)
    vehicles = Vehicle.objects.all()

    booked_vehicle_ids = []

    # ✅ BASE PRICE (ONLY distance)
    for v in vehicles:
        v.total_price = v.price_per_km * destination.distance

    # ✅ CHECK BOOKED VEHICLES
    if from_date and to_date:

        from_date_d = datetime.strptime(from_date, "%Y-%m-%d").date()
        to_date_d = datetime.strptime(to_date, "%Y-%m-%d").date()

        request_start = from_date_d - timedelta(days=2)
        request_end = to_date_d + timedelta(days=2)

        bookings = Booking1.objects.filter(
            v_from__lte=request_end,
            v_to__gte=request_start
        )

        booked_vehicle_ids = [b.vehicle.id for b in bookings]

    return render(request, 'vehicles.html', {
        'vehicles': vehicles,
        'booked_vehicle_ids': booked_vehicle_ids,
        'destination': destination,
        'from_date': from_date,
        'to_date': to_date
    })
# 🔹 BOOKING
def booking(request):
    place = request.GET.get('place')
    hotel_name = request.GET.get('hotel')
    vehicle_name = request.GET.get('vehicle')
    travel_date = request.GET.get('date')
    payment_method = request.GET.get('payment')
    # 🚫 Check empty date
    if not travel_date or travel_date.strip() == "":
        return HttpResponse("Please select travel date ❌")

    # 🚫 Validate date format
    try:
        travel_date_obj = date.fromisoformat(travel_date)
    except:
        return HttpResponse("Invalid date format ❌")

    # 🚫 Prevent past booking
    if travel_date_obj <= date.today():
        return HttpResponse("Date must be future ❌")

    # 🔍 Get objects
    try:
        destination = Destination1.objects.get(name=place)
        vehicle = Vehicle.objects.get(name=vehicle_name)
    except:
        return HttpResponse("Invalid data ❌")

    hotel = None
    if hotel_name:
        try:
            hotel = Hotel.objects.get(name=hotel_name)
        except:
            hotel = None

    # 🚫 Check vehicle already booked
    blocked = Booking.objects.filter(
        vehicle=vehicle,
        travel_date__range=[
            travel_date_obj,
            travel_date_obj + timedelta(days=2)
        ],
        status='booked'
    ).exists()

    if blocked:
        return HttpResponse("Vehicle already booked for this date ❌")

    # ✅ Create booking
    booking = Booking.objects.create(
        destination=destination,
        hotel=hotel,
        vehicle=vehicle,
        travel_date=travel_date_obj
    )

    return redirect(f'/booking-detail/{booking.id}/')


# 🔹 BOOKING DETAIL PAGE
def booking_detail(request, id):
    booking = get_object_or_404(Booking, id=id)
    return render(request, 'cancel_booking.html', {'booking': booking})

import random

# def booking_summary(request):
#     # 🔹 Get data from URL
#     place = request.GET.get('place')
#     hotel_name = request.GET.get('hotel')
#     vehicle_name = request.GET.get('vehicle')
#     date = request.GET.get('date')

#     # 🔹 Default values
#     vehicle_price = 0
#     hotel_price = 0
#     total_price = 0
#     distance = 0
#     price_per_km = 10

#     # 🚗 VEHICLE PRICE CALCULATION
#     if vehicle_name:
#         try:
#             vehicle = Vehicle.objects.get(name=vehicle_name)

#             # random distance (you can replace with real logic)
#             distance = random.randint(50, 300)

#             vehicle_price = distance * price_per_km

#         except Vehicle.DoesNotExist:
#             vehicle_price = 0

#     # 🏨 HOTEL PRICE CALCULATION
#     if hotel_name:
#         try:
#             hotel = Hotel.objects.get(name=hotel_name)

#             # ✅ If you want per day pricing
#             days = 1
#             if date:
#                 travel_date = datetime.strptime(date, "%Y-%m-%d").date()
#                 today = datetime.today().date()

#                 days = (travel_date - today).days
#                 if days <= 0:
#                     days = 1

#             hotel_price = hotel.price * days

#         except Hotel.DoesNotExist:
#             hotel_price = 0

#     # 💰 TOTAL PRICE
#     total_price = vehicle_price + hotel_price

#     # 🔹 Send to template
#     return render(request, 'booking_summery.html', {
#         'place': place,
#         'hotel': hotel_name,
#         'vehicle': vehicle_name,
#         'date': date,
#         'distance': distance,
#         'price_per_km': price_per_km,
#         'vehicle_price': vehicle_price,
#         'hotel_price': hotel_price,
#         'total_price': total_price,
#     })
from datetime import date
from django.shortcuts import render, get_object_or_404

def booking_summary(request):

    dest_id = request.GET.get('dest_id')
    vehicle_id = request.GET.get('vehicle_id')
    hotel_id = request.GET.get('hotel_id')

    v_from = date.fromisoformat(request.GET.get('v_from'))
    v_to = date.fromisoformat(request.GET.get('v_to'))

    destination = Destination1.objects.get(id=dest_id)
    vehicle = Vehicle.objects.get(id=vehicle_id)

    hotel = None
    if hotel_id and hotel_id != "none":
        hotel = Hotel.objects.get(id=hotel_id)

    days = (v_to - v_from).days
    if days <= 0:
        days = 1

    distance = destination.distance

    vehicle_cost = distance * vehicle.price_per_km * days
    hotel_cost = hotel.price * days if hotel else 0

    total = vehicle_cost + hotel_cost + 500

    return render(request, 'booking_summary.html', {
        'destination': destination,
        'vehicle': vehicle,
        'hotel': hotel,
        'vehicle_cost': vehicle_cost,
        'hotel_cost': hotel_cost,
        'total': total,
        'days': days
    })
def payment(request):
    place = request.GET.get('place')
    hotel = request.GET.get('hotel')
    vehicle = request.GET.get('vehicle')
    date = request.GET.get('date')
    amount = request.GET.get('amount')

    return render(request, 'payment.html', {
        'place': place,
        'hotel': hotel,
        'vehicle': vehicle,
        'date': date,
        'amount': amount
    })

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .models import UserProfile
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .models import UserProfile

def user_register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        photo = request.FILES.get("photo")

        # ❌ check user exists
        if User.objects.filter(username=username).exists():
            return render(request, "user_register.html", {"error": "Username already exists"})

        # ✅ create user
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email
        )

        # ✅ create profile manually
        UserProfile.objects.create(
            user=user,
            phone=phone,
            address=address,
            photo=photo
        )

        return redirect("user_login")

    return render(request, "user_register.html")
def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("/")   # index page
        else:
            return render(request, "user_login.html", {"error": "Invalid credentials"})

    return render(request, "user_login.html")

def user_logout(request):
    logout(request)
    return redirect("user_login")


def feedback_view(request):
    if request.method == "POST":
        rating = request.POST.get("rating")
        message = request.POST.get("message")

        Feedback.objects.create(
            user=request.user,
            rating=rating,
            message=message
        )

        return redirect("/")   # redirect after submit

    return render(request, "feedback.html")

def index(request):
    from .models import Feedback

    feedbacks = Feedback.objects.all()

    return render(request, "index.html", {"feedbacks": feedbacks})

from django.db.models import Sum

def available_rooms(hotel, h_from, h_to):

    bookings = Booking1.objects.filter(
        hotel=hotel,
        h_from__lt=h_to,
        h_to__gt=h_from
    )

    booked = bookings.aggregate(Sum('rooms_booked'))['rooms_booked__sum'] or 0

    return hotel.total_rooms - booked

from datetime import date
from django.shortcuts import render
from .models import Vehicle, Hotel, UserProfile
from datetime import date
from django.shortcuts import render
from .models import *

def booking_summary(request):

    dest_id = request.GET.get('dest_id')
    vehicle_id = request.GET.get('vehicle_id')
    hotel_id = request.GET.get('hotel_id')

    v_from = date.fromisoformat(request.GET.get('v_from'))
    v_to = date.fromisoformat(request.GET.get('v_to'))

    destination = Destination1.objects.get(id=dest_id)
    vehicle = Vehicle.objects.get(id=vehicle_id)

    hotel = None
    if hotel_id != "none":
        hotel = Hotel.objects.get(id=hotel_id)

    days = (v_to - v_from).days
    if days <= 0:
        days = 1

    distance = destination.distance

    vehicle_cost = distance * vehicle.price_per_km * days
    hotel_cost = hotel.price * days if hotel else 0

    total = vehicle_cost + hotel_cost + 500

    return render(request, 'booking_summary.html', {
        'destination': destination,
        'vehicle': vehicle,
        'hotel': hotel,
        'vehicle_cost': vehicle_cost,
        'hotel_cost': hotel_cost,
        'total': total,
        'days': days
    })

    
from django.shortcuts import render
from datetime import datetime
from django.shortcuts import render, redirect
from datetime import datetime

from datetime import datetime


# 📄 BOOKING SUMMARY
def booking_summary(request):

    dest_id = request.GET.get('dest_id')
    vehicle_id = request.GET.get('vehicle_id')
    hotel_id = request.GET.get('hotel_id')

    v_from = request.GET.get('v_from')
    v_to = request.GET.get('v_to')

    destination = Destination1.objects.get(id=dest_id)
    vehicle = Vehicle.objects.get(id=vehicle_id)

    hotel = None
    if hotel_id and hotel_id != "none":
        hotel = Hotel.objects.get(id=hotel_id)
    
    # ✅ DATE CALCULATION
    v_from_d = datetime.strptime(v_from, "%Y-%m-%d").date()
    v_to_d = datetime.strptime(v_to, "%Y-%m-%d").date()

    days = (v_to_d - v_from_d).days + 1

    # ✅ FINAL PRICE (distance × rate × days)
    distance = destination.distance
    rate = vehicle.price_per_km

    vehicle_cost = rate * distance * days

    # ✅ HOTEL COST
    rooms = int(request.GET.get('rooms', 1))
    hotel_cost = hotel.price * days * rooms if hotel else 0

    total = vehicle_cost + hotel_cost

    return render(request, "booking_summary.html", {
        "destination": destination,
        "vehicle": vehicle,
        "hotel": hotel,
        "days": days,
        "vehicle_cost": vehicle_cost,
        "hotel_cost": hotel_cost,
        "total": total,
        "v_from": v_from,
        "v_to": v_to,
        "distance": distance,
        "rooms": rooms
    })


# ✅ CONFIRM BOOKING (SAVE TO DB)
def confirm_booking(request):

    if request.method == "POST":

        dest_id = request.POST.get('dest_id')
        vehicle_id = request.POST.get('vehicle_id')
        hotel_id = request.POST.get('hotel_id')

        v_from = request.POST.get('v_from')
        v_to = request.POST.get('v_to')

        destination = Destination1.objects.get(id=dest_id)
        vehicle = Vehicle.objects.get(id=vehicle_id)

        hotel = None
        if hotel_id and hotel_id != "none":
            hotel = Hotel.objects.get(id=hotel_id)

        # ✅ DATE
        v_from_d = datetime.strptime(v_from, "%Y-%m-%d").date()
        v_to_d = datetime.strptime(v_to, "%Y-%m-%d").date()

        days = (v_to_d - v_from_d).days + 1

        # ✅ FINAL PRICE AGAIN (IMPORTANT)
        distance = destination.distance
        rate = vehicle.price_per_km

        vehicle_cost = rate * distance * days
        rooms = int(request.POST.get('rooms', 1))
        hotel_cost = hotel.price * days * rooms if hotel else 0

        total = vehicle_cost + hotel_cost

        # ✅ SAVE BOOKING
        Booking1.objects.create(
        user=request.user,
        destination=destination,   
        vehicle=vehicle,
        hotel=hotel,
        v_from=v_from_d,
        v_to=v_to_d,
        h_from=v_from_d,
        h_to=v_to_d,
        rooms_booked=rooms,
        total_amount=total,
        status='booked'
)

        return redirect('my_bookings')

    return redirect('/')

def my_bookings(request):

    if not request.user.is_authenticated:
        return redirect('/ulogin')

    bookings = Booking1.objects.filter(user=request.user).order_by('-id')

    return render(request, 'my_bookings.html', {
        'bookings': bookings
    })

from datetime import date

def cancel_booking(request, booking_id):

    booking = Booking1.objects.get(id=booking_id)

    # 🚨 prevent cancelling again
    if booking.status == "cancelled":
        return redirect('my_bookings')

    today = date.today()

    # days before travel
    days_left = (booking.v_from - today).days

    refund = 0

    # 🎯 REFUND LOGIC
    if days_left >= 3:
        refund = booking.total_amount * 0.9   # 90%
    elif days_left == 2:
        refund = booking.total_amount * 0.5   # 50%
    else:
        refund = 0   # no refund

    # ✅ update booking
    booking.status = "cancelled"
    booking.refund_amount = refund
    booking.save()

    return redirect('my_bookings')

def view_destinations(request):
    destinations = Destination1.objects.all()
    return render(request, 'view_destinations.html', {'destinations': destinations})

def delete_destination(request, id):
    dest = Destination1.objects.get(id=id)
    dest.delete()
    return redirect('view_destinations')
def edit_destination(request, id):
    dest = Destination1.objects.get(id=id)

    if request.method == "POST":
        dest.name = request.POST.get('name')
        dest.description = request.POST.get('description')
        dest.distance = request.POST.get('distance')
        dest.type = request.POST.get('type')
        dest.save()

        # ✅ ADD NEW IMAGES ONLY
        files = request.FILES.getlist('images')
        for file in files:
            DestinationImage1.objects.create(
                destination=dest,
                image=file
            )

        return redirect('view_destinations')

    return render(request, 'edit_destination.html', {'d': dest})

def view_hotels(request):
    hotels = Hotel.objects.select_related('destination').all()
    return render(request, 'view_hotels.html', {'hotels': hotels})
def edit_hotel(request, id):
    hotel = Hotel.objects.get(id=id)
    destinations = Destination1.objects.all()

    if request.method == "POST":
        hotel.destination_id = request.POST.get('destination')
        hotel.name = request.POST.get('name')
        hotel.total_rooms = request.POST.get('total_rooms')
        hotel.price = request.POST.get('price')

        # ✅ ONLY update image if new one uploaded
        if request.FILES.get('image'):
            hotel.image = request.FILES.get('image')

        hotel.save()
        return redirect('view_hotels')

    return render(request, 'edit_hotel.html', {
        'hotel': hotel,
        'destinations': destinations
    })
def delete_hotel(request, id):
    hotel = Hotel.objects.get(id=id)
    hotel.delete()
    return redirect('view_hotels')

# VIEW VEHICLES
@admin_login_required
def view_vehicles(request):
    vehicles = Vehicle.objects.all()
    return render(request, 'view_vehicles.html', {'vehicles': vehicles})


# DELETE VEHICLE
@admin_login_required
def delete_vehicle(request, id):
    vehicle = Vehicle.objects.get(id=id)
    vehicle.delete()
    return redirect('view_vehicles')


# EDIT VEHICLE
@admin_login_required
def edit_vehicle(request, id):
    vehicle = Vehicle.objects.get(id=id)

    if request.method == "POST":
        vehicle.name = request.POST.get('name')
        vehicle.type = request.POST.get('type')
        vehicle.seats = request.POST.get('seats')
        vehicle.price_per_km = request.POST.get('price')
        vehicle.description = request.POST.get('description')

        # ✅ update image only if new uploaded
        if request.FILES.get('image'):
            vehicle.image = request.FILES.get('image')

        vehicle.save()
        return redirect('view_vehicles')

    return render(request, 'edit_vehicle.html', {'vehicle': vehicle})

# VIEW FEEDBACK
@admin_login_required
def view_feedback(request):
    feedbacks = Feedback.objects.all().order_by('-created_at')
    return render(request, 'view_feedback.html', {'feedbacks': feedbacks})


# DELETE FEEDBACK
@admin_login_required
def delete_feedback(request, id):
    feedback = Feedback.objects.get(id=id)
    feedback.delete()
    return redirect('view_feedback')

from django.contrib.auth.models import User
from .models import UserProfile

# 👀 VIEW USERS
@admin_login_required
def view_users(request):
    users = User.objects.all()
    return render(request, 'view_users.html', {'users': users})


# ✏️ EDIT USER
@admin_login_required
def edit_user(request, id):
    user = User.objects.get(id=id)
    profile = UserProfile.objects.get(user=user)

    if request.method == "POST":
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.save()

        profile.phone = request.POST.get('phone')
        profile.address = request.POST.get('address')

        if request.FILES.get('photo'):
            profile.photo = request.FILES.get('photo')

        profile.save()

        return redirect('view_users')

    return render(request, 'edit_user.html', {
        'user': user,
        'profile': profile
    })


# ❌ DELETE USER
@admin_login_required
def delete_user(request, id):
    user = User.objects.get(id=id)
    user.delete()
    return redirect('view_users')


def how_it_works(request):
    return render(request, 'how_it_works.html')


from django.contrib import messages

def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # You can save to DB or print
        print(name, email, subject, message)

        messages.success(request, "Message sent successfully!")
        return redirect('contact')

    return render(request, 'contact.html')


###################Report----------------------------
def feedback_report(request):
    feedbacks = Feedback.objects.select_related('user').all().order_by('-created_at')

    # Average Rating
    avg_rating = Feedback.objects.aggregate(avg=Avg('rating'))['avg']

    context = {
        'feedbacks': feedbacks,
        'avg_rating': avg_rating
    }
    return render(request, 'feedback_report.html', context)

def user_report(request):
    users = None
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')

    if from_date and to_date:
        users = UserProfile.objects.select_related('user').filter(
            user__date_joined__date__range=[from_date, to_date]
        ).order_by('-user__date_joined')

    context = {
        'users': users,
        'from_date': from_date,
        'to_date': to_date
    }
    return render(request, 'user_report.html', context)


def booking_report(request):
    bookings = None
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')

    if from_date and to_date:
        bookings = Booking1.objects.select_related(
            'user', 'destination', 'vehicle', 'hotel'
        ).filter(
            v_from__range=[from_date, to_date]
        ).order_by('-v_from')

        # Total Revenue
        total_revenue = bookings.aggregate(total=Sum('total_amount'))['total']
    else:
        total_revenue = None

    context = {
        'bookings': bookings,
        'from_date': from_date,
        'to_date': to_date,
        'total_revenue': total_revenue
    }

    return render(request, 'booking_report.html', context)

def vehicle_booking_report(request):
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')

    bookings = Booking1.objects.all()

    # Filter by date range
    if from_date and to_date:
        bookings = bookings.filter(v_from__range=[from_date, to_date])

    # Group by vehicle
    report = bookings.values(
        'vehicle__name',
        'vehicle__type'
    ).annotate(
        total_bookings=Count('id'),
        total_earning=Sum('total_amount')
    ).order_by('-total_bookings')

    context = {
        'report': report,
        'from_date': from_date,
        'to_date': to_date
    }

    return render(request, 'vehicle_booking_report.html', context)

def hotel_report(request):
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')

    bookings = Booking1.objects.exclude(hotel=None)

    # Date filter (using hotel booking date)
    if from_date and to_date:
        bookings = bookings.filter(h_from__range=[from_date, to_date])

    # Group by hotel
    report = bookings.values(
        'hotel__name',
        'hotel__destination__name'
    ).annotate(
        total_bookings=Count('id'),
        total_rooms=Sum('rooms_booked'),
        total_earning=Sum('total_amount')
    ).order_by('-total_bookings')

    context = {
        'report': report,
        'from_date': from_date,
        'to_date': to_date
    }

    return render(request, 'hotel_report.html', context)

def destination_report(request):
    destinations = Destination1.objects.all()

    query = request.GET.get('q', '')
    dest_type = request.GET.get('type', '')

    # 🔍 Search filter
    if query:
        destinations = destinations.filter(name__icontains=query)

    # 🔽 Type filter
    if dest_type and dest_type.strip() != "":
        destinations = destinations.filter(type__iexact=dest_type)

    context = {
        'destinations': destinations,
    }

    return render(request, 'destination_report.html', context)