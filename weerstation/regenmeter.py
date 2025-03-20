import RPi.GPIO as GPIO
import time
from django.utils import timezone
from weerstation.models import RegenMeting

# Stel de pinmodus in
GPIO.setmode(GPIO.BCM)

# Definieer de GPIO-pin voor de drukknop
button_pin = 22

# Stel de pin in als input met een pull-down weerstand
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Initialiseer de teller
counter = 0

# Calibratiefactor (aantal keer knop ingedrukt per 100 mm regen)
calibratie_factor = 132  # Pas deze waarde aan voor calibratie

# Variabele om de vorige status van de knop bij te houden
previous_button_state = GPIO.LOW

# Variabele om de tijd van de laatste meting bij te houden
last_measurement_time = time.time()

try:
    while True:
        # Lees de status van de drukknop
        button_state = GPIO.input(button_pin)
        
        # Controleer of de knop is ingedrukt (van LOW naar HIGH)
        if button_state == GPIO.HIGH and previous_button_state == GPIO.LOW:
            counter += 1
        
        # Update de vorige status van de knop
        previous_button_state = button_state
        
        # Controleer of er 60 seconden zijn verstreken sinds de laatste meting
        current_time = time.time()
        if current_time - last_measurement_time >= 60:
            # Bereken de regenval in de afgelopen minuut
            regenval = counter * (100 / calibratie_factor)
            # Sla de meting op in de database
            RegenMeting.objects.create(tijdstip=timezone.now(), regenval=regenval)
            
            # Reset de teller en de tijd van de laatste meting
            counter = 0
            last_measurement_time = current_time
        
        # Wacht even om te voorkomen dat de loop te snel draait
        time.sleep(0.1)

except KeyboardInterrupt:
    # Opruimen bij het afsluiten van het programma
    GPIO.cleanup()
    print("Programma afgesloten.")