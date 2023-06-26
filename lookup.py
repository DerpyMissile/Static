import bluetooth

nearby_devices = bluetooth.discover_devices()
for addr in nearby_devices:
    print("Device:", addr, bluetooth.lookup_name(addr))
