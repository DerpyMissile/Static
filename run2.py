import bluetooth

target_address = "00:23:01:00:00:45"

services = bluetooth.find_service(address=target_address)
for service in services:
    print("Service Name:", service["name"])
    print("Protocol:", service["protocol"])
    print("Port:", service["port"])
    print("--------------------")
