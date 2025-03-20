#!/bin/bash

# Stop de Django-server en gerelateerde processen
echo "Zoeken naar draaiende Django-processen..."

# Vind de process ID (PID) van de Django server en stop deze
ps aux | grep 'manage.py runserver' | awk '{print $2}' | xargs kill -9

# Stop eventuele andere processen die je hebt gestart (bijv. start_loop, log_sensor_data)
ps aux | grep 'manage.py start_loop' | awk '{print $2}' | xargs kill -9
ps aux | grep 'manage.py log_sensor_data' | awk '{print $2}' | xargs kill -9

echo "Django processen gestopt."

# Wacht een paar seconden om ervoor te zorgen dat alle processen zijn gestopt
sleep 5

# Start de Django-server opnieuw
echo "Django wordt opnieuw gestart..."

# Ga naar de projectdirectory
cd /home/JasperLanoote/pidjango

# Activeer de virtuele omgeving
source /home/JasperLanoote/pidjango/djenv/bin/activate

sleep 2

# Start de Django server opnieuw
nohup python manage.py runserver 0.0.0.0:8000 > /home/JasperLanoote/pidjango/server.log 2>&1 &

sleep 3

# Start de loops opnieuw
nohup python manage.py start_loop > /home/JasperLanoote/pidjango/loop.log 2>&1 &

sleep 3

# Start het loggen van sensor data opnieuw
nohup python manage.py log_sensor_data > /home/JasperLanoote/pidjango/sensor.log 2>&1 &

echo "Django server en processen zijn opnieuw gestart!"
