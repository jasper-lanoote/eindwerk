import asyncio
import json
import time
import websockets
import RPi.GPIO as GPIO

# GPIO-instellingen
GPIO.setmode(GPIO.BCM)
button_pin = 22  # GPIO-pin voor de drukknop
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# WebSocket URL voor het versturen van regenval-data
REGEN_WS_URL = "ws://192.168.0.232:8000/ws/regensensor/"

# Variabelen
calibratie_factor = 132  # Aantal keer knop ingedrukt per 100 mm regen
running = True

async def send_regen_data():
    global running
    try:
        while running:
            # Start een minuut lang tellen
            counter = 0
            previous_button_state = GPIO.LOW
            start_time = time.time()

            print("Start met tellen gedurende een minuut...")

            while time.time() - start_time < 60:
                button_state = GPIO.input(button_pin)

                if button_state == GPIO.HIGH and previous_button_state == GPIO.LOW:
                    counter += 1

                previous_button_state = button_state
                time.sleep(0.1)

            # Bereken regenval
            regenval = counter * (100 / calibratie_factor)
            tijdstip = time.strftime("%Y-%m-%d %H:%M:%S")

            # Verstuur data via WebSocket
            data = {
                "regenval": round(regenval, 2),
                "tijdstip": tijdstip
            }

            print(f"Tijdstip: {tijdstip}, Totaal aantal drukken: {counter}, Regenval: {regenval:.2f} mm")

            await send_to_websocket(data)

    except KeyboardInterrupt:
        stop_loop()
    except Exception as e:
        print(f"Er trad een fout op: {e}")
        stop_loop()

async def send_to_websocket(data):
    try:
        async with websockets.connect(REGEN_WS_URL) as websocket:
            await websocket.send(json.dumps(data))
            print(f"Verstuurd naar RegenSensorUpload WebSocket: {data}")
    except Exception as e:
        print(f"Fout bij het verbinden met de WebSocket: {e}")

def stop_loop():
    global running
    running = False
    GPIO.cleanup()
    print("De regensensor lus is gestopt en GPIO is opgeruimd.")

def start_loop():
    asyncio.run(send_regen_data())

if __name__ == "__main__":
    try:
        start_loop()
    except KeyboardInterrupt:
        stop_loop()
