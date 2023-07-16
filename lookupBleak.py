import asyncio
import bleak

async def discover_devices():
    scanner = bleak.BleakScanner()
    devices = await scanner.discover()

    for device in devices:
        print("Device Name:", device.name)
        print("Device Address:", device.address)
        print()

async def main():
    await discover_devices()

# Run the event loop
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
