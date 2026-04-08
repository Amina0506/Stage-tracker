import os
import sys
from tabulate import tabulate
import data_manager

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def toon_tabel(data):
    if not data:
        print("\n[INFO] De tracker is nog leeg.")
        return
    headers = ["ID", "BEDRIJF", "CONTACT", "STATUS", "PRIORITEIT"]
    tabel_data = [[i, d['bedrijf'], d['contact'], d['status'], d['prioriteit']] for i, d in enumerate(data)]
    print("\n" + tabulate(tabel_data, headers=headers, tablefmt="fancy_grid"))

def main():
    data = data_manager.load_data()

    while True:
        clear_screen()
        print("="*60)
        print("        STAGE-TRACKER PRO v3.0 - INTERACTIEF")
        print("="*60)
        toon_tabel(data)
        print("\nOPTIONS:")
        print("1. Toevoegen | 2. Update Status | 3. Verwijderen | 4. Exit")
        print("-"*60)

        keuze = input("Wat wil je doen? ")

        if keuze == '1':
            bedrijf = input("Naam bedrijf: ")
            contact = input("Naam contactpersoon: ")
            status = "Gecontacteerd"
            prioriteit = input("Prioriteit (Hoog/Medium/Laag): ")
            data.append({"bedrijf": bedrijf, "contact": contact, "status": status, "prioriteit": prioriteit})
            data_manager.save_data(data)

        elif keuze == '2':
            if data:
                idx = int(input("Voer het ID in van het bedrijf: "))
                nieuwe_status = input("Nieuwe status: ")
                data[idx]['status'] = nieuwe_status
                data_manager.save_data(data)

        elif keuze == '3':
            if data:
                idx = int(input("Voer het ID in om te verwijderen: "))
                verwijderd = data.pop(idx)
                data_manager.save_data(data)
                print(f"[INFO] {verwijderd['bedrijf']} verwijderd.")

        elif keuze == '4':
            print("Afsluiten...")
            break

if __name__ == "__main__":
    main()
