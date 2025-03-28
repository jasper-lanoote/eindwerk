import asyncio
import json
import time
import websockets
import RPi.GPIO as GPIO
import threading
import board
import adafruit_bme680
import Adafruit_ADS1x15

# GPIO-instellingen voor regen sensor
GPIO.setmode(GPIO.BCM)
button_pin = 22  # GPIO-pin voor de drukknop
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# WebSocket URL voor het versturen van regenval-data
REGEN_WS_URL = "ws://localhost:8000/ws/regensensor/"

# Variabelen voor de regen sensor
calibratie_factor = 132  # Aantal keer overgeschakeld per 100 mm regen
running = True

# Setup ADS1115 voor windsnelheid met de ADS1115 module
adc = Adafruit_ADS1x15.ADS1115(address=0x48, busnum=1)
GAIN = 1  

# Initialiseer de I2C bus voor de BME680 sensor
i2c = board.I2C()
sensor = adafruit_bme680.Adafruit_BME680_I2C(i2c)

# WebSocket URL van de server voor sensor data
SENSOR_WS_URL = "ws://localhost:8000/ws/upload/"

# Functie om ping-berichten naar de WebSocket server te sturen
async def ping(websocket):
    try:
        while True:
            await websocket.ping()
            await asyncio.sleep(30)
    except Exception as e:
        print(f"Ping error: {e}")

# Functie om sensor data te sturen via WebSocket
async def send_sensor_data():
    while True:
        try:
            # Lees sensorwaarden uit
            temperature = round(sensor.temperature, 1)
            humidity = round(sensor.humidity)
            pressure = round(sensor.pressure, 2)
            gas = round(sensor.gas, 2)

            # Lees de waarde van de ADS1115 en bereken de windsnelheid
            value = adc.read_adc_difference(0, gain=GAIN)
            voltage = value * (4.096 / 32768.0)
            min_volt = 0.97
            max_volt = 4.7
            min_wind = 0
            max_wind = 35

            windsnelheid = ((voltage - min_volt) * (max_wind - min_wind) / (max_volt - min_volt)) + min_wind
            windsnelheid = max(windsnelheid, 0)
            windsnelheid_kmph = round(windsnelheid * 3.6, 2)  # km/h

            # Maak een dictionary met de data
            data = {
                "temperature": temperature,
                "humidity": humidity,
                "pressure": pressure,
                "gas": gas,
                "wind_speed_kmh": windsnelheid_kmph
            }

            # Open de WebSocket-verbinding
            async with websockets.connect(SENSOR_WS_URL) as websocket:
                # Start een aparte taak voor pings
                ping_task = asyncio.create_task(ping(websocket))

                # Stuur de sensor data naar de WebSocket
                await websocket.send(json.dumps(data))
                print(f"Sent data: {data}")

                # Wacht een paar seconden voor de volgende meting
                await asyncio.sleep(3)

                # Stop de ping-taak na het verzenden van data
                ping_task.cancel()
                try:
                    await ping_task
                except asyncio.CancelledError:
                    pass

        except Exception as e:
            print(f"Error: {e}")
            await asyncio.sleep(5)  # Even wachten voordat je het opnieuw probeert

# Functie om regenval data te sturen via WebSocket
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
                await asyncio.sleep(0.1)  # Gebruik asyncio.sleep in plaats van time.sleep

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

# Stop de regensensor lus
def stop_loop():
    global running
    running = False
    GPIO.cleanup()
    print("De regensensor lus is gestopt en GPIO is opgeruimd.")

# Start beide taken in afzonderlijke threads
def start_threads():
    sensor_thread = threading.Thread(target=lambda: asyncio.run(send_sensor_data()))
    regen_thread = threading.Thread(target=lambda: asyncio.run(send_regen_data()))
    sensor_thread.start()
    regen_thread.start()
    sensor_thread.join()
    regen_thread.join()

if __name__ == "__main__":
    try:
        start_threads()  # Start beide taken in verschillende threads
    except KeyboardInterrupt:
        stop_loop()
