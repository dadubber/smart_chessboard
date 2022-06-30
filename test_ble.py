import asyncio
from bleak import BleakClient

address = "D0:3A:1C:27:B8:7D"
measurment_UUID = "6e400003-b5a3-f393-e0a9-e50e24dcca9e"


async def main():
    async with BleakClient(address) as client:
        model_number = await client.read_gatt_char(measurment_UUID)
        board_positions = [int(pos) for pos in model_number.decode('utf-8')]

def tyout():
    while True:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())

tyout()