import pickle
import datetime
import paho.mqtt.client as mqtt
import time
import subprocess

# creating the client object and connecting to the mqtt server
client = mqtt.Client()
client.username_pw_set("username", "password")
client.connect("192.168.178.117", 1883, 60)

# the max lengths of strings that is allowed
lengthTeachers = 10
lengthOriginalTeachers = 10
lengthSubjects = 10
lengthKlassen = 10
lengthOriginalRoom = 10

offsetSleepStartHour = datetime.timedelta(minutes=5)
"""how long before the start of an hour does the ESP wake up"""

offsetBreakEnd = offsetSleepStartHour + datetime.timedelta(minutes=5)
"""how long before the end of the break do we say it ended"""

offsetSleepEndHour = datetime.timedelta(minutes=0)
"""how long before the end of an hour does the ESP wake up"""

offsetBreakStart = offsetSleepEndHour + datetime.timedelta(minutes=0)
"""how long before the start of an break do we say it started"""

with open("test", "rb") as infile:
    rooms = pickle.load(infile)  # using pickle to read the file containing all the untis data
# print(rooms)


def getCurrentHourIndex(room):
    """goes through the hours and returns the index of the earliest which isn't over jet using the offset"""
    for i, hour in enumerate(room):
        if hour["end"] > (datetime.datetime.now() + offsetBreakStart):
            return i


def getCurrentHour(room):
    """goes through the hours and returns the earliest which isn't over jet using the offset"""
    for i, hour in enumerate(room):
        if hour["end"] > (datetime.datetime.now() + offsetBreakStart):
            return hour


def getStartOfHour(room, i):
    """goes through the list of hours and returns the start time of the last one that is the same"""
    j = i
    while room[i]["subjects"] == room[j]["subjects"] and room[i]["klassen"] == room[j]["klassen"]:
        if j > 0:
            j -= 1
        else:
            return room[j]["start"]
    return room[j + 1]["start"]


def getEndOfHour(room, i):
    """goes through the list of hours and returns the end time of the last one that is the same"""
    j = i
    while room[i]["subjects"] == room[j]["subjects"] and room[i]["klassen"] == room[j]["klassen"]:
        if len(room) > (j + 1):
            j += 1
        else:
            return room[j]["end"]
    return room[j - 1]["end"]


def timeToString(time):
    """:returns the time in the format hh:mm"""
    return str(time.hour) + ":" + str(time.minute)


def teachersToString(hour):
    """:returns a string with a max length containing all teachers of the room"""
    long = ""

    for teacher in hour["teachers"]:
        long += (teacher[0] + "; ")
    long = long[:-2]  # deletes the last to characters which are "; "

    if len(hour["original_teachers"]) != 0:
        long += "("
        for teacher in hour["original_teachers"]:
            long += (teacher[0] + "; ")
        long = long[:-2]  # deletes the last to characters which are "; "
        long += ")"

    if len(long) < lengthTeachers:
        return long

    short = ""
    for teacher in hour["teachers"]:
        short += (teacher[1] + "; ")
    short = short[:-2]  # deletes the last to characters which are "; "

    if len(hour["original_teachers"]) != 0:
        short += " ("
        for teacher in hour["original_teachers"]:
            short += (teacher[1] + "; ")
        short = short[:-2]  # deletes the last to characters which are "; "
        short += ")"
    short = short[:lengthTeachers]  # cuts of every character after tha set limit TODO: find better solution
    return short


def subjectsToString(hour):
    """:returns a string with a max length containing all subjects of the room"""
    long = ""

    for subject in hour["subjects"]:
        long += (subject[0] + "; ")
    long = long[:-2]  # deletes the last to characters which are "; "

    if len(long) < lengthSubjects:
        return long

    short = ""
    for subject in hour["subjects"]:
        short += (subject[1] + "; ")
    short = short[:-2]  # deletes the last to characters which are "; "
    short = short[:lengthSubjects]  # cuts of every character after tha set limit TODO: find better solution

    return short


def klassenToString(hour):
    """:returns a string with a max length containing all Klassen of the room"""
    long = ""

    for klasse in hour["klassen"]:
        long += (klasse[0] + "; ")
    long = long[:-2]  # deletes the last to characters which are "; "

    if len(long) < lengthKlassen:
        return long

    short = ""
    for klasse in hour["klassen"]:
        short += (klasse[1] + "; ")
    short = short[:-2]  # deletes the last to characters which are "; "
    short = short[:lengthKlassen]  # cuts of every character after tha set limit TODO: find better solution

    return short


def getSleepTime(room):
    """
    :returns the number of seconds until the ESP has to wakeup
    """
    if getCurrentHour(room)["start"] > (datetime.datetime.now() + offsetSleepStartHour):
        # is the start of the next or current hour more into the future than the offset?
        return (getCurrentHour(room)["start"] - datetime.datetime.now() - offsetSleepStartHour).total_seconds()
        # returns the number of seconds until the start of the next hour minus the offset.
    else:
        return (getCurrentHour(room)["end"] - datetime.datetime.now() - offsetSleepEndHour).total_seconds()
        # returns the number of seconds until the end of the current hour minus the offset.


def isBreak(room):
    """:returns false during class including the offsets"""
    for hour in room:
        if (hour["start"] - offsetBreakEnd) < datetime.datetime.now() < (hour["end"] - offsetBreakStart):
            return False
    return True


def updateMqtt():
    for room in rooms:
        hour = getCurrentHour(rooms[room])
        print(room + ":")
        if hour is None:
            print("sleep until tomorrow")
            client.publish(room + "/DeepSleepTime", (datetime.datetime.now().replace(hour=7, minute=0, second=0)
                                                     - datetime.datetime.now()
                                                     + datetime.timedelta(days=1)).total_seconds())
            print()
            continue

        fach = subjectsToString(hour)
        print(" Fach: " + fach)
        client.publish(room + "/Fach", fach)

        lehrer = teachersToString(hour)
        print(" Lehrer: " + lehrer)
        client.publish(room + "/Lehrer", lehrer)

        zeit = (timeToString(getStartOfHour(rooms[room], getCurrentHourIndex(rooms[room]))) + " - "
                + timeToString(getEndOfHour(rooms[room], getCurrentHourIndex(rooms[room]))))
        print(" Zeit: " + zeit)
        client.publish(room + "/Zeit")

        klasse = klassenToString(rooms[room][0])
        print(" Klasse: " + klasse)
        client.publish(room + "/Klasse", klasse)

        pause = isBreak(rooms[room])
        print(" Pause: " + repr(pause))
        client.publish(room + "/Pause", pause)

        deepSleepTime = getSleepTime(rooms[room])
        print(" DeepSleepTime: " + repr(deepSleepTime))
        client.publish(room + "/DeepSleepTime", deepSleepTime)

        print()

nextApiUpdate = datetime.datetime.now()
while True:  # run forever
    if nextApiUpdate < datetime.datetime.now():
        print("updating API")
        print(subprocess.run("API.py", shell=True))  # runAPI.py
        nextApiUpdate = nextApiUpdate + datetime.timedelta(hours=1)  # increase next update time by one hour
    updateMqtt()
    time.sleep(60)
