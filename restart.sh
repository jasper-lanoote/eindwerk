#!/bin/bash

# 🔴 Stop de Django-server en gerelateerde processen
echo "Zoeken naar draaiende Django-processen..."

# Vind de process ID (PID) van de Django-server en stop deze
ps aux | grep 'manage.py runserver' | grep -v grep | awk '{print $2}' | xargs kill -9

# Stop eventuele andere Django-processen (start_loop, log_sensor_data)
ps aux | grep 'manage.py start_loop' | grep -v grep | awk '{print $2}' | xargs kill -9
ps aux | grep 'manage.py log_sensor_data' | grep -v grep | awk '{print $2}' | xargs kill -9

echo "Django-processen gestopt."

# 🔴 Stop de React-app als die nog draait
echo "Zoeken naar draaiende React-processen..."

ps aux | grep 'npm run dev' | grep -v grep | awk '{print $2}' | xargs kill -9

echo "React-processen gestopt."

# Wacht een paar seconden om ervoor te zorgen dat alles is afgesloten
sleep 5

# 🚀 Start de Django-server opnieuw
echo "Django wordt opnieuw gestart..."

# Ga naar de projectdirectory
cd /home/JasperLanoote/pidjango

# Activeer de virtuele omgeving
source /home/JasperLanoote/pidjango/djenv/bin/activate

sleep 2

# Start de Django-server opnieuw
nohup python manage.py runserver 0.0.0.0:8000 > /home/JasperLanoote/pidjango/server.log 2>&1 &

sleep 3

# Start de loops opnieuw
nohup python manage.py start_loop > /home/JasperLanoote/pidjango/loop.log 2>&1 &

sleep 3

# Start het loggen van sensor data opnieuw
nohup python manage.py log_sensor_data > /home/JasperLanoote/pidjango/sensor.log 2>&1 &

echo "Django server en processen zijn opnieuw gestart!"

# 🚀 Start de React-app opnieuw
echo "React-app wordt opnieuw gestart..."

cd /home/JasperLanoote/pidjango/react_website

# Start de React-app
nohup npm run dev > /home/JasperLanoote/pidjango/react_website/react.log 2>&1 &

echo "React-app is opnieuw gestart!"
