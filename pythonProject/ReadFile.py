import pickle
import datetime

with open("test","rb") as infile:
    rooms = pickle.load(infile)


def curentHour(room):
    for hour in room:
        if (hour["start"] < datetime.datetime.now()) & (hour["end"] > datetime.datetime.now()):
            return hour


def nextTime(room):
    time = datetime.datetime.now() + datetime.timedelta(days=1)
    for hour in room:
        if time > hour["start"] > datetime.datetime.now():
            time = hour["start"]
        if time > hour["end"] > datetime.datetime.now():
            time = hour["end"]
    return time

print(nextTime(rooms["2.312"]))