import pickle
import datetime

lengthTeachers = 10
lengthOriginalTeachers = 10
lengthSubjects = 10
lengthKlassen = 10
lengthOriginalRoom = 10

with open("test", "rb") as infile:
    rooms = pickle.load(infile)
# print(rooms)


def getCurentHourIndex(room):
    for i, hour in enumerate(room):
        if hour["end"] > datetime.datetime.now():
            return i


def getCurentHour(room):
    for i, hour in enumerate(room):
        if hour["end"] > datetime.datetime.now():
            return hour


def getStartOfHour(room, i):
    j = i
    while room[i]["subjects"] == room[j]["subjects"] and room[i]["klassen"] == room[j]["klassen"]:
        if j > 0:
            j -= 1
        else:
            return room[j]["start"]
    return room[j + 1]["start"]


def getEndOfHour(room, i):
    j = i
    while room[i]["subjects"] == room[j]["subjects"] and room[i]["klassen"] == room[j]["klassen"]:
        if len(room) > (j + 1):
            j += 1
        else:
            return room[j]["end"]
    return room[j - 1]["end"]


def timeToString(time):
    return str(time.hour) + ":" + str(time.minute)


def teachersToString(hour):
    long = ""

    for teacher in hour["teachers"]:
        long += (teacher[0] + "; ")
    long = long[:-2]

    if len(hour["original_teachers"]) != 0:
        long += "("
        for teacher in hour["original_teachers"]:
            long += (teacher[0] + "; ")
        long = long[:-2]
        long += ")"

    if len(long) < lengthTeachers:
        return long

    short = ""
    for teacher in hour["teachers"]:
        short += (teacher[1] + "; ")
    short = short[:-2]

    if len(hour["original_teachers"]) != 0:
        short += " ("
        for teacher in hour["original_teachers"]:
            short += (teacher[1] + "; ")
        short = short[:-2]
        short += ")"

    return short


def subjectsToString(hour):
    long = ""

    for subject in hour["subjects"]:
        long += (subject[0] + "; ")
    long = long[:-2]

    if len(long) < lengthSubjects:
        return long

    short = ""
    for subject in hour["subjects"]:
        short += (subject[1] + "; ")
    short = short[:-2]

    return short


def klassenToString(hour):
    long = ""

    for klasse in hour["klassen"]:
        long += (klasse[0] + "; ")
    long = long[:-2]

    if len(long) < lengthSubjects:
        return long

    short = ""
    for klasse in hour["klassen"]:
        short += (klasse[1] + "; ")
    short = short[:-2]

    return short


# print(timeToString(getStartOfHour(rooms["2.311"], getCurentHourIndex(rooms["2.311"]))))
# print(timeToString(getEndOfHour(rooms["2.311"], getCurentHourIndex(rooms["2.311"]))))
# print(rooms["2.311"][getCurentHourIndex(rooms["2.311"])]["subjects"])


for room in rooms:
    hour = getCurentHour(rooms[room])
    if hour is None:
        print("sleep until tomorow")
        print()
        continue
    print("Fach: " + subjectsToString(hour))
    print("Lehrer: " + teachersToString(hour))
    print("Zeit: " + timeToString(getStartOfHour(rooms[room], getCurentHourIndex(rooms[room]))) + " - "
          + timeToString(getEndOfHour(rooms[room], getCurentHourIndex(rooms[room]))))
    print("Klasse: " + klassenToString(rooms[room][0]))
    print()
