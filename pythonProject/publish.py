import paho.mqtt.client as mqtt

client = mqtt.Client()
client.username_pw_set("username","password")
client.connect("192.168.178.45", 1883, 60)

while (True):
    print("Input a topic or q to quit")
    topic = input()
    if (topic == "q"):
        break
    print("Input a value for " + topic)
    value = input()
    client.publish(topic, value)

client.disconnect()
