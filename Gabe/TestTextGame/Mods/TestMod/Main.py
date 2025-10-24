import math,random #math
import os,importlib.util,sys #For importing all the other things in the mod
from Default_Stuff.Main import Coins,people,Jobs,Materails

def GenResDay():

    gain = [0] * 11
    MinAmmount = people.ammount/Jobs.Miner.Ammount
    gain[0] = math.floor(((people.ammount*(people.born-people.death+(random.randrange(1,2)/10)))/365)*100)/100
    gain[1] = (people.ammount/Jobs.Lumberjack.Ammount)*3*(random.randrange(1,2)/10) #wood
    gain[2] = MinAmmount*(random.randrange(1,2)/10)*Materails.mine.percent.Stone #stone
    gain[3] = MinAmmount*(random.randrange(1,2)/10)*Materails.mine.percent.Salt #salt
    gain[4] = MinAmmount*(random.randrange(1,2)/10)*Materails.mine.percent.Coal #coal
    gain[5] = MinAmmount*(random.randrange(1,2)/10)*Materails.mine.percent.Copper #copper
    gain[6] = MinAmmount*(random.randrange(1,2)/10)*Materails.mine.percent.Iron #iron
    gain[7] = MinAmmount*(random.randrange(1,2)/10)*Materails.mine.percent.Gold #gold
    gain[8] = MinAmmount*(random.randrange(1,2)/10)*Materails.mine.percent.Diamond #diamond
    gain[9] = MinAmmount*(random.randrange(1,2)/10)*Materails.mine.percent.Platinum #platinum
    gain[10] = 0 #Coins
    for j in range(len(gain)):
        gain[j] = math.floor(gain[j]*100)/100
    for j in range(1,10):
        gain[j] = math.floor(gain[j])
    return gain

    
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

    