import os
import sys
from tabulate import tabulate
import data_manager
from fpdf import FPDF

def clear_screen():
    """Maakt de terminal leeg voor een propere interface."""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_valid_priority():
    """Dwingt de gebruiker om een juiste prioriteit te kiezen."""
    geldige_opties = ["Hoog", "Medium", "Laag"]
    while True:
        prio = input("Prioriteit (Hoog/Medium/Laag): ").capitalize()
        if prio in geldige_opties:
            return prio
        print(f"[FOUT] '{prio}' is ongeldig. Kies uit: Hoog, Medium of Laag.")

def toon_tabel(data):
    """Toont de tabel inclusief contactgegevens."""
    if not data:
        print("\n[INFO] De tracker is nog leeg.")
        return

    # We voegen Email en Telefoon toe aan de headers
    headers = ["ID", "BEDRIJF", "CONTACT", "EMAIL", "TELEFOON", "STATUS", "PRIORITEIT"]
    tabel_data = []

    for i, d in enumerate(data):
        # We gebruiken .get() om te voorkomen dat oude data (zonder email/tel) het script doet crashen
        tabel_data.append([
            i,
            d['bedrijf'],
            d['contact'],
            d.get('email', '-'),
            d.get('telefoon', '-'),
            d['status'],
            d['prioriteit']
        ])

    print("\n" + tabulate(tabel_data, headers=headers, tablefmt="fancy_grid"))

def exporteer_naar_pdf(data):
    """Genereert een PDF rapport met alle contactgegevens."""
    if not data:
        print("[FOUT] Geen data om te exporteren.")
        return

    # We gebruiken 'L' (Landscape) omdat de tabel nu breder is
    pdf = FPDF(orientation='L', unit='mm', format='A4')
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, txt="Gedetailleerd Stage-Tracker Overzicht", ln=True, align='C')
    pdf.ln(10)

    # Tabel koppen (breedtes aangepast voor A4 Landscape)
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(35, 10, "Bedrijf", 1)
    pdf.cell(35, 10, "Contact", 1)
    pdf.cell(50, 10, "Email", 1)
    pdf.cell(35, 10, "Telefoon", 1)
    pdf.cell(45, 10, "Status", 1)
    pdf.cell(30, 10, "Prioriteit", 1)
    pdf.ln()

    # Data rijen
    pdf.set_font("Arial", size=9)
    for d in data:
        pdf.cell(35, 10, str(d['bedrijf']), 1)
        pdf.cell(35, 10, str(d['contact']), 1)
        pdf.cell(50, 10, str(d.get('email', '-')), 1)
        pdf.cell(35, 10, str(d.get('telefoon', '-')), 1)
        pdf.cell(45, 10, str(d['status']), 1)
        pdf.cell(30, 10, str(d['prioriteit']), 1)
        pdf.ln()

    pdf.output("Stage_Rapport_Gedetailleerd.pdf")
    print("\n[SUCCES] Gedetailleerd rapport gegenereerd: Stage_Rapport_Gedetailleerd.pdf")
    input("Druk op Enter om door te gaan...")

def main():
    data = data_manager.load_data()

    while True:
        clear_screen()
        print("="*90)
        print("                STAGE-TRACKER CRM v4.0 - CONTACT MANAGEMENT")
        print("="*90)

        toon_tabel(data)

        print("\nOPTIES:")
        print("1. Toevoegen | 2. Update Status | 3. Verwijderen | 4. Export PDF | 5. Exit")
        print("-" * 90)

        keuze = input("Maak een keuze: ")

        if keuze == '1':
            bedrijf = input("Naam bedrijf: ")
            contact = input("Naam contactpersoon: ")
            email = input("E-mailadres: ")
            telefoon = input("Telefoonnummer: ")
            status = "Gecontacteerd"
            prioriteit = get_valid_priority()

            data.append({
                "bedrijf": bedrijf,
                "contact": contact,
                "email": email,
                "telefoon": telefoon,
                "status": status,
                "prioriteit": prioriteit
            })
            data_manager.save_data(data)

        elif keuze == '2':
            if data:
                try:
                    idx = int(input("Voer het ID in: "))
                    nieuwe_status = input("Nieuwe status: ")
                    data[idx]['status'] = nieuwe_status
                    data_manager.save_data(data)
                except (ValueError, IndexError):
                    print("[FOUT] Ongeldig ID.")
                    input("Enter...")

        elif keuze == '3':
            if data:
                try:
                    idx = int(input("Voer het ID in om te verwijderen: "))
                    verwijderd = data.pop(idx)
                    data_manager.save_data(data)
                    print(f"[INFO] {verwijderd['bedrijf']} verwijderd.")
                    input("Enter...")
                except (ValueError, IndexError):
                    print("[FOUT] ID niet gevonden.")
                    input("Enter...")

        elif keuze == '4':
            exporteer_naar_pdf(data)

        elif keuze == '5':
            print("Veel succes met je sollicitaties!")
            break

if __name__ == "__main__":
    main()
