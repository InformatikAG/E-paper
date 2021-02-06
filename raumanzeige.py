#!/usr/bin/env python
import configparser
import paho.mqtt.client as mqtt
import time
import schedule
import datetime

display_raum = {}
mqtt_client = None
 
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))
 
#client = mqtt.Client()
#client.on_message = on_message
#client.connect("127.0.0.1", 1883, 60)
#client.subscribe("test/temperatur")
#client.loop_forever()

def getDisplayRaeume(c): #reads displays and rooms and returns them as dict
    for key in c['Displays_Raum']:
        display_raum[key] = c.get('Displays_Raum', key)
    return display_raum

def sendMQTTRoomUpdate(client,display,zeit,lehrer,klasse,deepsleeptime):
    ## Topic-Keywords
    zeit = config.get('MQTT_Topics', 'Zeit')
    lehrer = config.get('MQTT_Topics', 'Lehrer')
    klasse = config.get('MQTT_Topics', 'Klasse')
    deepsleeptime = config.get('MQTT_Topics', 'DeepSleepTime')
    ##

def setupMQTTConnection(brokerIP,BrokerPort,display_raum,config):
    ## Topic-Keywords
    status = config.get('MQTT_Topics', 'Status')
    ##
    client = mqtt.Client()
    client.on_message = on_message
    client.connect(brokerIP, int(BrokerPort), 60)
    for key in display_raum: #subscribe to all "Status-Topics" of all Displays
        topic = key+"/"+status
        client.subscribe(topic)
        print(topic)

    return client

def initConfig(): #Sets up config-file
    config = configparser.ConfigParser()
    config.read("./config.ini")
    config.sections()
    return config

def wakeUp():
    print("WAKY WAKY")

def work(last_work_call = False):
    print("WORK: last_work_call="+str(last_work_call))
    run = True
    starttime = datetime.datetime.now().strftime("%M") # Minutes of current time
    config = initConfig()
    runtime = config.get('Work_Duration_In_Minutes', 'runtime')
    ## GET ALL UNTIS INFORMATION 
    while run: # Run for x Minutes
        currenttime = datetime.datetime.now().strftime("%M")
        if currenttime > starttime+runtime:         # check, if the time is up
            run = False  # No more work
        
        mqtt_client.loop() # get one MQTT-Message
        #### DO THE WORK HERE ####
        # IF DISPLAY IS THERE -> SEND INFORMATION
        # 
        time.sleep(0.25)

    print("WORK: Work is done! Schedule new workday for tommorrow")
    scheduleWorkDay()



def scheduleWorkDay(day = "TOMORROW"): # Parameter: TODAY or TOMORROW. Default: TOMORROW
    config = initConfig()
    weekdayIndex = datetime.datetime.today().weekday() #0:Monday 6: Sunday
    if day == "TOMORROW":
        weekdayIndex = weekdayIndex + 1 # Tomorrow
        if weekdayIndex > 6:
            weekdayIndex = 0

    print("SCHED: Schedule for "+day)
    print("SCHED: Schedule for Weekday Index: "+str(weekdayIndex))

    mode = ""
    if weekdayIndex > 4: # 4: Friday (Select Saturdays and Sundays)
        mode = "Weekend_Hours"
    else:
        mode = "Workday_Hours"
    
    print("#Len: "+str(len(config[mode])))
    count = 0
    for key in config[mode]:
        count = count + 1
        time = config.get(mode, key)
        schedule.every().day.at(time).do(work)
        if count == len(config[mode]): # last key is reached, schedule last_work_call
            schedule.every().day.at(time).do(work, True)
            print("SCHED: Schedule last_work_call at: "+time)
        else:
            schedule.every().day.at(time).do(work)
            print("SCHED: Schedule time: "+time)


        

def run():
    global display_raum, mqtt_client
    print("MAIN: Start!")
    print("MAIN: Reading config")
    config = initConfig() # Config-Access
    #####
    MQTT_Broker_IP = config.get('MQTT', 'BrokerIP')
    MQTT_Broker_Port = config.get('MQTT', 'BrokerPort')
    #####
    print("MAIN: Read Room - Display - Mappings")
    display_raum = getDisplayRaeume(config)
    print(display_raum)
    print("MAIN: Connecting to MQTT-Broker")
    mqtt_client = setupMQTTConnection(MQTT_Broker_IP,MQTT_Broker_Port,display_raum,config)
    run = True
    #schedule.every(10).seconds.do(wakeUp)
    schedule.every().day.at('19:40').do(wakeUp)
    scheduleWorkDay("TODAY") # Only on the first run
    while run:
        #mqtt_client.loop()
        schedule.every().day.at("16:45").do(work, True)
        schedule.run_pending()
        time.sleep(10)



if __name__ == "__main__":
	run()