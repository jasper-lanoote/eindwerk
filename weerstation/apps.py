from django.apps import AppConfig
from django.db.backends.signals import connection_created
from django.utils.autoreload import restart_with_reloader
import threading

# class WeerstationConfig(AppConfig):
#     default_auto_field = "django.db.models.BigAutoField"
#     name = "weerstation"

#     loop_started =False 
    
#     def ready(self):
#         """
#         Start de achtergrondthread pas nadat de databaseverbinding is opgezet.
#         """
#         from .tasks import start_loop  # Import hier om de fout te vermijden

#         # Controleer of de app herstart om dubbele threads te vermijden
#         if threading.active_count() == 1:  # Alleen starten als geen andere thread loopt
#             thread = threading.Thread(target=start_loop, daemon=True)
#             thread.start()
#             print("Achtergrondloop gestart.")
