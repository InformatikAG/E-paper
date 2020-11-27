import pickle
import datetime

'''the max lengths of strings that is allowed'''
lengthTeachers = 10
lengthOriginalTeachers = 10
lengthSubjects = 10
lengthKlassen = 10
lengthOriginalRoom = 10

offsetSleepStartHour = datetime.timedelta(minutes=5)
'''how long before the start of an hour does the ESP wake up'''

offsetPauseEnd = offsetSleepStartHour + datetime.timedelta(minutes=5)
'''how long before the end of the pause do we say it ended'''

offsetSleepEndHour = datetime.timedelta(minutes=0)
'''how long before the end of an hour does the ESP wake up'''

offsetPauseStart = datetime.timedelta(minutes=0)
'''how long before the start of an pause do we say it started'''

with open("test", "rb") as infile:
    rooms = pickle.load(infile)
# print(rooms)


def getCurentHourIndex(room):
    """goes through the hours and returns the index of the earliest which isn't over jet"""
    for i, hour in enumerate(room):
        if hour["end"] > datetime.datetime.now():
            return i


def getCurentHour(room):
    """goes through the hours and returns the earliest which isn't over jet"""
    for i, hour in enumerate(room):
        if hour["end"] > datetime.datetime.now():
            return hour


def getStartOfHour(room, i):
    """goes through the list of hours and returns the start time of last one that is not the same"""
    j = i
    while room[i]["subjects"] == room[j]["subjects"] and room[i]["klassen"] == room[j]["klassen"]:
        if j > 0:
            j -= 1
        else:
            return room[j]["start"]
    return room[j + 1]["start"]


def getEndOfHour(room, i):
    """goes through the list of hours and returns the end time of last one that is not the same"""
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
    short = short[:lengthTeachers]
    return short


def subjectsToString(hour):
    """:returns a string with a max length containing all subjects of the room"""
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
    short = short[:lengthSubjects]

    return short


def klassenToString(hour):
    """:returns a string with a max length containing all klasses of the room"""
    long = ""

    for klasse in hour["klassen"]:
        long += (klasse[0] + "; ")
    long = long[:-2]

    if len(long) < lengthKlassen:
        return long

    short = ""
    for klasse in hour["klassen"]:
        short += (klasse[1] + "; ")
    short = short[:-2]
    short = short[:lengthKlassen]

    return short


def getSleepTime(room):
    """
    :returns the number of seconds until the ESP has to wakeup
    """
    if getCurentHour(room)["start"] > (datetime.datetime.now() + offsetSleepStartHour):
        # is the start of the next or current hour more into the future than the offset?
        return (getCurentHour(room)["start"] - datetime.datetime.now() - offsetSleepStartHour).total_seconds()
        # returns the number of seconds until the start of the next hour minus the offset.
    else:
        return (getCurentHour(room)["end"] - datetime.datetime.now() - offsetSleepEndHour).total_seconds()
        # returns the number of seconds until the end of the current hour minus the offset.


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
    print("DeepSleepTime: " + str(getSleepTime(rooms[room])))
    print()
