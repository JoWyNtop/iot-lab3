from machine import Pin
import machine
import dht
import time
import lcd128_32_fonts
from lcd128_32 import lcd128_32
import urequests as requests
import network

DHT = dht.DHT11(Pin(13))

clock_pin = 22
data_pin = 21
bus = 0
i2c_addr = 0x3f
use_i2c = True
WIFI_SSID = ''  # TODO: add your SSID, password and thing name with default message body
WIFI_PASS = ''
THING = 'KNUS-12-15'
DEFAULT_MESSAGE = {
    "name": "VolodymyrL"
}
HEADERS = {"Content-Type": "application/json"}


def scan_for_devices():
    i2c = machine.I2C(bus, sda=machine.Pin(data_pin), scl=machine.Pin(clock_pin))
    devices = i2c.scan()
    if devices:
        for d in devices:
            print(hex(d))
    else:
        print('no i2c devices')


try:
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if wlan.isconnected():
        wlan.disconnect()
    wlan.connect(WIFI_SSID, WIFI_PASS)
    while not wlan.isconnected():
        print("Connecting to Wifi")
    print("Connected to Wifi")
    while True:
        DHT.measure()
        temperature = int(DHT.temperature())
        humidity = int(DHT.humidity())
        if use_i2c:
            scan_for_devices()
            lcd = lcd128_32(data_pin, clock_pin, bus, i2c_addr)
        lcd.Clear()
        lcd.Cursor(0, 0)
        lcd.Display(f"Temperature: {temperature} C")
        lcd.Cursor(2, 0)
        lcd.Display(f"Humidity: {humidity} %")
        message = DEFAULT_MESSAGE.copy()
        message.update({"humidity": humidity, "temperature": temperature})
        resp = requests.post(f"https://dweet.io/dweet/for/{THING}", json=message, headers=HEADERS)
        resp.close()
        time.sleep(0.1)
except Exception as error:
    print(error)
