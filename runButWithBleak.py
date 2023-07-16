import asyncio
import bleak
import pyaudio
import wave

# Specify the Bluetooth device name or address
device_name = "D9:2E:73:17:5A:11"

# Specify the audio file path
audio_file = "SoundsForStatic//metalPipe.mp3"

async def connect_and_play(device):
    # Connect to the Bluetooth device
    async with bleak.BleakClient(device) as client:
        # Enable the audio service on the device
        audio_service_uuid = "0000110d-0000-1000-8000-00805f9b34fb"
        audio_service = await client.get_service(audio_service_uuid)

        # Find the characteristic for audio streaming
        audio_stream_characteristic = None
        for char in audio_service.characteristics:
            if "write" in char.properties:
                audio_stream_characteristic = char
                break

        if audio_stream_characteristic:
            print("Audio streaming characteristic found.")

            # Open the audio file
            with wave.open(audio_file, 'rb') as wf:
                # Initialize PyAudio
                audio = pyaudio.PyAudio()

                # Open a stream to play the audio
                stream = audio.open(format=audio.get_format_from_width(wf.getsampwidth()),
                                    channels=wf.getnchannels(),
                                    rate=wf.getframerate(),
                                    output=True)

                # Read audio data and play it in chunks
                chunk = 1024
                data = wf.readframes(chunk)

                while data:
                    # Send audio data to the Bluetooth device
                    await audio_stream_characteristic.write_value(data, response=False)

                    # Play audio data through the output stream
                    stream.write(data)

                    # Read the next chunk of audio data
                    data = wf.readframes(chunk)

                # Close the stream and terminate PyAudio
                stream.stop_stream()
                stream.close()
                audio.terminate()

        else:
            print("Audio streaming characteristic not found.")

async def discover_and_connect():
    scanner = bleak.BleakScanner()
    devices = await scanner.discover()

    print("Gets to here")
    for device in devices:
        print(device.name)
        print(device.address)
        if device.name == device_name or device.address == device_name:
            print("Bluetooth device found:", device)
            await connect_and_play(device)
            break

async def main():
    print("Starting...")
    await discover_and_connect()
    print("Ending...")

# Run the event loop
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
