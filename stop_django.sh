#!/bin/bash

echo "Bezig met stoppen van Django-processen..."

# Zoek en stop alle processen die manage.py uitvoeren
PIDS=$(ps aux | grep manage.py | grep -v grep | awk '{print $2}')

if [ -z "$PIDS" ]; then
    echo "Geen draaiende Django-processen gevonden."
else
    echo "Django-processen stoppen..."
    kill -9 $PIDS
    echo "Alle Django-processen zijn gestopt!"
fi
