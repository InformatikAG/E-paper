import webuntis
import datetime
import pickle

requestedRooms = {"2.312", "2.311", "2.310"}

today = datetime.date.today()
monday = today - datetime.timedelta(days=today.weekday())
friday = monday + datetime.timedelta(days=4)


def sort(e):
    """:returns the start value of the input"""
    return e["start"]


def convertTeachers(hour):
    """:returns a list of lists with the long and short name"""
    try:
        new = []
        for i in hour.teachers:  # goes through all teachers and appends them to the list
            new.append([i.long_name, i.name])  # appends a list with the long and short name
        return new
    except:
        return []


def convertRooms(hour):
    """:returns a list of all rooms"""
    try:
        new = []
        for i in hour.rooms:  # goes through all rooms and appends them to the list
            new.append(i.name)  # appends the name
        return new
    except:
        return []


def convertOriginalTeachers(hour):
    """:returns a list of lists with the long and short name"""
    try:
        new = []
        for i in hour.original_teachers:  # goes through all teachers and appends them to the list
            new.append([i.long_name, i.name])  # appends a list with the long and short name
        return new
    except:
        return []


def convertOriginalRooms(hour):
    """:returns a list of all the names"""
    try:
        new = []
        for i in hour.original_rooms:  # goes through all rooms and appends them to the list
            new.append(i.name)  # appends the name
        return new
    except:
        return []


def convertSubjects(hour):
    """:returns a list of lists with the long and short name"""
    try:
        new = []
        for i in hour.subjects:  # goes through all subjects and appends them to the list
            new.append([i.long_name, i.name])  # appends a list with the long and short name
        return new
    except:
        return []


def convertKlassen(hour):
    """:returns a list of lists with the long and short name"""
    try:
        new = []
        for i in hour.klassen:  # goes through all klassen and appends them to the list
            new.append([i.long_name, i.name])  # appends a list with the long and short name
        return new
    except:
        return []


def timetableToPy(timetable):
    """:returns a list of dictionaries one for each hour containing all Characteristics"""
    table = []  # creates a list
    for hour in timetable:  # goes through all hours and appends a dictionary of all Characteristics
        table.append({
            "teachers": convertTeachers(hour),
            "original_teachers": convertOriginalTeachers(hour),
            "rooms": convertRooms(hour),
            "original_rooms": convertOriginalRooms(hour),
            "start": hour.start,
            "end": hour.end,
            "subjects": convertSubjects(hour),
            "klassen": convertKlassen(hour),
            "code": hour.code
        })
    table.sort(key=sort)
    return table


with webuntis.Session(
        username='',  # username
        password='',  # password
        server='tipo.webuntis.com',
        school='TBZ Mitte Bremen',
        useragent='E-Paper AG'
).login() as s:
    with open("test", "wb") as file:
        data = {}

        rooms = s.rooms().filter(name=requestedRooms)
        print(rooms)

        for room in rooms:
            tt = s.timetable(room=room, start=today, end=today)
            data.update({room.name: timetableToPy(tt)})

        pickle.dump(data, file)
        print(data)
