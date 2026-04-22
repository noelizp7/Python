# --- CONFIGURACIÓ INICIAL ---
# Hem afegit les llibreries per gestionar els fitxers 
import csv
import os
inventari = []
MAX_EQUIPS = 10

#CONSTANT ARXIU
ARXIU="equips.csv"

# Funció per la persistencia i emmagatzemar les dades
def datos(): 
    global inventari
    if os.path.exists(ARXIU):
        try:
             #whit hem permet la gestió de fitxers segons google com obrir i tancar-los 
            with open(ARXIU, mode='r', enconding='utf-8') as f:
                reader= csv.DictReader(f)
                inventari=[]
                
                print("[SISTEMA] Dades carregades correctament ({len(inventari)} equips).")

        except Exception as e:
            print("[SISTEMA] No s'han pogut carregar les dades]", {e})

    else: 
        print("[SISTEMA] El fitxer no existeix. El inventari començara buit") 

def guardar_dades():
    """Guarda tot l'inventari al fitxer CSV."""
    # Definim les columnes exactament com a la imatge 2
    columnes = ["id", "nom", "aula", "serie", "tipus", "so", "ram", "disc", 
                "estat", "ip", "mac", "obs", "incidencia", "tecnic", "estat_inc"]
    try:
        with open(ARXIU, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=columnes)
            writer.writeheader()
            writer.writerows(inventari)
        print("\n[SISTEMA] Dades guardades correctament.")
    except Exception as e:
        print("[ERROR] No s'han pogut guardar les dades:",{e}) 
                

# --- FUNCIONS DE VALIDACIÓ (Fase 2 i 3) ---

def validar_ram():
    while True:
        try:
            valor = int(input("Introdueix la RAM (GB): "))
            return valor
        except ValueError:
            print(" Error: has d'introduir un número.")

def validar_estat():
    estats_valids = ["operatiu", "avariat", "reparacio", "baixa"]
    while True:
        valor = input(f"Estat ({', '.join(estats_valids)}): ")
        if valor in estats_valids:
            return valor
        print(" Error: estat no vàlid")

def demanar_id_valid():
    try:
        id_cercat = int(input("Introdueix l'ID de l'equip: "))
        for e in inventari:
            if e["id"] == id_cercat:
                return e
        print(" Error: equip no trobat.")
    except ValueError:
        print(" Error: has d'introduir un número.")
    return None



# FER INFORME opcio 8   

def informe(): 
    if not inventari:
        print("No hi ha dades l'inventari per generar l'informe")
        return
    
    nom_informe= "informe-direccio.txt"
    with open(nom_informe, "w", encoding="utf-8") as f:
        f.write("INFORME D'INVENTARI TECNOLÒGIC\n")
        f.write("="*40 + "\n")
        for e in inventari: 
            f.write(f"ID: {e['id']} | Equip: {e['nom']} | Aula: {e['aula']}\n")
            f.write(f"Estat: {e['estat'].upper()} | Incidència: {e['incidencia']}\n")
            f.write("-" * 40 + "\n")
    print("informe", {nom_informe}, "fet de manera exitosa!")





# --- FUNCIONS DE VISUALITZACIÓ ---

def mostrar_resum_aula():
    total = len(inventari)
    operatius = sum(1 for e in inventari if e["estat"] == "operatiu")
    avariats = sum(1 for e in inventari if e["estat"] == "avariat")
    reparacio = sum(1 for e in inventari if e["estat"] == "reparacio")
    baixa = sum(1 for e in inventari if e["estat"] == "baixa")

    print("\n--- RESUM DE L'AULA ---")
    print(f"Total equips: {total}/10")
    print(f"Operatius: {operatius} | Avariats: {avariats} | En reparació: {reparacio} | De baixa: {baixa}")
    print("-" * 25)

def llistar_tots():
    if not inventari:
        print("\n No hi ha equips registrats.")
        return

    print("\nID | Nom                | Aula       | Estat")
    print("-" * 45)
    for e in inventari:
        # Fem servir ljust() per quadrar les columnes
        print(f"{e['id']}  | {e['nom'].ljust(18)} | {e['aula'].ljust(10)} | {e['estat']}")

def mostrar_individual(e):
    print("\n--- INFORMACIÓ DE L'EQUIP ---")
    print(f"ID: {e['id']}")
    print(f"Nom: {e['nom']} | Sèrie: {e['serie']}")
    print(f"Aula: {e['aula']} | Estat: {e['estat']}")
    print(f"SO: {e['so']} | RAM: {e['ram']}GB | Disc: {e['disc']}")
    print(f"Incidència: {e['incidencia']}")
    print(f"Tècnic: {e['tecnic']} | Estat incidència: {e['estat_incidencia']}")

# --- BUCLE PRINCIPAL ---

datos()

while True:
    mostrar_resum_aula()
    print("\n=== AulaManager ===")
    print("1) Registrar equip")
    print("2) Llistar tots els equips")
    print("3) Consultar equip")
    print("4) Canviar estat")
    print("5) Modificar dades")
    print("6) Gestionar incidència")
    print("7 Cercar equip")
    print("8 Generar informe")
    print("0) Sortir")
    
    opcio = input("\nSelecciona una opció: ")

    if opcio == "1":
        if len(inventari) >= MAX_EQUIPS:
            print(" Error: No es poden afegir més equips (màxim 10).")
        else:
            nom = input("Nom de l'equip: ")
            while not nom: nom = input("El nom no pot estar buit: ")
            
            serie = input("Número de sèrie: ")
            while not serie: serie = input("El sèrie no pot estar buit: ")

            nou_equip = {
                "id": len(inventari) + 1,
                "nom": nom,
                "serie": serie,
                "aula": input("Aula: "),
                "so": input("Sistema operatiu: "),
                "ram": validar_ram(),
                "disc": input("Disc: "),
                "estat": validar_estat(),
                "incidencia": "Cap",
                "tecnic": "Cap",
                "estat_incidencia": "resolta"
            }
            inventari.append(nou_equip)
            print(f" Equip '{nom}' registrat amb ID {nou_equip['id']}.")

    elif opcio == "2":
        llistar_tots()

    elif opcio in ["3", "4", "5", "6"]:
        # Totes aquestes opcions requereixen buscar un ID primer
        equip_trobat = demanar_id_valid()
        
        if equip_trobat:
            if opcio == "3":
                mostrar_individual(equip_trobat)
            
            elif opcio == "4":
                print(f"Estat actual de {equip_trobat['nom']}: {equip_trobat['estat']}")
                equip_trobat["estat"] = validar_estat()
                print(" Estat actualitzat.")
            
            elif opcio == "5":
                if input(f"Segur que vols modificar {equip_trobat['nom']}? (s/n): ") == 's':
                    equip_trobat["nom"] = input("Nou nom: ")
                    equip_trobat["aula"] = input("Nova aula: ")
                    equip_trobat["so"] = input("Nou SO: ")
                    equip_trobat["ram"] = validar_ram()
                    equip_trobat["disc"] = input("Nou disc: ")
                    print(" Dades modificades.")
            
            elif opcio == "6":
                equip_trobat["incidencia"] = input("Descripció incidència: ")
                equip_trobat["tecnic"] = input("Tècnic: ")
                est_inc = input("Estat (pendent/resolta): ")
                equip_trobat["estat_incidencia"] = est_inc if est_inc in ["pendent", "resolta"] else "pendent"
                print(" Incidència gestionada.")

    elif opcio == "8":
        informe()

    elif opcio == "0":
        print("Tancant el sistema...")
        break
    else:
        print(" Opció no vàlida.")