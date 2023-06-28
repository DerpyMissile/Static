import bluetooth
import pyaudio
from pydub import AudioSegment

target_address = "00:23:01:00:00:45"
port = 1  # Default RFCOMM port

# Connect to the Bluetooth speaker
sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.connect((target_address, port))

# Specify the audio file path
audio_file = "SoundsForStatic/metal-pipe-falling-sound-effect-By-tuna.voicemod.net.wav"

# Load the MP3 file using pydub
audio = AudioSegment.from_mp3(audio_file)

# Convert the audio to WAV format
audio = audio.set_frame_rate(44100).set_channels(2)
wav_data = audio.raw_data

# Initialize PyAudio
pyaudio_instance = pyaudio.PyAudio()

# Open a stream to play the audio
stream = pyaudio_instance.open(
    format=pyaudio_instance.get_format_from_width(audio.sample_width),
    channels=audio.channels,
    rate=audio.frame_rate,
    output=True
)

# Split the audio into chunks and play them
chunk_size = 1024
offset = 0

while offset < len(wav_data):
    # Get the chunk to play
    chunk = wav_data[offset:offset+chunk_size]

    # Send audio data to the Bluetooth speaker
    sock.send(chunk)

    # Play audio data through the output stream
    stream.write(chunk)

    offset += chunk_size

# Close the stream and terminate PyAudio
stream.stop_stream()
stream.close()
pyaudio_instance.terminate()

# Close the Bluetooth connection
sock.close()
