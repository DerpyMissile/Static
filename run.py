import bluetooth

target_address = "00:23:01:00:00:45"
port = 1  # Default RFCOMM port

# Connect to the device
sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.connect((target_address, port))

# Send commands to the device
# Example: Send 'play' command to start playing music
command = b'play'
sock.send(command)

# Receive data from the device
data = sock.recv(1024)
print("Received data:", data)

# Close the connection
sock.close()
