import json
import board
import adafruit_bme680
import Adafruit_ADS1x15
from channels.generic.websocket import AsyncWebsocketConsumer
import asyncio
from .models import SensorData
from asgiref.sync import sync_to_async

# Setup ADS1115 
adc = Adafruit_ADS1x15.ADS1115(address=0x48, busnum=1)
GAIN = 1  

# Initialiseer de I2C bus van de BME680
i2c = board.I2C()
sensor = adafruit_bme680.Adafruit_BME680_I2C(i2c)

class SensorConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.running = True
        asyncio.create_task(self.send_sensor_data())

    async def disconnect(self, close_code):
        self.running = False

    async def send_sensor_data(self):
        while self.running:
            try:
                # Lees sensorwaarden asynchroon uit
                temperature = await asyncio.to_thread(lambda: sensor.temperature)
                humidity = await asyncio.to_thread(lambda: sensor.humidity)
                pressure = await asyncio.to_thread(lambda: sensor.pressure)
                gas = await asyncio.to_thread(lambda: sensor.gas)

                # Correcte uitlezing van ADS1115
                value = await asyncio.to_thread(lambda: adc.read_adc_difference(0, GAIN))
                voltage = round(value * (4.096 / 32768.0), 4)

                min_volt = 0.97
                max_volt = 4.7

                min_wind = 0
                max_wind = 35

                # Berekening windsnelheid consistent houden
                windsnelheid_ms = ((voltage - min_volt) * (max_wind - min_wind) / (max_volt - min_volt)) + min_wind
                windsnelheid_ms = max(windsnelheid_ms, 0)

                # Data opslaan in de database
                await self.save_sensor_data(temperature, humidity, pressure, gas, windsnelheid_ms)

                # Verzenden naar WebSocket-client
                data = {
                    "temperature": round(temperature, 2),
                    "humidity": round(humidity, 2),
                    "pressure": round(pressure, 2),
                    "gas": round(gas, 2),
                    "wind_speed_kmh": round(windsnelheid_ms, 2)
                }

                await self.send(json.dumps(data))
                await asyncio.sleep(5)

            except Exception as e:
                import traceback
                error_message = traceback.format_exc()
                await self.send(json.dumps({"error": error_message}))
                self.running = False

    @sync_to_async
    def save_sensor_data(self, temperature, humidity, pressure, gas, wind_speed_kmh):
        """Slaat sensordata asynchroon op in de database"""
        SensorData.objects.create(
            temperature=temperature,
            humidity=humidity,
            pressure=pressure,
            gas=gas,
            wind_speed_kmh=wind_speed_kmh
        )
