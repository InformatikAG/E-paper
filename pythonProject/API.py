import webuntis
import datetime

with webuntis.Session(
    username='', # username
    password='', # password
    server='tipo.webuntis.com',
    school='TBZ Mitte Bremen',
    useragent='E-Paper AG'
).login() as s:
    today = datetime.date.today()
    monday = today - datetime.timedelta(days=today.weekday())
    friday = monday + datetime.timedelta(days=4)

    print(s.timegrid_units)

    student = s.get_student(surname="otten",fore_name="niklas")
    tt = s.timetable(student=student, start=friday, end=friday)

    def next_hour_start_time(hours):
        delta_time = datetime.timedelta(days=-356)
        for hour in hours:
            if datetime.timedelta() >= (hour.start-datetime.datetime(year=2020, month=10, day=9, hour=10)) > delta_time:
                next_start = hour.start
                delta_time = hour.start-datetime.datetime(year=2020, month=10, day=9, hour=10)
        return next_start

    print(next_hour_start_time(tt))

    for hour in tt:
        if hour.start == datetime.datetime(year=2020, month=10, day=9, hour=10):
            print(hour.subjects)
