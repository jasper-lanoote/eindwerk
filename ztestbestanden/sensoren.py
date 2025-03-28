import time
import board
import adafruit_bme680
import Adafruit_ADS1x15
import asyncio
import websockets
import json

# Setup ADS1115 
adc = Adafruit_ADS1x15.ADS1115(address=0x48, busnum=1)
GAIN = 1  

# Initialiseer de I2C bus van de BME680
i2c = board.I2C()
sensor = adafruit_bme680.Adafruit_BME680_I2C(i2c)

# WebSocket URL van de server
ws_url = "ws://localhost:8000/ws/upload/"  # Pas dit aan naar je WebSocket-URL

async def ping(websocket):
    try:
        while True:
            await websocket.ping()
            await asyncio.sleep(30)
    except Exception as e:
        print(f"Ping error: {e}")

async def send_sensor_data():
    while True:
        try:
            # Lees sensorwaarden uit
            temperature = round(sensor.temperature, 1)
            humidity = round(sensor.humidity )
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
            async with websockets.connect(ws_url) as websocket:
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

# Start de WebSocket communicatie
asyncio.run(send_sensor_data())
