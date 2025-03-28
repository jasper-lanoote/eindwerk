import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
import websockets
import logging
from .models import SensorData, RegenMeting
from django.utils import timezone

# Configureer logging
logger = logging.getLogger(__name__)

# WebSocket URL voor de display
DISPLAY_WS_URL = "ws://192.168.0.232:8001/ws/display/"

class SensorUpload(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        logger.info("WebSocket connected for uploading data")

    async def disconnect(self, close_code):
        logger.info(f"WebSocket disconnected with close code {close_code}")

    async def receive(self, text_data):
        try:
            # Parse de ontvangen data
            data = json.loads(text_data)
            logger.info(f"Ontvangen data via WebSocket: {data}")

            # Haal de waarden op uit het bericht
            temperature = data.get('temperature')
            humidity = data.get('humidity')
            pressure = data.get('pressure')
            gas = data.get('gas')
            wind_speed_kmh = data.get('wind_speed_kmh')

            # Valideer de data
            if None not in (temperature, humidity, pressure, gas, wind_speed_kmh):
                # Data is geldig, sla op in de database
                logger.info("Data is geldig, wordt opgeslagen in de database")
                await self.save_to_db(
                    temperature=temperature,
                    humidity=humidity,
                    pressure=pressure,
                    gas=gas,
                    wind_speed_kmh=wind_speed_kmh
                )

                # Bevestiging sturen naar de client
                await self.send(text_data=json.dumps({
                    'status': 'success',
                    'temperature': temperature,
                    'humidity': humidity,
                    'pressure': pressure,
                    'gas': gas,
                    'wind_speed_kmh': wind_speed_kmh
                }))

                # Verstuur data naar de display WebSocket
                await self.send_to_display_ws({
                    'temperature': temperature,
                    'humidity': humidity,
                    'pressure': pressure,
                    'gas': gas,
                    'wind_speed_kmh': wind_speed_kmh
                })

                # Verstuur data naar alle `SensorReader` clients
                await self.broadcast_to_readers({
                    'temperature': temperature,
                    'humidity': humidity,
                    'pressure': pressure,
                    'gas': gas,
                    'wind_speed_kmh': wind_speed_kmh
                })

            else:
                logger.warning("Ongeldige data ontvangen!")
                await self.send(text_data=json.dumps({
                    'status': 'error',
                    'message': 'Invalid data'
                }))

        except json.JSONDecodeError as e:
            logger.error(f"Fout in het verwerken van de data: {e}")
            await self.send(text_data=json.dumps({
                'status': 'error',
                'message': 'Invalid JSON format'
            }))
        except Exception as e:
            logger.error(f"Onverwachte fout: {str(e)}")
            await self.send(text_data=json.dumps({
                'status': 'error',
                'message': 'Error processing data'
            }))

    async def save_to_db(self, temperature, humidity, pressure, gas, wind_speed_kmh):
        try:
            sensor_data = await SensorData.objects.acreate(
                temperature=temperature,
                humidity=humidity,
                pressure=pressure,
                gas=gas,
                wind_speed_kmh=wind_speed_kmh,
                timestamp=timezone.localtime(timezone.now())
            )
            logger.info(f"Data succesvol opgeslagen in de database: {sensor_data}")
        except Exception as e:
            logger.error(f"Error bij het opslaan in de database: {str(e)}")

    async def send_to_display_ws(self, data):
        try:
            async with websockets.connect(DISPLAY_WS_URL) as display_ws:
                await display_ws.send(json.dumps(data))
                logger.info(f"Verstuurd naar display WebSocket: {data}")

        except Exception as e:
            logger.error(f"Fout bij verbinding met display WebSocket: {e}")

    async def broadcast_to_readers(self, data):
        channel_layer = get_channel_layer()
        await channel_layer.group_send(
            "sensor_readers",  # Stuur naar de readers groep
            {
                'type': 'send.sensor.data',
                'data': data
            }
        )

class SensorReader(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        logger.info("WebSocket connected for reading sensor data")

        # Voeg de client toe aan de 'sensor_readers' groep
        await self.channel_layer.group_add(
            "sensor_readers",
            self.channel_name
        )

    async def disconnect(self, close_code):
        logger.info(f"WebSocket disconnected with close code {close_code}")

        # Verwijder de client uit de groep
        await self.channel_layer.group_discard(
            "sensor_readers",
            self.channel_name
        )

    async def receive(self, text_data):
        # Optioneel: Log ontvangen berichten
        logger.info(f"Received data in reader: {text_data}")

    # Deze methode ontvangt data vanuit de channel layer
    async def send_sensor_data(self, event):
        data = event['data']
        await self.send(text_data=json.dumps(data))

class RegenSensorUpload(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        logger.info("WebSocket connected for rain sensor data")

    async def disconnect(self, close_code):
        logger.info(f"WebSocket disconnected with close code {close_code}")

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            logger.info(f"Ontvangen regenval data: {data}")

            regenval = data.get("regenval")
            tijdstip = data.get("tijdstip")

            if regenval is not None:
                # Sla op in de database
                await self.save_to_db(regenval, tijdstip)

                # Bevestiging naar client
                await self.send(json.dumps({
                    "status": "success",
                    "regenval": regenval,
                    "tijdstip": tijdstip
                }))
            else:
                logger.warning("Ongeldige regenval data ontvangen!")
                await self.send(json.dumps({
                    "status": "error",
                    "message": "Invalid data"
                }))

        except json.JSONDecodeError as e:
            logger.error(f"JSON-fout: {e}")
            await self.send(json.dumps({
                "status": "error",
                "message": "Invalid JSON format"
            }))
        except Exception as e:
            logger.error(f"Fout bij verwerken van data: {e}")
            await self.send(json.dumps({
                "status": "error",
                "message": "Error processing data"
            }))

    async def save_to_db(self, regenval, tijdstip):
        try:
            regen_meting = await RegenMeting.objects.acreate(
                regenval=regenval,
                tijdstip=timezone.now()
            )
            logger.info(f"Regenval opgeslagen in database: {regen_meting}")
        except Exception as e:
            logger.error(f"Fout bij opslaan in database: {e}")