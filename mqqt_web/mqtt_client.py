import paho.mqtt.publish as publish

MQTT_HOST = "206.189.51.153"
MQTT_PORT = 1883
MQTT_USER = "userA"
MQTT_PASSWORD = "12345678913"
TOPIC = "home/relay1/control"

def send_mqtt_command(message):
    publish.single(
        topic=TOPIC,
        payload=message,
        hostname=MQTT_HOST,
        port=MQTT_PORT,
        auth={'username': MQTT_USER, 'password': MQTT_PASSWORD}
    )
