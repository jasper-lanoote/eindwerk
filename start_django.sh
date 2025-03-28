#!/bin/bash

# Wacht een paar seconden om er zeker van te zijn dat alle systemen klaar zijn
sleep 10

# Zorg ervoor dat de logs directory bestaat
mkdir -p /home/JasperLanoote/pidjango/logs
chmod 777 /home/JasperLanoote/pidjango/logs

echo "Django wordt gestart..."

# Ga naar de projectdirectory
cd /home/JasperLanoote/pidjango

# Activeer de virtuele omgeving
source /home/JasperLanoote/pidjango/djenv/bin/activate

# Controleer of de juiste Python- en Django-versie beschikbaar zijn
echo "Python gebruikt: $(which python)"
echo "Django versie: $(python -m django --version)"

sleep 3

# Start de Django server
nohup /home/JasperLanoote/pidjango/djenv/bin/python manage.py runserver 0.0.0.0:8000 > /home/JasperLanoote/pidjango/logs/server.log 2>&1 || echo "FOUT: Django server kon niet worden gestart. Zie logs voor details." &

sleep 5

echo "Django server en processen zijn gestart!"

echo "Python script wordt gestart..."

# Start het Python script alles_uitlezen.py
nohup /home/JasperLanoote/pidjango/djenv/bin/python /home/JasperLanoote/pidjango/weerstation/alles_uitlezen.py > /home/JasperLanoote/pidjango/logs/alles_uitlezen.log 2>&1 || echo "FOUT: alles_uitlezen.py kon niet worden gestart. Zie logs voor details." &

echo "Python script is gestart!"

echo "React app wordt gestart..."

# Ga naar React directory
cd /home/JasperLanoote/pidjango/react_website

sleep 3

# Start de React-app
nohup npm run dev > /home/JasperLanoote/pidjango/logs/react.log 2>&1 || echo "FOUT: React-app kon niet worden gestart. Zie logs voor details." &

echo "React app is gestart!"

# Wacht even om te zorgen dat alles goed opgestart is
sleep 10
