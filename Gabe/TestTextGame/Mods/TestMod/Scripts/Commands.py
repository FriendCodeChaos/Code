import math
from contextlib import contextmanager


from Mods import mods


from Default_Stuff.Vars.Materials import Materails
from Default_Stuff.Vars.people import people
from Default_Stuff.Scripts.Time import Time
from Default_Stuff.Vars.TimeTrack import TimeTrack
from main import LoadData,DataSave,SaveNamePath,ext
#from main import people,Materails,TimeTrack,mods,Time,DataSave,LoadData,SaveNamePath,ext

def Stats():
    print(f"People:{math.floor(people.ammount)}")
    print(f"People per year:{math.floor(people.ammount*people.born)}")
    print(f"Deaths:{math.floor(people.ammount*people.death)}")
    print(f"Salt:{math.floor(Materails.mine.Salt)}")
def Help():
    print("type save to save data. Every month it will auto save")
    print("stats for current stats")

def HTP():
    print("To go to the next time you type time")
    print("you then need to type [Day,Week,Month,Year]")
    print("This can be shortened to [D,W,M,Y]")


def Commands(SplitCommand):
    if SplitCommand[0] == "help":
        Help()
    elif SplitCommand[0] == "how to play":
        HTP()
    elif SplitCommand[0] == "stats":
        Stats()
    elif SplitCommand[0] in ("y", "year"):
        TimeTrack.TotalDay += 365
        mods.run_all("Time",1)
        Time(365)
    elif SplitCommand[0] == "save":
        DataSave()
    elif SplitCommand[0] == "load":
        if len(SplitCommand) > 1:
            path = f"save/{SplitCommand[1]}.{ext}"
            LoadData(path)
        else:
            LoadData(SaveNamePath)