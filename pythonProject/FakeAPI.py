import datetime
import pickle
from math import ceil
speed = 5  # in minutes
length = 120  # in minutes
teachers = ["1", "2", "3", "4"]
original_teachers = ["4", "1", "2", "3"]
subjects = ["IFT", "TPR"]
klassen = ["191", "192", "193"]


def timetableToPy(room):
    """:returns a list of dictionaries one for each hour containing all Characteristics"""
    table = []  # creates a list
    for i in range(ceil(120/speed)):  # goes through all hours and appends a dictionary of all Characteristics
        table.append({
            "teachers": teachers[i % len(teachers)],
            "original_teachers": original_teachers[i % len(original_teachers)],
            "rooms": room,
            "original_rooms": rooms[i % len(rooms)],
            "start": datetime.datetime.now().replace(minute=0, second=0, microsecond=0) + datetime.timedelta(minutes=speed*i),
            "end": datetime.datetime.now().replace(minute=0, second=0, microsecond=0) + datetime.timedelta(minutes=speed*(i + 1)),
            "subjects": subjects[i % len(subjects)],
            "klassen": klassen[i % len(klassen)],
            # "code": hour.code
        })
    return table


data = {}
rooms = ["2.312"]
for room in rooms:
    data.update({room: timetableToPy(room)})

with open("test", "wb") as file:
    pickle.dump(data, file)
print(data)
