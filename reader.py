import json
import os

#Globales
ruta_json = "db/db.json" # Ruta del json
Panel_db = ""
Resultados = []
panel_name = ""
panel_elegido_ = 0

#Datos para calculo de paneles

Consumo = 300 #En kWh
autonomia = 1 #En dias
hsp = 3.69 #En hora solar pico
Vtrabajo = 48
DoD = 0.9



def dict_create(ruta_json):
    os.system("cls")
    with open(ruta_json) as p_db:
            Panel_db =  json.load(p_db)
    return Panel_db

def do_with_panel():
    print(f"Tu instalacion con el panel {panel_name}:")
    print("")
    print("Menú:")
    print("")
    print("1.Energia de autonomia")
    print("2.Energia del panel")
    print("3.Capacidad del banco de baterias")
    print("4.Energia del banco de baterias")
    print("5.Energia del banco de baterias descargado")
    print("6.Energia a cargar a las baterias")
    print("7.Energia total a suministrar por los paneles")
    print("8.Cantidad de paneles")
    print("9.Salir")
    print("")
    choice = int(input("¿Que te gustaria ver de la instalacion? (1 - 9): "))
    
    if choice == 1:
        os.system("cls")
        print(f"La energia de autonomia es de: {Resultados[choice-1]}Wh")
        print("")
        do_with_panel()
    if choice == 2:
        os.system("cls")
        print(f"La energia de un panel es de: {Resultados[choice-1]}Wh")
        print("")
        do_with_panel()
    if choice == 3:
        os.system("cls")
        print(f"La capacidad del banco de baterias es de: {Resultados[choice-1]}Ah")
        print("")
        do_with_panel()
    if choice == 4:
        os.system("cls")
        print(f"La energia del banco de baterias es de: {Resultados[choice-1]}Ah")
        print("")
        do_with_panel()
    if choice == 5:
        os.system("cls")
        print(f"La energia del banco de baterias descargado es de: {Resultados[choice-1]}Ah")
        print("")
        do_with_panel()
    if choice == 6:
        os.system("cls")
        print(f"La energia a cargar de las baterias es de: {Resultados[choice-1]}Ah")
        print("")
        do_with_panel()
    if choice == 7:
        os.system("cls")
        print(f"La energia total que debe suministrar los paneles es de: {Resultados[choice-1]}Wh")
        print("")
        do_with_panel()
    if choice == 8:
        os.system("cls")
        print(f"La cantidad total de paneles es de: {Resultados[choice-1]}")
        print("")
        do_with_panel()
    if choice == 9:
        os.system("cls")
        return None

def calc_panel(consumo,autonomia,hsp,DoD,Vtrabajo):
    #Sanitizar entrada (Pasar todo a float)
    Vtrabajo = float(Vtrabajo)
    DoD = float(DoD)
    consumo = float(consumo)
    autonomia = float(autonomia)
    hsp = float(hsp)
    Pm = Panel_db["Paneles"][panel_elegido_-1]["Potencia maxima"].strip("W")
    Pm = float(Pm)

    Eautonomia = autonomia * consumo * 1000/30
    Epanel = hsp * Pm
    Cbb = Eautonomia*DoD/(Vtrabajo*0.95*DoD)
    Ebb = Cbb * Vtrabajo
    Eb_desc = Ebb - Eautonomia
    Ec = (Ebb * DoD)-Eb_desc
    Eps =  Eautonomia + Ec
    C_Paneles = Eps/(Epanel*autonomia*0.9)
    Resultados = [Eautonomia,Epanel,Cbb,Ebb,Eb_desc,Ec,Eps,C_Paneles]
    return Resultados

def menu_paneles_creator(ruta_json,Panel_db):
    global panel_elegido_
    global panel_name
    opciones_posibles = [] #Creo una lista para el menu, la lista se crea teniendo en cuenta la cantidad de paneles
    print("\n")
    for i in range(len(Panel_db["Paneles"])): #El for se repite la cantidad de paneles que tengamos
        nombre = Panel_db["Paneles"][i]["Nombre"] #nombre sera el nombre del panel, que se encuentra en el json
        opciones_posibles.append(i+1) #Agrega (del 1 hasta la cantidad de paneles que hayan) para la cantidad de opciones
        print(f"{i+1}. {nombre}") #Imprime el nombre del panel en pantalla

    panel_elegido = int(input(f"\nElige un panel para usar ({opciones_posibles[0]} - {opciones_posibles[-1]}): "))
    os.system("cls")
    panel_name = Panel_db["Paneles"][int(panel_elegido)-1]["Nombre"]
    panel_elegido_ = panel_elegido
    if int(panel_elegido) not in opciones_posibles:
        os.system("cls")
        print(f"\nError: Por favor, elige una opcion posible! ({opciones_posibles[0]} - {opciones_posibles[-1]})")
        menu_paneles_creator(ruta_json)

def main():
    global Panel_db
    global Resultados
    Panel_db = dict_create(ruta_json)
    os.system("cls") #Borro toda la consola
    os.chdir("C:/Users/LUCAS/Desktop/Polaris Solution/db_reader") #Selecciono la ruta de trabajo
    print("\nMenú:")
    menu_paneles_creator(ruta_json,Panel_db)
    Resultados = calc_panel(Consumo,autonomia,hsp,DoD,Vtrabajo)
    do_with_panel()
if __name__ == "__main__": #Flujo del programa
    main()
    