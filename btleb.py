import gatt, binascii, struct

manager = gatt.DeviceManager(adapter_name='hci0')

class AnyDevice(gatt.Device):
    def services_resolved(self):
        super().services_resolved()

        device_information_service = next(
            s for s in self.services
            if s.uuid == 'ebe0ccb0-7a0a-4b0c-8a1a-6ff2997da3a6')
        temperature_humidity_characteristic = next(
            c for c in device_information_service.characteristics
            if c.uuid == 'ebe0ccc1-7a0a-4b0c-8a1a-6ff2997da3a6')
        temperature_humidity_characteristic.enable_notifications()

        #temperature_humidity_characteristic.read_value()

    def characteristic_value_updated(self, characteristic, value):
        #print("Temperature and humidity:", binascii.hexlify(value))
        tempraw, humidityraw, uk1, uk2 = struct.unpack('<hbcc', value)
        print(f"Temperature and humidity: {str(tempraw/100)}, {str(humidityraw)}")

    def characteristic_enable_notification_succeeded(self, characteristic):
        print(f"Enabled notification succeeded on {characteristic}")

    def characteristic_enable_notification_failed(self, characteristic):
        print(f"Enabled notification failed on {characteristic}")


device = AnyDevice(mac_address='A4:C1:38:7F:7B:F1', manager=manager)
device.connect()

manager.run()