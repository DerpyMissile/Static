import bluetooth

print("hello?")
target_address = "00:23:01:00:00:45"

nearby_devices = bluetooth.discover_devices()
for addr in nearby_devices:
    print("Device:", addr, bluetooth.lookup_name(addr))
    print("Service Name:", addr["name"])
    print("Protocol:", addr["protocol"])
    print("Port:", addr["port"])
    print("--------------------")
