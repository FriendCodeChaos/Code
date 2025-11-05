import math,random
from Default_Stuff.Vars.Materials import Materails
from Default_Stuff.Vars.Jobs import Jobs
from Default_Stuff.Vars.people import people

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
