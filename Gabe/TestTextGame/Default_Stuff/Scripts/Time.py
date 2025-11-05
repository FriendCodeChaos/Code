import math,random #math
import os,sys
from contextlib import contextmanager
from pathlib import Path
#make temp mod directory

@contextmanager
def local_directory(path):
    old_dir = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(old_dir)

script_dir = os.path.dirname(os.path.abspath(__file__))
print(script_dir)
with local_directory(script_dir):
    if script_dir not in sys.path:
        sys.path.insert(0, script_dir)

    #scripts
    from GenDay import GenResDay

from Default_Stuff.Vars.Coins import Coins
from Default_Stuff.Vars.Materials import Materails
from Default_Stuff.Vars.people import people


def Time(Days):
    for day in range(0,Days):
        gain = GenResDay()
        people.ammount = people.ammount + gain[0]
        Materails.Wood = Materails.Wood + gain[1]
        Materails.mine.Stone = Materails.mine.Stone + gain[2]
        Materails.mine.Salt = Materails.mine.Salt + gain[3]
        Materails.mine.Coal = Materails.mine.Coal + gain[4]
        Materails.mine.Copper = Materails.mine.Copper + gain[5]
        Materails.mine.Iron = Materails.mine.Iron + gain[6]
        Materails.mine.Gold = Materails.mine.Gold + gain[7]
        Materails.mine.Diamond = Materails.mine.Diamond + gain[8]
        Materails.mine.Platinum = Materails.mine.Platinum + gain[9]
        Coins.Lesser = Coins.Lesser + gain[10]
    people.ammount = math.floor(people.ammount*100)/100
    print(f"you have {math.floor(people.ammount)} people")
