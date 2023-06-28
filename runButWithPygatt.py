import bluetooth
import pygatt
import subprocess

target_address = "00:23:01:00:00:45"
port = 1  # Default RFCOMM port

# Connect to the Bluetooth speaker
sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.connect((target_address, port))

# Specify the audio file path
audio_file = "SoundsForStatic//metalPipe.mp3"

# Use FFmpeg to decode the MP3 file to raw PCM data
ffmpeg_command = ["ffmpeg", "-i", audio_file, "-f", "s16le", "-ar", "44100", "-ac", "2", "-"]
ffmpeg_process = subprocess.Popen(ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

# Initialize Pygatt
adapter = pygatt.GATTToolBackend()

try:
    # Start the Pygatt adapter
    adapter.start()

    # Connect to the Bluetooth speaker
    device = adapter.connect(target_address)

    # Enable the audio streaming service on the device
    audio_stream_service_uuid = "0000110d-0000-1000-8000-00805f9b34fb"
    audio_stream_service = device.discover_characteristics(audio_stream_service_uuid)[0]

    # Read and send the raw PCM data in chunks
    chunk_size = 1024
    while True:
        pcm_data = ffmpeg_process.stdout.read(chunk_size)
        if not pcm_data:
            break

        # Send the PCM data to the Bluetooth speaker
        audio_stream_service.write_value(pcm_data, wait_for_response=False)

finally:
    # Stop the Pygatt adapter and close the Bluetooth connection
    adapter.stop()
    sock.close()
