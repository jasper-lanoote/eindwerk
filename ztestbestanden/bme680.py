import time
import board
import adafruit_bme680

# Initialiseer de I2C bus
i2c = board.I2C()  # Standaard I2C bus op de Raspberry Pi
sensor = adafruit_bme680.Adafruit_BME680_I2C(i2c)

# Functie om de sensor te lezen
def read_sensor():
    try:
        # Lees de temperatuur, vochtigheid, luchtdruk en gas (luchtkwaliteit)
        temperature = sensor.temperature
        humidity = sensor.humidity
        pressure = sensor.pressure
        gas = sensor.gas

        print(f"Temperatuur: {temperature:.2f} C")
        print(f"Vochtigheid: {humidity:.2f} %")
        print(f"Luchtdruk: {pressure:.2f} hPa")
        print(f"Gas (luchtkwaliteit): {gas} ohms")
        print("-" * 40)

    except Exception as e:
        print(f"Fout bij het uitlezen van de sensor: {e}")

# Lezen van de sensor in een loop
while True:
    read_sensor()
    time.sleep(2)  # Wacht 2 seconden tussen elke meting
