import pickle
import datetime

with open("test","rb") as infile:
    rooms = pickle.load(infile)
print(rooms)


def getCurentHourIndex(room):
    for i, hour in enumerate(room):
        if hour["end"] > datetime.datetime.now():
            return i


def getStartOfHour(room, i):
    j = i
    while room[i]["subjects"] == room[j]["subjects"] and room[i]["klassen"] == room[j]["klassen"]:
        if j > 0:
            j -= 1
        else:
            return room[j]["start"]
    return room[j+1]["start"]


def getEndOfHour(room, i):
    j = i
    while room[i]["subjects"] == room[j]["subjects"] and room[i]["klassen"] == room[j]["klassen"]:
        if len(room) > (j+1):
            j += 1
        else:
            return room[j]["end"]
    return room[j-1]["end"]


print(getStartOfHour(rooms["2.312"], getCurentHourIndex(rooms["2.312"])))
print(getEndOfHour(rooms["2.312"], getCurentHourIndex(rooms["2.312"])))
