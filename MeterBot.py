#!/usr/bin/env python3

import requests
import paho.mqtt.client as mqtt

# SwitchBot API endpoint for getting temperature data
API_ENDPOINT = "https://api.switch-bot.com/v1.0/devices/{device_id}/status"

# Replace 'YOUR_DEVICE_ID' with your actual SwitchBot device ID
DEVICE_ID = "C7624839B0B5"

# SwitchBot API token
API_TOKEN = "f326f2aa513eeeeacb6d6a42ad5d515e5b8e83540c808d82d0732b6c449d749530bda39933570c614e730acdeb65f3cc"

# MQTT broker details
MQTT_BROKER_ADDRESS = "mqtt broker address"
MQTT_PORT = 1883
MQTT_TOPIC_TEMP = "wetter/act-temp"
MQTT_TOPIC_HUMIDITY = "wetter/act-hum"

def get_device_status():
    headers = {
        "Authorization": API_TOKEN
    }

    # Make a GET request to the SwitchBot API
    response = requests.get(API_ENDPOINT.format(device_id=DEVICE_ID), headers=headers)

    if response.status_code == 200:
        data = response.json()
        temperature_celsius = data['body']['temperature']
        humidity = round(data['body']['humidity'])  # Round the humidity to the nearest whole number
        temperature_fahrenheit = round((temperature_celsius * 9/5) + 32)  # Convert temperature to Fahrenheit
        return temperature_fahrenheit, humidity
    else:
        print("Failed to retrieve device status.")
        return None, None

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

def publish_mqtt_data(temperature, humidity):
    client = mqtt.Client()
    client.on_connect = on_connect

    client.connect(MQTT_BROKER_ADDRESS, MQTT_PORT, 60)
    client.publish(MQTT_TOPIC_TEMP, temperature)
    client.publish(MQTT_TOPIC_HUMIDITY, humidity)
    print(f"Temperature data published to MQTT topic '{MQTT_TOPIC_TEMP}'")
    print(f"Humidity data published to MQTT topic '{MQTT_TOPIC_HUMIDITY}'")
    print(f'{humidity}')
def main():
    temperature, humidity = get_device_status()

    if temperature is not None and humidity is not None:
        publish_mqtt_data(temperature, humidity)

if __name__ == "__main__":
    main()

