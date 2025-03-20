from django.urls import path, include
from weerstation import views
from rest_framework.routers import DefaultRouter
from .views import SensorDataViewSet
from .views import RegenMetingViewSet

router = DefaultRouter()
router.register(r'sensordata', SensorDataViewSet)
router.register(r'regenmetingen', RegenMetingViewSet)

urlpatterns = [
    path('regenmetingen/', views.regen_data_view, name='regenmetingen'),
    path('check_status/', views.check_status, name='check_status'),
    path('stop_task/', views.stop_task, name='stop_task'),
    path('api/', include(router.urls)),
    
]