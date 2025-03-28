from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('Weerstation/', include('weerstation.urls')),
]
  # path('EnergieManagement/',include('DigitaleMeter.urls')),