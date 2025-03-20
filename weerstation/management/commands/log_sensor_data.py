import time
import board
import adafruit_bme680
import Adafruit_ADS1x15
from django.core.management.base import BaseCommand
from weerstation.models import SensorData

class Command(BaseCommand):
    help = "Log sensor data to the database continuously"

    def handle(self, *args, **kwargs):
        adc = Adafruit_ADS1x15.ADS1115(address=0x48, busnum=1)
        GAIN = 1  
      
        i2c = board.I2C()
        sensor = adafruit_bme680.Adafruit_BME680_I2C(i2c)

        self.stdout.write("Logging sensor data. Press Ctrl+C to stop.")

        try:
            while True:
                temperature = round(sensor.temperature, 2)
                humidity = round(sensor.humidity, 2)
                pressure = round(sensor.pressure, 2)
                gas = round(sensor.gas, 2)
                
                value = adc.read_adc_difference(0, gain=GAIN)
                voltage = value * (4.096 / 32768.0) 
                min_volt = 0.97
                max_volt = 4.7

                min_wind = 0
                max_wind = 35

                windsnelheid = ((voltage - min_volt) * (max_wind - min_wind) / (max_volt - min_volt)) + min_wind
                windsnelheid = max(windsnelheid, 0)
                windsnelheid_kmph = round(windsnelheid * 3.6, 2)  # Beperk tot 2 decimalen

                # Opslaan in database
                SensorData.objects.create(
                    temperature=temperature,
                    humidity=humidity,
                    pressure=pressure,
                    gas=gas,
                    wind_speed_kmh=windsnelheid_kmph
                )

                # Log data in console (beperkt tot 2 decimalen)
                self.stdout.write(
                    f"Data opgeslagen: Temp={temperature:.2f}, Wind={windsnelheid_kmph:.2f} km/h"
                )

                time.sleep(2)  # Interval aanpassen naar wens
                
        except KeyboardInterrupt:
            self.stdout.write("Sensor logging gestopt.")
