import webuntis

with webuntis.Session(
    username='', # username
    password='', # password
    server='tipo.webuntis.com',
    school='TBZ Mitte Bremen',
    useragent='E-Paper AG'
).login() as s:
    print("Klassen: ---------------------------------")
    for klasse in s.klassen():
        print(klasse.name)