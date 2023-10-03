from django.urls import path
from .views import insurancebot 

urlpatterns = [
    path('',insurancebot),
]