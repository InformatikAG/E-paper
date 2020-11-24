import pickle

with open("test","rb") as infile:
    tt = pickle.load(infile)

for i in tt:
    print(i["start"])