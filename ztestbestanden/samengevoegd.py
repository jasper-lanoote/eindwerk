import time
import board
import adafruit_bme680
import Adafruit_ADS1x15

# setup ADS1115 
adc = Adafruit_ADS1x15.ADS1115(address=0x48, busnum=1)  # Address van ads1115 digital converter
GAIN = 1  # Set gain value
channel = 0  # A0 is channel 0


# Initialiseer de I2C bus van de bme680
i2c = board.I2C()  
sensor = adafruit_bme680.Adafruit_BME680_I2C(i2c)

# Functie om de sensor te lezen
def read_sensor():
    try:
        # Lees de temperatuur, vochtigheid, luchtdruk en gas (luchtkwaliteit)
        temperature = sensor.temperature
        humidity = sensor.humidity
        pressure = sensor.pressure
        gas = sensor.gas
        print("-"*40)
        print(f"Temperatuur: {temperature:.2f} C")
        print(f"Vochtigheid: {humidity:.2f} %")
        print(f"Luchtdruk: {pressure:.2f} hPa")
        print(f"Gas (luchtkwaliteit): {gas} ohms")
        print("-" * 40)

    except Exception as e:
        print(f"Fout bij het uitlezen van de sensor: {e}")

def read_windspeed():
    raw_value = adc.read_adc(channel, gain=GAIN)
    voltage = raw_value * (4.096 / 32767.0)  # Convert to voltage
    wind_speed = ((voltage - 0.4) / 1.6 * 32.4)
    wind_speedkmh = wind_speed * 3.6
    
    print(f'windsnelheid: {wind_speedkmh:.4F} km/h')
    time.sleep(1)

# Lezen van de sensor in een loop
while True:
    read_sensor()
    read_windspeed()
    #windrichting
    #hoeveelheid regen
    time.sleep(2)  # Wacht 2 seconden tussen elke meting
