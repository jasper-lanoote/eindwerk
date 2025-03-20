from django.shortcuts import render
from django.http import JsonResponse
import serial
import crcmod.predefined
import re
import datetime

def home(request):
    return render(request, 'DigitaleMeter.html')

def DigitaleMeter(request):
    # Change your serial port here:
    serialport = '/dev/ttyUSB0'

    # Enable debug if needed:
    debug = False

    # Add/update OBIS codes here:
    obiscodes = {
        "0-0:1.0.0": "Timestamp",
        "0-0:96.3.10": "Switch electricity",
        "0-1:24.4.0": "Switch gas",
        "0-0:96.1.1": "Meter serial electricity",
        "0-1:96.1.1": "Meter serial gas",
        "0-0:96.14.0": "Current rate (1=day,2=night)",
        "1-0:1.8.1": "Rate 1 (day) - total consumption",
        "1-0:1.8.2": "Rate 2 (night) - total consumption",
        "1-0:2.8.1": "Rate 1 (day) - total production",
        "1-0:2.8.2": "Rate 2 (night) - total production",
        "1-0:21.7.0": "L1 consumption",
        "1-0:41.7.0": "L2 consumption",
        "1-0:61.7.0": "L3 consumption",
        "1-0:1.7.0": "All phases consumption",
        "1-0:22.7.0": "L1 production",
        "1-0:42.7.0": "L2 production",
        "1-0:62.7.0": "L3 production",
        "1-0:2.7.0": "All phases production",
        "1-0:32.7.0": "L1 voltage",
        "1-0:52.7.0": "L2 voltage",
        "1-0:72.7.0": "L3 voltage",
        "1-0:31.7.0": "L1 current",
        "1-0:51.7.0": "L2 current",
        "1-0:71.7.0": "L3 current",
        "0-1:24.2.3": "Gas consumption"
    }

    def checkcrc(p1telegram):
        # Check CRC16 checksum of telegram and return False if not matching
        for match in re.compile(b'\r\n(?=!)').finditer(p1telegram):
            p1contents = p1telegram[:match.end() + 1]
            givencrc = hex(int(p1telegram[match.end() + 1:].decode('ascii').strip(), 16))
        calccrc = hex(crcmod.predefined.mkPredefinedCrcFun('crc16')(p1contents))
        if debug:
            print(f"Given checksum: {givencrc}, Calculated checksum: {calccrc}")
        if givencrc != calccrc:
            if debug:
                print("Checksum incorrect, skipping...")
            return False
        return True

    def parsetelegramline(p1line):
        # Parse a single line of the telegram and extract relevant data
        unit = ""
        timestamp = ""
        if debug:
            print(f"Parsing:{p1line}")
        obis = p1line.split("(")[0]
        if obis in obiscodes:
            values = re.findall(r'\(.*?\)', p1line)
            value = values[0][1:-1]
            if obis == "0-0:1.0.0" or len(values) > 1:
                value = value[:-1]
            if len(values) > 1:
                timestamp = value
                value = values[1][1:-1]
            if "96.1.1" in obis:
                value = bytearray.fromhex(value).decode()
            else:
                lvalue = value.split("*")
                value = float(lvalue[0])
                if len(lvalue) > 1:
                    unit = lvalue[1]
            return (obiscodes[obis], value, unit, timestamp)
        else:
            return None

    def main():
        ser = serial.Serial(serialport, 115200, xonxoff=1)
        p1telegram = bytearray()
        data_output = {}
        try:
            while True:
                p1line = ser.readline()
                if "/" in p1line.decode('ascii'):
                    p1telegram = bytearray()
                p1telegram.extend(p1line)
                if "!" in p1line.decode('ascii'):
                    if checkcrc(p1telegram):
                        for line in p1telegram.split(b'\r\n'):
                            parsed = parsetelegramline(line.decode('ascii'))
                            if parsed:
                                desc, value, unit, timestamp = parsed
                                data_output[desc] = {
                                    "value": value,
                                    "unit": unit,
                                    "timestamp": timestamp if timestamp else None
                                }
                    break  # Exit after first complete telegram for demo purposes
        except Exception as e:
            if debug:
                print(f"Error: {e}")
        finally:
            ser.close()
        
        return JsonResponse(data_output, safe=False)

    return main()

def DigitaleMeter_dummy(request):
    # Mock data to simulate meter readings
    def mock_data():
        obiscodes = {
            "Timestamp": "0-0:1.0.0",
            "Switch electricity": "0-0:96.3.10",
            "Switch gas": "0-1:24.4.0",
            "Meter serial electricity": "0-0:96.1.1",
            "Meter serial gas": "0-1:96.1.1",
            "Current rate (1=day,2=night)": "0-0:96.14.0",
            "Rate 1 (day) - total consumption": "1-0:1.8.1",
            "Rate 2 (night) - total consumption": "1-0:1.8.2",
            "Rate 1 (day) - total production": "1-0:2.8.1",
            "Rate 2 (night) - total production": "1-0:2.8.2",
            "L1 consumption": "1-0:21.7.0",
            "L2 consumption": "1-0:41.7.0",
            "L3 consumption": "1-0:61.7.0",
            "All phases consumption": "1-0:1.7.0",
            "L1 production": "1-0:22.7.0",
            "L2 production": "1-0:42.7.0",
            "L3 production": "1-0:62.7.0",
            "All phases production": "1-0:2.7.0",
            "L1 voltage": "1-0:32.7.0",
            "L2 voltage": "1-0:52.7.0",
            "L3 voltage": "1-0:72.7.0",
            "L1 current": "1-0:31.7.0",
            "L2 current": "1-0:51.7.0",
            "L3 current": "1-0:71.7.0",
            "Gas consumption": "0-1:24.2.3"
        }

        # Dummy values for each OBIS code
        dummy_values = {
            "Timestamp": str(datetime.datetime.now()),
            "Switch electricity": 1,
            "Switch gas": 1,
            "Meter serial electricity": "123456789",
            "Meter serial gas": "987654321",
            "Current rate (1=day,2=night)": 1,
            "Rate 1 (day) - total consumption": 1500.75,
            "Rate 2 (night) - total consumption": 850.50,
            "Rate 1 (day) - total production": 500.25,
            "Rate 2 (night) - total production": 300.10,
            "L1 consumption": 500.0,
            "L2 consumption": 300.0,
            "L3 consumption": 200.0,
            "All phases consumption": 1000.0,
            "L1 production": 100.0,
            "L2 production": 50.0,
            "L3 production": 25.0,
            "All phases production": 175.0,
            "L1 voltage": 230.5,
            "L2 voltage": 231.0,
            "L3 voltage": 232.0,
            "L1 current": 5.0,
            "L2 current": 4.0,
            "L3 current": 3.5,
            "Gas consumption": 125.35
        }

        # Create mock output data
        data_output = {}
        for key, obis in obiscodes.items():
            data_output[key] = {
                "value": dummy_values[key],
                "unit": "kWh" if "consumption" in key or "production" in key else ""  # Dummy unit
            }

        return data_output

    # Return the mock data as a JSON response
    return JsonResponse(mock_data(), safe=False)
