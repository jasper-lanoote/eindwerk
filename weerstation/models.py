from django.db import models
from django.utils import timezone

class RegenMeting(models.Model):
    tijdstip = models.DateTimeField(blank=True)  # We verwijderen auto_now_add
    regenval = models.FloatField(help_text="Regenval in mm")

    def save(self, *args, **kwargs):
        if not self.tijdstip:  # Stel de tijd in als deze nog niet is ingesteld
            self.tijdstip = timezone.localtime(timezone.now())  # Converteer naar lokale tijd
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.tijdstip}: {self.regenval} mm"

class WindMeting(models.Model):
    tijdstip = models.DateTimeField(blank=True)  # We verwijderen auto_now_add
    windsnelheid = models.FloatField(help_text="snelheid in km/h")

    def save(self, *args, **kwargs):
        if not self.tijdstip:  # Stel de tijd in als deze nog niet is ingesteld
            self.tijdstip = timezone.localtime(timezone.now())  # Converteer naar lokale tijd
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.tijdstip}: {self.windsnelheid} km/h"

class SensorData(models.Model):
    timestamp = models.DateTimeField(blank=True)  # We verwijderen auto_now_add
    temperature = models.FloatField()
    humidity = models.FloatField()
    pressure = models.FloatField()
    gas = models.FloatField()
    wind_speed_kmh = models.FloatField()

    def save(self, *args, **kwargs):
        if not self.timestamp:  # Stel de tijd in als deze nog niet is ingesteld
            self.timestamp = timezone.localtime(timezone.now())  # Converteer naar lokale tijd
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.timestamp} - Temp: {self.temperature}°C, Wind: {self.wind_speed_kmh} km/h"
