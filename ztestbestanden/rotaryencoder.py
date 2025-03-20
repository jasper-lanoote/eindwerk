import RPi.GPIO as GPIO
import time

# Definieer de pinnen
encoder_Pin_1 = 17  # GPIO 17
encoder_Pin_2 = 27  # GPIO 27

# Counts Per Revolution (CPR)
CPR = 1900  # 2400 Counts Per Revolution (CPR)
degrees_per_count = 360 / CPR  # Bereken graden per count

lastEncoded = 0
encoderValue = 0

lastMSB = 0
lastLSB = 0

def setup():
    GPIO.setmode(GPIO.BCM)
    print(f"Setting up pins {encoder_Pin_1} and {encoder_Pin_2}")
    GPIO.setup(encoder_Pin_1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(encoder_Pin_2, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    try:
        GPIO.add_event_detect(encoder_Pin_1, GPIO.BOTH, callback=updateEncoder)
        GPIO.add_event_detect(encoder_Pin_2, GPIO.BOTH, callback=updateEncoder)
        print("Event detection successfully added")
    except RuntimeError as e:
        print(f"Failed to add event detection: {e}")

def updateEncoder(channel):
    global lastEncoded, encoderValue

    MSB = GPIO.input(encoder_Pin_1)
    LSB = GPIO.input(encoder_Pin_2)

    encoded = (MSB << 1) | LSB
    sum = (lastEncoded << 2) | encoded

    if sum == 0b1101 or sum == 0b0100 or sum == 0b0010 or sum == 0b1011:
        encoderValue += 1
    if sum == 0b1110 or sum == 0b0111 or sum == 0b0001 or sum == 0b1000:
        encoderValue -= 1

    lastEncoded = encoded

def loop():
    while True:
        # Bereken de hoek in graden
        angle = encoderValue * degrees_per_count
        print(encoderValue)
        #print(f"Angle: {angle:.2f}°")  # Toon de hoek met 2 decimalen
        time.sleep(0.1)  # Kortere vertraging voor vloeiendere updates

if __name__ == "__main__":
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        GPIO.cleanup()