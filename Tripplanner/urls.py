"""
URL configuration for Tripplanner project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from Tripplanner import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('travel.urls')),

    path('', views.index, name="index"),
    path('destinations/', views.destination_list, name='destinations'),
    path('plan_trip', views.plan_trip, name="plan_trip"),
    path('plan_trip1', views.plan_trip1, name="plan_trip1"),
    path('itinerary', views.itinerary, name="itinerary"),
    path('packages', views.packages, name="packages"),
    path('about', views.about, name="about"),
    path('contact', views.contact, name="contact"),
    path('auth', views.auth, name="auth"),
    path('register/', views.register_user, name="register"),
    # path('login/', views.login_user, name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('transport/', views.transport, name='transport'),
    path('hotels/', views.hotels, name='hotels'),
    path('guides/', views.guides, name='guides'),
    path('places/', views.places, name='places'),
    path('feedback/', views.feedback, name='feedback'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)