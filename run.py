import bluetooth
import pyaudio
import wave

target_address = "00:23:01:00:00:45"
port = 1  # Default RFCOMM port

# Connect to the Bluetooth speaker
sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

try:
    # Try to close the socket
    sock.close()
    print("Socket closed successfully")
except bluetooth.btcommon.BluetoothError as e:
    print("Error while closing socket:", e)

sock.connect((target_address, port))

# Specify the audio file path
audio_file = "SoundsForStatic\metal-pipe-falling-sound-effect-By-tuna.voicemod.net.wav"

# Open the audio file
wf = wave.open(audio_file, 'rb')

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
    # Send audio data to the Bluetooth speaker
    sock.send(data)

    # Play audio data through the output stream
    stream.write(data)

    # Read the next chunk of audio data
    data = wf.readframes(chunk)

# Close the stream and terminate PyAudio
stream.stop_stream()
stream.close()
audio.terminate()

# Close the Bluetooth connection
sock.close()