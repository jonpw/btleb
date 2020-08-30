import gatt, binascii, struct
#from influxwriter import InfluxWriter
#from mqttwriter import MqttWriter

manager = gatt.DeviceManager(adapter_name='hci0')

#influxwriter = InfluxWriter(hostname, database=ASSET_DB_NAME, user=INFLUX_USER, password=INFLUX_PASS)
#mqttwriter = MqttWriter(hostname, topic_prefix=MQTT_BASE_TOPIC, user=MQTT_USER, password=MQTT_PASS)

class XiaoMiTHDevice(gatt.Device):
    def services_resolved(self):
        super().services_resolved()

        device_information_service = next(
            s for s in self.services
            if s.uuid == 'ebe0ccb0-7a0a-4b0c-8a1a-6ff2997da3a6')
        temperature_humidity_characteristic = next(
            c for c in device_information_service.characteristics
            if c.uuid == 'ebe0ccc1-7a0a-4b0c-8a1a-6ff2997da3a6')
        temperature_humidity_characteristic.enable_notifications()

    def characteristic_value_updated(self, characteristic, value):
        tempraw, humidityraw, uk1, uk2 = struct.unpack('<hbcc', value)
        temperature = tempraw/100
        humidity = humidityraw
        print(f"Temperature and humidity: {str(temperature)}, {str(humidity)}")
        #influxwriter({"device": self.mac_address, "data": {"temperature": temperature, "humidity": humidity}})

    def characteristic_enable_notification_succeeded(self, characteristic):
        print(f"Enabled notification succeeded on {characteristic}")

    def characteristic_enable_notification_failed(self, characteristic):
        print(f"Enabled notification failed on {characteristic}")

btmacs = ('A4:C1:38:7F:7B:F1', 'A4:C1:38:A9:98:38')
devices = []
for btmac in btmacs:
    device = XiaoMiTHDevice(mac_address=btmac, manager=manager)
    device.connect()
    devices.append(device)

manager.run()