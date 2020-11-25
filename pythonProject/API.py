import webuntis
import datetime
import pickle

requestedRooms = {"2.312", "2.311", "2.310"}

today = datetime.date.today()
monday = today - datetime.timedelta(days=today.weekday())
friday = monday + datetime.timedelta(days=4)


def convertTeachers(hour):
    try:
        new = []
        for i in hour.teachers:
            new.append([i.long_name, i.name])
        return new
    except:
        return []


def convertRooms(hour):
    try:
        new = []
        for i in hour.rooms:
            new.append(i.name)
        return new
    except:
        return []


def convertOriginalTeachers(hour):
    try:
        new = []
        for i in hour.original_teachers:
            new.append([i.long_name, i.name])
        return new
    except:
        return []


def convertOriginalRooms(hour):
    try:
        new = []
        for i in hour.original_rooms:
            new.append(i.name)
        return new
    except:
        return []


def convertSubjects(hour):
    try:
        new = []
        for i in hour.subjects:
            new.append([i.long_name,i.name])
        return new
    except:
        return []


def convertKlassen(hour):
    try:
        new = []
        for i in hour.klassen:
            new.append([i.long_name,i.name])
        return new
    except:
        return []


def timetableToPy(timetable):
    table = []
    for hour in timetable:
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
