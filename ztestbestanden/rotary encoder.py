import RPi.GPIO as GPIO
import time

# Definieer de GPIO-pinnen
PIN_A = 17
PIN_B = 27

# Encoder specificaties
PULSES_PER_REV = 600  # Pulsen per omwenteling
DEGREES_PER_PULSE = 360 / PULSES_PER_REV  # 0.6° per puls

# Huidige positie
position = 0

# GPIO-instellingen
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN_A, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(PIN_B, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Callback-functie voor het afhandelen van interrupts
def rotary_callback(channel):
    global position
    A_state = GPIO.input(PIN_A)
    B_state = GPIO.input(PIN_B)

    if A_state == B_state:
        position += 1  # Draait rechtsom (clockwise)
    else:
        position -= 1  # Draait linksom (counterclockwise)

    # Bereken graden
    angle = position * DEGREES_PER_PULSE
    print(f"Encoder positie: {position} pulsen, {angle:.1f}°")

# Interrupts instellen
GPIO.add_event_detect(PIN_A, GPIO.BOTH, callback=rotary_callback, bouncetime=2)

try:
    while True:
        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nProgramma gestopt.")
    GPIO.cleanup()
