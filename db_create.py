import json
import os
paneles = ""
baterias = ""
inverters = ""
def db_create():
    global paneles
    global baterias
    global inverters

    for db in os.listdir("./db"):
        if db == "paneles.json":
            with open(f"db/{db}") as database:
                paneles = json.load(database)
        if db == "baterias.json":
            with open(f"db/{db}") as database:
                baterias = json.load(database)
        if db == "inverters.json":
            pass
    return paneles, baterias


