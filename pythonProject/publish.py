import paho.mqtt.client as mqtt

client = mqtt.Client()
client.connect("192.168.178.117", 1883, 60)

client.publish("test/temperatur", "25 C")
client.disconnect()
