from channels.consumer import AsyncConsumer, SyncConsumer
from channels.exceptions import StopConsumer
import json


import asyncio
from channels.generic.websocket import WebsocketConsumer
import serial
import crcmod.predefined
import re
import datetime





# synchrone connectie
class MySyncConsumer(SyncConsumer):
    def websocket_connect(self, event):
        print("Websocket connected...", event)
        self.send({
        'type': 'websocket.accept'
        })
    def websocket_receive(self, event):
        print('Message received form client', event)
        self.send(
        {
        'type': 'websocket.send',
        'text': f"Hello"
        }
    )
    def websocket_disconnect(self, event):
        print("Websocket disconnected", event)
        StopConsumer()
# Asynchrone connectie
class MyAsyncConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print("Websocket connected...", event)
        self.send({
        'type': 'websocket.accept'
        })
    async def websocket_receive(self, event):
        print('Message received form client', event)
    async def websocket_disconnect(self, event):
        print("Websocket disconnected", event)



from channels.generic.websocket import WebsocketConsumer
import json
import re
import serial
import crcmod.predefined

class DigitaleMeterConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        self.serialport = '/dev/ttyUSB0'  # Update as necessary
        self.debug = False
        self.running = True
        self.start_reading_meter_data()

    def disconnect(self, close_code):
        self.running = False

    def receive(self, text_data):
        # Optional: Handle incoming messages from the client
        data = json.loads(text_data)
        if data.get("command") == "stop":
            self.running = False
        elif data.get("command") == "start":
            self.running = True
            self.start_reading_meter_data()

    def send_meter_data(self, data):
        self.send(text_data=json.dumps(data))

    def start_reading_meter_data(self):
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
            for match in re.compile(b'\r\n(?=!)').finditer(p1telegram):
                p1contents = p1telegram[:match.end() + 1]
                givencrc = hex(int(p1telegram[match.end() + 1:].decode('ascii').strip(), 16))
                calccrc = hex(crcmod.predefined.mkPredefinedCrcFun('crc16')(p1contents))
                return givencrc == calccrc

        def parsetelegramline(p1line):
            unit, timestamp = "", ""
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
                return obiscodes[obis], value, unit, timestamp
            return None

        # Start reading data
        try:
            ser = serial.Serial(self.serialport, 115200, xonxoff=1)
            p1telegram = bytearray()
            while self.running:
                p1line = ser.readline()
                if "/" in p1line.decode('ascii'):
                    p1telegram = bytearray()
                p1telegram.extend(p1line)
                if "!" in p1line.decode('ascii'):
                    if checkcrc(p1telegram):
                        data_output = {}
                        for line in p1telegram.split(b'\r\n'):
                            parsed = parsetelegramline(line.decode('ascii'))
                            if parsed:
                                desc, value, unit, timestamp = parsed
                                data_output[desc] = {
                                    "value": value,
                                    "unit": unit,
                                    "timestamp": timestamp if timestamp else None,
                                }
                        self.send_meter_data(data_output)
                    p1telegram = bytearray()  # Clear telegram after sending
        except Exception as e:
            self.send_meter_data({"error": str(e)})
        finally:
            ser.close()
