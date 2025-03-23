#!/bin/bash

echo "Bezig met stoppen van Django- en React-processen..."

# 🔴 Zoek en stop alle processen die manage.py uitvoeren (Django)
PIDS=$(ps aux | grep manage.py | grep -v grep | awk '{print $2}')

if [ -z "$PIDS" ]; then
    echo "Geen draaiende Django-processen gevonden."
else
    echo "Django-processen stoppen..."
    kill -9 $PIDS
    echo "Alle Django-processen zijn gestopt!"
fi

# 🔴 Zoek en stop alle processen die npm run dev uitvoeren (React)
REACT_PIDS=$(ps aux | grep "npm run dev" | grep -v grep | awk '{print $2}')

if [ -z "$REACT_PIDS" ]; then
    echo "Geen draaiende React-processen gevonden."
else
    echo "React-processen stoppen..."
    kill -9 $REACT_PIDS
    echo "Alle React-processen zijn gestopt!"
fi

echo "Alle processen zijn gestopt!"
