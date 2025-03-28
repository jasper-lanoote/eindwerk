#!/bin/bash

echo "Bezig met stoppen van Django-, React- en Python-processen..."

# 🔴 Zoek en stop Django-processen
DJANGO_PIDS=$(ps aux | grep 'python manage.py runserver' | grep -v grep | awk '{print $2}')

if [ -z "$DJANGO_PIDS" ]; then
    echo "Geen draaiende Django-processen gevonden."
else
    echo "Django-processen stoppen..."
    kill -9 $DJANGO_PIDS
    echo "Django-processen zijn gestopt!"
fi

# Stop het Python-script alles_uitlezen.py
PYTHON_PIDS=$(ps aux | grep "python /home/JasperLanoote/pidjango/weerstation/alles_uitlezen.py" | grep -v grep | awk '{print $2}')

if [ -z "$PYTHON_PIDS" ]; then
    echo "Geen draaiende Python-processen gevonden (alles_uitlezen.py)."
else
    echo "Python-processen stoppen..."
    kill -9 $PYTHON_PIDS
    echo "Python-processen zijn gestopt!"
fi

# Zoek en stop React-processen
REACT_PIDS=$(ps aux | grep 'npm run dev' | grep -v grep | awk '{print $2}')

if [ -z "$REACT_PIDS" ]; then
    echo "Geen draaiende React-processen gevonden."
else
    echo "React-processen stoppen..."
    kill -9 $REACT_PIDS
    echo "React-processen zijn gestopt!"
fi

# Wacht een paar seconden om er zeker van te zijn dat alles is afgesloten
sleep 5

# Start de Django-server opnieuw
echo "Django wordt opnieuw gestart..."

# Ga naar de projectdirectory
cd /home/JasperLanoote/pidjango

# Activeer de virtuele omgeving
source /home/JasperLanoote/pidjango/djenv/bin/activate

sleep 2

# Start Django server
nohup python manage.py runserver 0.0.0.0:8000 > /home/JasperLanoote/pidjango/logs/server.log 2>&1 &

sleep 3

echo " Django-server is opnieuw gestart!"

# Start het Python-script alles_uitlezen.py opnieuw
echo "Python script alles_uitlezen.py wordt opnieuw gestart..."

nohup python /home/JasperLanoote/pidjango/weerstation/alles_uitlezen.py > /home/JasperLanoote/pidjango/logs/alles_uitlezen.log 2>&1 &

sleep 3

echo " Python-script alles_uitlezen.py is opnieuw gestart!"

# Start de React-app opnieuw
echo "React-app wordt opnieuw gestart..."

cd /home/JasperLanoote/pidjango/react_website

# Start React-app
nohup npm run dev > /home/JasperLanoote/pidjango/logs/react.log 2>&1 &

echo "React-app is opnieuw gestart!"

echo " Alle processen zijn succesvol herstart!"
