import bluetooth

target_address = "C8:84:47:59:BE:65"

services = bluetooth.find_service(address=target_address)
for service in services:
    print("Service Name:", service["name"])
    print("Protocol:", service["protocol"])
    print("Port:", service["port"])
    print("--------------------")
