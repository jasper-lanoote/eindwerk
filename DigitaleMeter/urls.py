from django.urls import path
from . import views

urlpatterns = [
    #path('DigitaleMeter/' ,views.DigitaleMeter),
    path('DigitaleMeter_dummy/' ,views.DigitaleMeter_dummy),
    path('website/', views.home , name='home'),
]