import os
import importlib.util
import threading
from time import sleep


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

    def run_all(self, method_name, arg):
        with self._lock:
            for mod_name, mod in self._loaded_mods.items():
                if hasattr(mod, method_name) and callable(getattr(mod, method_name)):
                    try:
                        getattr(mod, method_name)(arg)
                    except Exception as e:
                        print(f"Error calling '{method_name}({arg})' in mod '{mod_name}': {e}")
                else:
                    print(f"Error loading '{mod_name}': method '{method_name}' not found or not callable")

if 'mods' not in globals():
    mods = Mods()
    mods.load_mods()