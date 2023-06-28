import ctypes
import time

# Define the GUID of the Bluetooth audio service
BLUETOOTH_AUDIO_SERVICE_GUID = "{E0CBF06C-CD8B-4647-BB8A-263B43F0F974}"

# Define the address of the Bluetooth speaker
target_address = "00:23:01:00:00:45"  # Replace with the actual Bluetooth MAC address

# Load the Windows Bluetooth API DLL
bthapi = ctypes.windll.bthprops

# Define the necessary Bluetooth data structures
class BLUETOOTH_DEVICE_SEARCH_PARAMS(ctypes.Structure):
    _fields_ = [
        ("dwSize", ctypes.c_ulong),
        ("fReturnAuthenticated", ctypes.c_int),
        ("fReturnRemembered", ctypes.c_int),
        ("fReturnUnknown", ctypes.c_int),
        ("fReturnConnected", ctypes.c_int),
        ("fIssueInquiry", ctypes.c_int),
        ("cTimeoutMultiplier", ctypes.c_byte),
        ("hRadio", ctypes.c_ulonglong)
    ]

class BLUETOOTH_DEVICE_INFO(ctypes.Structure):
    _fields_ = [
        ("dwSize", ctypes.c_ulong),
        ("Address", ctypes.c_ulonglong),
        ("ulClassofDevice", ctypes.c_ulong),
        ("fConnected", ctypes.c_int),
        ("fRemembered", ctypes.c_int),
        ("fAuthenticated", ctypes.c_int),
        ("stLastSeen", ctypes.c_ulonglong),
        ("stLastUsed", ctypes.c_ulonglong),
        ("szName", ctypes.c_wchar * 248)
    ]

# Define the callback function for device enumeration
def device_callback(pDevice, pvParam):
    device_info = BLUETOOTH_DEVICE_INFO()
    device_info.dwSize = ctypes.sizeof(device_info)
    bthapi.BluetoothGetDeviceInfo(pDevice, ctypes.byref(device_info))
    if device_info.Address == int(target_address.replace(":", ""), 16):
        print("Found Bluetooth device:", device_info.szName)
        # Connect to the Bluetooth speaker using the audio service
        bthapi.BluetoothRegisterForAuthenticationEx(None, ctypes.byref(pDevice), None)
        bthapi.BluetoothAuthenticateDeviceEx(None, ctypes.byref(pDevice), None, None)
        bthapi.BluetoothSdpGetContainerElementData(None, device_info.Address, BLUETOOTH_AUDIO_SERVICE_GUID)
        bthapi.BluetoothConnectAudio()
        time.sleep(2)  # Wait for the connection to establish

        # Play audio through the Bluetooth speaker (replace with your audio playback code)
        print("Playing audio...")
        # Replace the code below with your audio playback logic using the connected audio device
        
        # Example: Using the winsound library to play a beep sound
        import winsound
        winsound.Beep(440, 1000)  # Play a beep sound for 1 second
        
        print("Audio playback completed.")
    return True

# Set up the device search parameters
search_params = BLUETOOTH_DEVICE_SEARCH_PARAMS()
search_params.dwSize = ctypes.sizeof(search_params)
search_params.fReturnConnected = True
search_params.fReturnRemembered = False
search_params.fIssueInquiry = False

# Enumerate the Bluetooth devices and find the target speaker
bthapi.BluetoothFindFirstDevice(ctypes.byref(search_params), ctypes.byref(device_info))
bthapi.BluetoothFindDeviceClose(None)

# Set up the device enumeration callback
ENUMFUNC = ctypes.CFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_ulonglong), ctypes.c_void_p)
enum_callback = ENUMFUNC(device_callback)

# Start the device enumeration
bthapi.BluetoothEnumerateInstalledServices(0, ctypes.byref(device_info), enum_callback, None)
