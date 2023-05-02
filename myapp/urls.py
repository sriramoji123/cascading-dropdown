from django.urls import path
from . import views

urlpatterns = [
    path('', views.address, name='address'),
    path('load-states/', views.load_states, name='ajax_load_states'),
    path('load-cities/', views.load_cities, name='ajax_load_cities'),
]
