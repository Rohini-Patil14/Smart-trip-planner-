from django.db import models
from datetime import date, timedelta
# 🔐 ADMIN USER
# class AdminUser(models.Model):
#     username = models.CharField(max_length=50, unique=True)
#     password = models.CharField(max_length=100)

#     def __str__(self):
#         return self.username
class AdminUser1(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.username

# # 🌍 DESTINATION
class Destination1(models.Model):

    TYPE_CHOICES = [
        ('beach', 'Beach'),
        ('city', 'City'),
        ('hill', 'Hill'),
    ]

    name = models.CharField(max_length=100)

    # ❌ removed location
    description = models.TextField()

    distance = models.FloatField()  # ✅ distance in KM

    type = models.CharField(max_length=20, choices=TYPE_CHOICES)

    def __str__(self):
        return self.name
    
class PlaceToVisit(models.Model):
    destination = models.ForeignKey(Destination1, on_delete=models.CASCADE, related_name='places')
    place_name = models.CharField(max_length=100)

    def __str__(self):
        return self.place_name


# 🖼 MULTIPLE IMAGES
class DestinationImage1(models.Model):
    destination = models.ForeignKey(Destination1, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='destinations/')


# models.py

class Hotel(models.Model):
    destination = models.ForeignKey(Destination1, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    total_rooms = models.IntegerField()
    price = models.IntegerField()
    image = models.ImageField(upload_to='hotels/')

    def __str__(self):
        return self.name
    
class Vehicle(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50)  # Car, SUV, Bus
    seats = models.IntegerField()
    price_per_km = models.FloatField()
    image = models.ImageField(upload_to='vehicles/')
    description = models.TextField()

from django.db import models
from datetime import date

class Booking(models.Model):
    destination = models.ForeignKey(Destination1, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.SET_NULL, null=True, blank=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)

    travel_date = models.DateField()
    booking_date = models.DateField(auto_now_add=True)

    STATUS = [
        ('booked', 'Booked'),
        ('cancelled', 'Cancelled')
    ]
    status = models.CharField(max_length=20, choices=STATUS, default='booked')
    payment_method = models.CharField(max_length=20, default='cash')
    def __str__(self):
        return f"{self.destination.name} - {self.vehicle.name}"
    


from django.contrib.auth.models import User 
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)

    def __str__(self):
        return self.user.username
    
class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    
class Booking1(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    destination = models.ForeignKey('Destination1', on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, null=True, blank=True)
    v_from = models.DateField()
    v_to = models.DateField()

    h_from = models.DateField()
    h_to = models.DateField()

    rooms_booked = models.IntegerField(default=1)

    total_amount = models.FloatField(default=0)

    status = models.CharField(max_length=20, default='booked')
    refund_amount = models.FloatField(default=0) 
    def __str__(self):
        return f"{self.user.username} - ₹{self.total_amount}"
    

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200, blank=True, null=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name