from django.urls import path

from src.couriers.controllers.couriers import CouriersController

urlpatterns = [
    path('service<int:num>/', CouriersController.as_view({'post': 'create'})),
]
