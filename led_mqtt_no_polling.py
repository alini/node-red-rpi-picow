from machine import Pin
from time import sleep
from umqtt.simple import MQTTClient
import network
from random import *

led = Pin(15, Pin.OUT)

# Configure your Wi-Fi credentials
SSID     = '<--WIFI-NETWORK-NAME-->'
PASSWORD = '<--WIFI-PASSWORD-->'

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID,PASSWORD)

while not wlan.isconnected():
    pass

print('Connected to Wi-Fi')
print(wlan.ifconfig())

# Setup MQTT
SERVER      = '<--SERVER-IP-ADDRESS-->'  # Replace with your MQTT broker IP
CLIENT_ID   = b'PICO'
TOPIC       = b'led_state'
USER        = b'<--MQTT_USER-->'    # Replace with your MQTT username
PASSWORD    = b'<--MQTT_PASSWORD-->'# Replace with your MQTT password

def mqtt_connect():
   client = MQTTClient(CLIENT_ID, SERVER, user=USER, password=PASSWORD, keepalive=3600)
   client.connect()
   print('Connected to %s MQTT Broker'%(SERVER))
   return client

def reconnect():
   print('Failed to connect to the MQTT Broker. Reconnecting...')
   sleep(5)
   machine.reset()

def on_message(topic, msg):
    print("Received message:", msg.decode())
    if msg == b'on':
        led.value(1)
    elif msg == b'off':
        led.value(0)


def main(server, topic, username, passw):
    client = MQTTClient(CLIENT_ID, server, user=username, password=passw, keepalive=3600)
    client.set_callback(on_message)
    client.connect()
    client.subscribe(topic)
    print("Connected to %s, subscribed to %s topic" % (server, topic))

    try:
        while True:
            client.wait_msg()
#            client.check_msg()
#            sleep(1)

    finally:
        client.disconnect()

main(SERVER, TOPIC, USER, PASSWORD)
