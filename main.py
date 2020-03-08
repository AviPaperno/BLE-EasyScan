import atexit
import time

import Adafruit_BluefruitLE
from Adafruit_BluefruitLE.services import UART

import requests
import json


ble = Adafruit_BluefruitLE.get_provider()


def main():
    start_time = time.time()
    ble.clear_cached_data()
    adapter = ble.get_default_adapter()
    adapter.power_on()
    adapter.start_scan()
    atexit.register(adapter.stop_scan)
    known_uarts = {}
    while True:
        found = set(UART.find_devices())
        for device in found:
            if device.name not in known_uarts.keys():
                known_uarts[device.name] = device.id 
        time.sleep(1.0)
        if len(known_uarts) == 5:
            requests.put('localhost:8888/api/',json.dumps(known_uarts)) #Send JSON to SERVER
        if round(time.time() - start_time) % 10 == 0:
            break

ble.initialize()
ble.run_mainloop_with(main)
