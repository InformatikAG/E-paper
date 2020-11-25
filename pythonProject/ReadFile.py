import pickle
import datetime

with open("test","rb") as infile:
    rooms = pickle.load(infile)


def findCurentHour(room):
    for hour in room:
        if (hour["start"] < datetime.datetime.now()) & (hour["end"] > datetime.datetime.now()):
            return hour


print(findCurentHour(rooms["2.311"]))