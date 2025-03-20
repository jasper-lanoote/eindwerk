# Wind speed = (Output voltage - 0.4) / 1.6 * 32.4
import time
import Adafruit_ADS1x15

# Create an ADS1115 object, explicitly specifying the bus number
adc = Adafruit_ADS1x15.ADS1115(address=0x48, busnum=1)  # Address may vary depending on your setup

GAIN = 1  # Set gain value
channel = 0  # A0 is channel 0

while True:
    raw_value = adc.read_adc(channel, gain=GAIN)
    voltage = raw_value * (4.096 / 32767.0)  # Convert to voltage
    wind_speed = ((voltage - 0.4) / 1.6 * 32.4)
    wind_speedkmh = wind_speed * 3.6
    print(f'{wind_speedkmh:.4F} km/h {voltage:.4F}')
    time.sleep(1)
