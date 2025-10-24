import math
import json, os
import importlib.util
import threading
from Default_Stuff.Coins import Coins
from Default_Stuff.Materials import Materails
from Default_Stuff.Jobs import Jobs
from Default_Stuff.people import people
from Default_Stuff.Main import Time

# ----- Setup classes -----
class TimeTrack:
    TotalDay = 0
    Day = 0
    Week = 0
    Month = 0
    Year = 0

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

# ----- People calculation -----
def CaculateBornDeath():
    subclasses = [cls for cls in Jobs.__dict__.values() if isinstance(cls, type)]
    born_values = [cls.BornAdd for cls in subclasses]
    death_values = [cls.DeathAdd for cls in subclasses]
    people.born = math.floor(sum(born_values) / len(born_values)*100)/100
    people.death = math.floor(sum(death_values) / len(death_values)*100)/100
    print(people.born, people.death)

# ----- Mods -----
class Mods:
    def __init__(self, mod_list_file="mods.txt", mod_folder="Mods"):
        self.mod_list_file = mod_list_file
        self.mod_folder = mod_folder
        self._loaded_mods = {}
        self._lock = threading.Lock()

    def load_mods(self):
        choice = input("Load mods from 'mods.txt' or load all mods in folder? (txt/all): ").strip().lower()
        mod_folders = []

        if choice == "txt":
            try:
                with open(self.mod_list_file, "r") as f:
                    mod_folders = [line.strip() for line in f if line.strip()]
                print(f"Loaded mod list from {self.mod_list_file}: {mod_folders}")
            except FileNotFoundError:
                print(f"File '{self.mod_list_file}' not found. No mods loaded.")
                return
        elif choice == "all":
            try:
                mod_folders = [d for d in os.listdir(self.mod_folder)
                               if os.path.isdir(os.path.join(self.mod_folder, d))]
                print(f"Automatically detected mods: {mod_folders}")
            except FileNotFoundError:
                print(f"Mods folder '{self.mod_folder}' not found. No mods loaded.")
                return
        else:
            print("Invalid choice. Please type 'txt' or 'all'.")
            return

        # Load main.py from each mod folder
        for mod_name in mod_folders:
            mod_path = os.path.join(self.mod_folder, mod_name)
            main_py_path = os.path.join(mod_path, 'main.py')

            if os.path.isdir(mod_path) and os.path.isfile(main_py_path):
                try:
                    spec = importlib.util.spec_from_file_location(f"{mod_name}.main", main_py_path)
                    mod = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(mod)
                    with self._lock:
                        self._loaded_mods[mod_name] = mod
                        setattr(self, mod_name, mod)  # optional
                    print(f"Loaded {mod_name}/main.py successfully.")
                except Exception as e:
                    print(f"Failed to load {mod_name}/main.py: {e}")
            else:
                print(f"Skipped {mod_name}: no main.py found.")

    def list_mods(self):
        with self._lock:
            return list(self._loaded_mods.keys())

    def run_time_on_all(self, arg):
        with self._lock:
            for mod_name, mod in self._loaded_mods.items():
                if hasattr(mod, "Time") and callable(getattr(mod, "Time")):
                    try:
                        getattr(mod, "Time")(arg)
                    except Exception as e:
                        print(f"Error calling 'Time({arg})' in mod '{mod_name}': {e}")
                else:
                    print(f"Error Loading '{mod_name}' Error code is 1")

# ----- Commands -----
def Stats():
    print(f"People:{math.floor(people.ammount)}")
    print(f"People per year:{math.floor(people.ammount*people.born)}")
    print(f"Deaths:{math.floor(people.ammount*people.death)}")
    print(f"Salt:{math.floor(Materails.mine.Salt)}")
    # ... add other stats as needed ...

def Help():
    print("type save to save data. Every month it will auto save")
    print("stats for current stats")

def HTP():
    print("To go to the next time you type time")
    print("you then need to type [Day,Week,Month,Year]")
    print("This can be shortened to [D,W,M,Y]")

# ----- Text input -----

def Text():
    global mods
    global SaveNamePath
    Userin = input().strip().lower()
    SplitCommand = Userin.split(" ")

    if SplitCommand[0] == "help":
        Help()
    elif SplitCommand[0] == "how to play":
        HTP()
    elif SplitCommand[0] == "stats":
        Stats()
    elif SplitCommand[0] in ("y", "year"):
        TimeTrack.TotalDay += 365
        mods.run_time_on_all(1)
        Time(365)
    elif SplitCommand[0] == "save":
        DataSave()
    elif SplitCommand[0] == "load":
        if len(SplitCommand) > 1:
            path = f"save/{SplitCommand[1]}.{ext}"
            LoadData(path)
        else:
            LoadData(SaveNamePath)

# ----- Main -----
def main():
    global mods
    global SaveNamePath

    print("type how to play for instructions")
    print("type help for commands")

    # Normalize Jobs percentages
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
    mods = Mods()
    mods.load_mods()
    print("Loaded mods:", mods.list_mods())

    # Main loop
    if Materails.mine.Salt == 69:
        from Funny import start_cats
        start_cats()
    while True:
        Text()

if __name__ == "__main__":
    main()
