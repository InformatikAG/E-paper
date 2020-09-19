import paho.mqtt.client as mqtt

client = mqtt.Client()
client.connect("192.168.178.117", 1883, 60)

client.publish("inTopic", "1")

for i in range(10):
    test = input()
    client.publish("inTopic", test)

client.disconnect()
