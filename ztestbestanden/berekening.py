
volt = 0.97 + (4.7 - 0.97) * 0.5

min_volt = 0.97
max_volt = 4.7

min_wind = 0
max_wind = 35

snelheid_wind = ((volt - min_volt) * (max_wind - min_wind) / (max_volt - min_volt)) + min_wind

print(snelheid_wind)
