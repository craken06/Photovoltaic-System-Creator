import json
import os
import math
from db_create import db_create


def obtener_datos_iniciales():
    global CONSUMO, AUTONOMIA, HSP, V_TRABAJO
    os.system("cls")
    print("Configuración inicial de la instalación:")
    
    try:
        CONSUMO = float(input("Introduce el consumo mensual de la instalación (kWh): "))
        AUTONOMIA = float(input("Introduce los días de autonomía: "))
        HSP = float(input("Introduce la hora solar pico: "))
        V_TRABAJO = float(input("Introduce la tensión de trabajo (V): "))
    except ValueError:
        print("Error: Por favor, ingresa valores numéricos válidos!")
        obtener_datos_iniciales()

def seleccionar_panel(paneles_db):
    opciones_posibles = list(range(1, len(paneles_db["Paneles"]) + 1))
    for i, panel in enumerate(paneles_db["Paneles"]):
        nombre = panel["Nombre"]
        modelo = panel["Modelo"]
        print(f"{i+1}. {nombre} {modelo}")
    
    print(f"{len(opciones_posibles) + 1}. Salir")

    try:
        panel_elegido = int(input(f"\nElige un panel para usar ({opciones_posibles[0]} - {opciones_posibles[-1]}): "))
    except ValueError:
        os.system("cls")
        print(f"\nError: Por favor, ingresa un número válido!")
        return seleccionar_panel(paneles_db)

    if panel_elegido == len(opciones_posibles) + 1:
        os.system("cls")
        quit()

    if panel_elegido not in opciones_posibles:
        os.system("cls")
        print(f"\nError: Por favor, elige una opción válida! ({opciones_posibles[0]} - {opciones_posibles[-1]})")
        return seleccionar_panel(paneles_db)

    os.system("cls")
    panel_name = paneles_db["Paneles"][panel_elegido - 1]["Nombre"]
    return panel_elegido, panel_name

def seleccionar_bateria(baterias_db):
    opciones_posibles = list(range(1, len(baterias_db["Baterias"]) + 1))
    for i, bateria in enumerate(baterias_db["Baterias"]):
        nombre = bateria["Nombre"]
        modelo = bateria["Modelo"]
        print(f"{i+1}. {nombre} {modelo}")
    
    print(f"{len(opciones_posibles) + 1}. Salir")

    try:
        bateria_elegida = int(input(f"\nElige una batería para usar ({opciones_posibles[0]} - {opciones_posibles[-1]}): "))
    except ValueError:
        os.system("cls")
        print(f"\nError: Por favor, ingresa un número válido!")
        return seleccionar_bateria(baterias_db)

    if bateria_elegida == len(opciones_posibles) + 1:
        os.system("cls")
        quit()

    if bateria_elegida not in opciones_posibles:
        os.system("cls")
        print(f"\nError: Por favor, elige una opción válida! ({opciones_posibles[0]} - {opciones_posibles[-1]})")
        return seleccionar_bateria(baterias_db)

    os.system("cls")
    bateria_name = baterias_db["Baterias"][bateria_elegida - 1]["Nombre"]
    DOD = float(baterias_db["Baterias"][bateria_elegida - 1]["DOD"])
    return bateria_elegida, bateria_name, DOD

def calcular_panel(panel_elegido, paneles_db, consumo, autonomia, hsp, dod, v_trabajo):
    pm = float(paneles_db["Paneles"][panel_elegido - 1]["Potencia maxima"].strip("W"))

    e_autonomia = autonomia * consumo * 1000 / 30
    e_panel = hsp * pm
    c_bb = e_autonomia * autonomia / (v_trabajo * 0.95 * dod)
    e_bb = c_bb * v_trabajo
    eb_desc = e_bb - e_autonomia
    ec = (e_bb * dod) - eb_desc
    eps = e_autonomia + ec
    c_paneles = eps/(e_panel*1*dod)
    return [round(x, 2) for x in [e_autonomia, e_panel, c_bb, e_bb, eb_desc, ec, eps, c_paneles]]

def calcular_bateria(bateria_elegida, baterias_db, capacidad_total):
    capacidad = float(baterias_db["Baterias"][bateria_elegida - 1]["Capacidad nominal"].strip("Ah"))
    num_baterias = math.ceil(capacidad_total / capacidad)
    return num_baterias

def mostrar_menu_instalacion(panel_name, bateria_name, resultados, num_baterias, consumo, autonomia, hsp, v_trabajo):
    acciones = [
        "Cambiar consumo y parámetros",
        "Elegir otro panel",
        "Elegir otra batería",
        "Salir"
    ]
    unidades = [
        "paneles",
        "baterías"
    ]
    
    while True:
        os.system("cls")
        print(f"Tu instalación con el panel {panel_name} y la batería {bateria_name}:\n")
        print("Menú:\n")
        
        print(f"Número de paneles: {resultados[7]} paneles")
        print(f"Número de baterías: {num_baterias} baterías")
        print(f"Consumo mensual: {consumo} kWh")
        print(f"Consumo diario: {consumo / (autonomia * 30):.2f} kWh")
        
        for i, accion in enumerate(acciones, 1):
            print(f"{i}. {accion}")

        try:
            choice = int(input("¿Qué te gustaría hacer? (1 - 6): "))
        except ValueError:
            os.system("cls")
            print("\nError: Por favor, ingresa un número válido!")
            continue

        if choice == 4:
            os.system("cls")
            quit()
        elif choice == 1:
            return 'cambiar_parametros'
        elif choice == 2:
            return 'cambiar_panel'
        elif choice == 3:
            return 'cambiar_bateria'

def main():
    obtener_datos_iniciales()
    database = db_create()
    paneles_db = database[0]
    baterias_db = database[1]

    while True:
        os.system("cls")
        print("\nMenú:")
        panel_elegido, panel_name = seleccionar_panel(paneles_db)
        bateria_elegida, bateria_name, DOD = seleccionar_bateria(baterias_db)
        resultados = calcular_panel(panel_elegido, paneles_db, CONSUMO, AUTONOMIA, HSP, DOD, V_TRABAJO)
        num_baterias = calcular_bateria(bateria_elegida, baterias_db, resultados[2])
        
        while True:
            accion = mostrar_menu_instalacion(panel_name, bateria_name, resultados, num_baterias, CONSUMO, AUTONOMIA, HSP, V_TRABAJO)
            if accion == 'cambiar_parametros':
                obtener_datos_iniciales()
                resultados = calcular_panel(panel_elegido, paneles_db, CONSUMO, AUTONOMIA, HSP, DOD, V_TRABAJO)
                num_baterias = calcular_bateria(bateria_elegida, baterias_db, resultados[2])
            elif accion == 'cambiar_panel':
                panel_elegido, panel_name = seleccionar_panel(paneles_db)
                resultados = calcular_panel(panel_elegido, paneles_db, CONSUMO, AUTONOMIA, HSP, DOD, V_TRABAJO)
                num_baterias = calcular_bateria(bateria_elegida, baterias_db, resultados[2])
            elif accion == 'cambiar_bateria':
                bateria_elegida, bateria_name, DOD = seleccionar_bateria(baterias_db)
                num_baterias = calcular_bateria(bateria_elegida, baterias_db, resultados[2])

if __name__ == "__main__": 
    main()
