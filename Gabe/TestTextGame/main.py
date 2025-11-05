import math
import json, os
import importlib.util
import threading
if __name__ == "__main__":
    from Default_Stuff.Vars.Coins import Coins
    from Default_Stuff.Vars.Materials import Materails
    from Default_Stuff.Vars.Jobs import Jobs
    from Default_Stuff.Vars.people import people
    from Default_Stuff.Scripts.Commands import Commands
from Mods import mods
# ----- Save / Load -----
def ClassToJson(cls):
    data = {}
    for key, value in vars(cls).items():
        if key.startswith("__"): continue
        if isinstance(value, type):
            data[key] = ClassToJson(value)
        elif callable(value):
            continue
        else:
            data[key] = value
    return data

def JsonToClass(data, cls):
    for key, value in data.items():
        if hasattr(cls, key):
            attr = getattr(cls, key)
            if isinstance(value, dict) and isinstance(attr, type):
                JsonToClass(value, attr)
            else:
                setattr(cls, key, value)

def DataSave():
    global SaveNamePath
    data = {
        "people": ClassToJson(people),
        "Materails": ClassToJson(Materails),
        "Coins": ClassToJson(Coins),
        "Jobs": ClassToJson(Jobs),
    }
    json_data = json.dumps(data, indent=4)
    os.makedirs("save", exist_ok=True)

    if os.path.exists(SaveNamePath):
        os.remove(SaveNamePath)
    with open(SaveNamePath, "w") as f:
        f.write(json_data)

def LoadData(path):
    if not os.path.exists(path):
        print("Save file not found:", path)
        return False
    with open(path, "r") as f:
        data = json.load(f)

    JsonToClass(data.get("people", {}), people)
    JsonToClass(data.get("Materails", {}), Materails)
    JsonToClass(data.get("Coins", {}), Coins)
    JsonToClass(data.get("Jobs", {}), Jobs)
    return True

ext = "json"
SaveNamePath = ""

def CaculateBornDeath():
    subclasses = [cls for cls in Jobs.__dict__.values() if isinstance(cls, type)]
    born_values = [cls.BornAdd for cls in subclasses]
    death_values = [cls.DeathAdd for cls in subclasses]
    people.born = math.floor(sum(born_values) / len(born_values)*100)/100
    people.death = math.floor(sum(death_values) / len(death_values)*100)/100
    print(people.born, people.death)


def Text():
    global mods
    global SaveNamePath
    Userin = input().strip().lower()
    SplitCommand = Userin.split(" ")
    Commands(SplitCommand)
    mods.run_all("Commands",SplitCommand)
    

    

def main():
    global mods
    global SaveNamePath

    print("type how to play for instructions")
    print("type help for commands")

    for attr in dir(Jobs):
        JobClass = getattr(Jobs, attr)
        if isinstance(JobClass, type):
            for sub_attr in dir(JobClass):
                if not sub_attr.startswith("__"):
                    value = getattr(JobClass, sub_attr)
                    if isinstance(value, (int, float)):
                        setattr(JobClass, sub_attr, value / 100)

    CaculateBornDeath()

    # Load or create save
    while True:
        choice = input("Load save y/n: ").strip().lower()
        if choice == "y":
            name = input("Load Save: ").strip().lower()
            SaveNamePath = f"save/{name}.{ext}"
            if LoadData(SaveNamePath):
                break
        elif choice == "n":
            name = input("Save Name: ").strip().lower()
            SaveNamePath = f"save/{name}.{ext}"
            break

    DataSave()
    print("Loaded mods:", mods.list_mods())

    # Main loop
    if Materails.mine.Salt == 69:
        from Funny import start_cats
        start_cats()
    while True:
        Text()

if __name__ == "__main__":
    main()
