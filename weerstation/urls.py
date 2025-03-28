from django.urls import path, include
from weerstation import views
from rest_framework.routers import DefaultRouter
from .views import SensorDataViewSet
from .views import RegenMetingViewSet

router = DefaultRouter()
router.register(r'sensordata', SensorDataViewSet)
router.register(r'regenmetingen', RegenMetingViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]