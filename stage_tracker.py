import os
import sys
from tabulate import tabulate
import data_manager
from fpdf import FPDF

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_valid_priority():
    """Nieuwe functie: dwingt de gebruiker om een juiste prioriteit te kiezen."""
    geldige_opties = ["Hoog", "Medium", "Laag"]
    while True:
        prio = input("Prioriteit (Hoog/Medium/Laag): ").capitalize()
        if prio in geldige_opties:
            return prio
        print(f"[FOUT] '{prio}' is ongeldig. Kies uit: Hoog, Medium of Laag.")

def toon_tabel(data):
    if not data:
        print("\n[INFO] De tracker is nog leeg.")
        return
    headers = ["ID", "BEDRIJF", "CONTACT", "STATUS", "PRIORITEIT"]
    tabel_data = [[i, d['bedrijf'], d['contact'], d['status'], d['prioriteit']] for i, d in enumerate(data)]
    print("\n" + tabulate(tabel_data, headers=headers, tablefmt="fancy_grid"))

def exporteer_naar_pdf(data):
    if not data:
        print("[FOUT] Geen data om te exporteren.")
        return

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Stage-Tracker Infos", ln=True, align='C')
    pdf.ln(10)

    # Tabel koppen
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(45, 10, "Bedrijf", 1)
    pdf.cell(45, 10, "Contact", 1)
    pdf.cell(55, 10, "Status", 1)
    pdf.cell(35, 10, "Prioriteit", 1)
    pdf.ln()

    # Data rijen
    pdf.set_font("Arial", size=10)
    for d in data:
        pdf.cell(45, 10, d['bedrijf'], 1)
        pdf.cell(45, 10, d['contact'], 1)
        pdf.cell(55, 10, d['status'], 1)
        pdf.cell(35, 10, d['prioriteit'], 1)
        pdf.ln()

    pdf.output("Stage_Rapport.pdf")
    print("\n[SUCCES] Rapport gegenereerd: Stage_Rapport.pdf")
    input("Druk op Enter om door te gaan...")

def main():
    data = data_manager.load_data()

    while True:
        clear_screen()
        print("="*60)
        print("        STAGE-TRACKER PRO v3.1 - VALIDATIE UPGRADE")
        print("="*60)
        toon_tabel(data)
        print("\nOPTIONS:")
        print("1. Toevoegen | 2. Update Status | 3. Verwijderen | 4. Export PDF | 5. Exit")
        print("-"*60)

        keuze = input("Wat wilt u doen? ")

        if keuze == '1':
            bedrijf = input("Naam bedrijf: ")
            contact = input("Naam contactpersoon: ")
            status = "Gecontacteerd"
            # Gebruik de nieuwe validatie-functie
            prioriteit = get_valid_priority()

            data.append({"bedrijf": bedrijf, "contact": contact, "status": status, "prioriteit": prioriteit})
            data_manager.save_data(data)

        elif keuze == '2':
            if data:
                try:
                    idx = int(input("Voer het ID in van het bedrijf: "))
                    nieuwe_status = input("Nieuwe status: ")
                    data[idx]['status'] = nieuwe_status
                    data_manager.save_data(data)
                except (ValueError, IndexError):
                    print("[FOUT] Ongeldig ID. Voer een cijfer uit de tabel in.")
                    input("Druk op Enter om door te gaan...")

        elif keuze == '3':
            if data:
                try:
                    idx = int(input("Voer het ID in om te verwijderen: "))
                    verwijderd = data.pop(idx)
                    data_manager.save_data(data)
                    print(f"[INFO] {verwijderd['bedrijf']} verwijderd.")
                except (ValueError, IndexError):
                    print("[FOUT] Verwijderen mislukt. ID niet gevonden.")
                    input("Druk op Enter om door te gaan...")

        elif keuze == '4':
            exporteer_naar_pdf(data)

        elif keuze == '5':
            break

if __name__ == "__main__":
    main()
