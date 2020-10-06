import webuntis

s = webuntis.Session(
username='', # username
password='', # password
server='tipo.webuntis.com',
school='TBZ Mitte Bremen',
useragent='E-Paper AG'
).login()

print("Klassen: ---------------------------------")
for klasse in s.klassen():
print(klasse.name)

print("Räume: ---------------------------------")
for time in s.rooms():
print(time.name)

s.logout()