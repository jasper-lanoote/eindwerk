import time
import Adafruit_ADS1x15

# Maak een object voor de ADS1115
adc = Adafruit_ADS1x15.ADS1115(address=0x48, busnum=1)

# Stel de gain in via de constructor, bijvoorbeeld voor een bereik van ±4.096V (GAIN = 1)
GAIN = 1  # Dit kan worden aangepast afhankelijk van je spanningsbereik

def read_voltage():
    # Lees het verschil tussen A0 en A1 (verschilmodus)
    # value = adc.read_adc_difference(0, 1, gain=GAIN)
    value = adc.read_adc_difference(0,gain=GAIN)
    # Omrekeningen:
    # Het bereik van de ADS1115 is van -32768 tot 32767 voor 16 bits. De referentie is 4.096V voor de standaard gain.
    voltage = value * (4.096 / 32768.0)  # Schaal de waarde naar spanning
    
    min_volt = 0.97
    max_volt = 4.7

    min_wind = 0
    max_wind = 35

    windsnelheid = ((voltage - min_volt) * (max_wind - min_wind) / (max_volt - min_volt)) + min_wind

    windsnelheid = max(windsnelheid, 0)
    
    return windsnelheid

while True:
    voltage = read_voltage()
    print(f"Spanning tussen A0 en A1: {voltage:.4f} m/s")
    time.sleep(1)


