#!/bin/bash

# Wacht een paar seconden om er zeker van te zijn dat alle systemen klaar zijn
sleep 10

echo "Django wordt gestart..."

# Ga naar de projectdirectory
cd /home/JasperLanoote/pidjango

# Activeer de virtuele omgeving
source /home/JasperLanoote/pidjango/djenv/bin/activate

sleep 5

# Start de Django server
nohup python manage.py runserver 0.0.0.0:8000 > /home/JasperLanoote/pidjango/server.log 2>&1 &

sleep 5

# Start de loops
nohup python manage.py start_loop > /home/JasperLanoote/pidjango/loop.log 2>&1 &

sleep 5

# Start het loggen van sensor data
nohup python manage.py log_sensor_data > /home/JasperLanoote/pidjango/sensor.log 2>&1 &


echo "Django server en processen zijn gestart!"

echo "React app wordt gestart..."

cd /home/JasperLanoote/pidjango/react_website

# Start de React-app
nohup npm run dev > /home/JasperLanoote/pidjango/react_website/react.log 2>&1 &

echo "React app is gestart!"
