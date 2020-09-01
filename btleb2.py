import pygatt, binascii, struct
#from influxwriter import InfluxWriter
#from mqttwriter import MqttWriter

def data_handler_cb(handle, value):
    tempraw, humidityraw, uk1, uk2 = struct.unpack('<hbcc', value)
    temperature = tempraw/100
    humidity = humidityraw
    print(f"Temperature and humidity: {str(temperature)}, {str(humidity)}")

def main():
    adapter = pygatt.GATTToolBackend(search_window_size=2048)

    try:
        adapter.start()
        btmacs = ("A4:C1:38:7F:7B:F1", "A4:C1:38:A9:98:38")
        devices = []
        for btmac in btmacs:
            device = adapter.connect(btmac, timeout=30)
            device.subscribe("ebe0ccc1-7a0a-4b0c-8a1a-6ff2997da3a6", callback=data_handler_cb, wait_for_response=False)
            print(f"connected to {btmac}")
            devices.append(device)

        input('hit a key to stop\n')
    finally:
        adapter.stop()

    return 0

if __name__ == '__main__':
    exit(main())