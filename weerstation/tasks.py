import RPi.GPIO as GPIO
import time
from weerstation.models import RegenMeting  # Importeer het model

# GPIO-instellingen
GPIO.setmode(GPIO.BCM)
button_pin = 22  # GPIO-pin voor de drukknop
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Variabelen
calibratie_factor = 132  # Aantal keer knop ingedrukt per 100 mm regen
running = True  # Variabele om de lus te stoppen

def start_loop():
    """
    Start de main loop die de drukknop gedurende een minuut monitort en de regenval opslaat in de database.
    """
    global running
    try:
        while running:
            # Start een minuut lang tellen
            counter = 0  # Teller voor knopindrukken
            previous_button_state = GPIO.LOW  # Bijhouden van vorige knopstatus
            start_time = time.time()  # Starttijd van de minuut

            print("Start met tellen gedurende een minuut...")
            while time.time() - start_time < 60:  # 60 seconden loop
                # Lees de status van de drukknop
                button_state = GPIO.input(button_pin)

                # Controleer of de knop is ingedrukt (van LOW naar HIGH)
                if button_state == GPIO.HIGH and previous_button_state == GPIO.LOW:
                    counter += 1

                # Update de vorige status van de knop
                previous_button_state = button_state

                # Wacht even om te voorkomen dat de loop te snel draait
                time.sleep(0.1)

            # Bereken de regenval na 1 minuut
            regenval = counter * (100 / calibratie_factor)
            tijdstip = time.strftime("%Y-%m-%d %H:%M:%S")  # Huidig tijdstip

            # Opslaan in de database
            RegenMeting.objects.create(regenval=regenval)
            print(f"Tijdstip: {tijdstip}, Totaal aantal drukken: {counter}, Regenval: {regenval:.2f} mm")
            print("Regenval is opgeslagen in de database.")
            
    except KeyboardInterrupt:
        stop_loop()
    except Exception as e:
        print(f"Er trad een fout op: {e}")
        stop_loop()

def stop_loop():
    """
    Stop de main loop en maak de GPIO schoon.
    """
    global running
    running = False
    GPIO.cleanup()
    print("De weerstation lus is gestopt en GPIO is opgeruimd.")
