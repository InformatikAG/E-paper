import paho.mqtt.client as mqtt


def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))


client = mqtt.Client()
client.on_message = on_message
client.username_pw_set("username","password")
client.connect("192.168.178.45", 1883, 60)
client.subscribe("test/temperatur")
client.loop_forever()
