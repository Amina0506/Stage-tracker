import os
from tabulate import tabulate
import data_manager
from fpdf import FPDF

def clear_screen():
    """Maakt de terminal leeg voor een propere interface."""
    os.system('cls' if os.name == 'nt' else 'clear')

def toon_tabel(data, titel="ACTUEEL OVERZICHT"):
    """Universele functie om data in tabelvorm te tonen."""
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
            d.get('bedrijf', '-'),
            d.get('contact', '-'),
            d.get('email', '-'),
            d.get('telefoon', '-'),
            d.get('status', '-'),
            d.get('prioriteit', '-')
        ])

    print(f"\n--- {titel} ---")
    print(tabulate(tabel_data, headers=headers, tablefmt="fancy_grid"))

def zoek_bedrijf(data):
    """Zoekt naar bedrijven of contactpersonen in de lijst."""
    zoekterm = input("\nVoer een zoekterm in (Bedrijf of Contact): ").lower()
    resultaten = [d for d in data if zoekterm in d['bedrijf'].lower() or zoekterm in d['contact'].lower()]

    if resultaten:
        clear_screen()
        toon_tabel(resultaten, titel=f"ZOEKRESULTATEN VOOR: '{zoekterm}'")
    else:
        print(f"\n[!] Geen resultaten gevonden voor '{zoekterm}'.")

    input("\nDruk op Enter om terug te gaan...")

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
        pdf.cell(35, 10, str(d.get('bedrijf', '-')), 1)
        pdf.cell(35, 10, str(d.get('contact', '-')), 1)
        pdf.cell(50, 10, str(d.get('email', '-')), 1)
        pdf.cell(35, 10, str(d.get('telefoon', '-')), 1)
        pdf.cell(45, 10, str(d.get('status', '-')), 1)
        pdf.cell(30, 10, str(d.get('prioriteit', '-')), 1)
        pdf.ln()

    pdf.output("Stage_Rapport.pdf")
    print("\n[SUCCES] Rapport gegenereerd: Stage_Rapport.pdf")
    input("Enter...")

def main():
    data = data_manager.load_data()

    while True:
        clear_screen()
        print("="*90)
        print("                             STAGE-TRACKER - SEARCH ENABLED")
        print("="*90)

        toon_tabel(data)

        print("\nOPTIES:")
        print("1. Toevoegen | 2. Update Status | 3. Verwijderen | 4. Zoeken | 5. Export PDF | 6. Exit")
        print("-" * 90)

        keuze = input("Maak een keuze: ")

        if keuze == '1':
            bedrijf = input("Bedrijf: ")
            contact = input("Contactpersoon: ")
            email = input("Email: ")
            telefoon = input("Telefoon: ")
            status = "Gecontacteerd"
            prioriteit = input("Prioriteit (Hoog/Medium/Laag): ").capitalize()

            data.append({
                "bedrijf": bedrijf, "contact": contact, "email": email,
                "telefoon": telefoon, "status": status, "prioriteit": prioriteit
            })
            data_manager.save_data(data)

        elif keuze == '2':
            try:
                idx = int(input("ID voor status update: "))
                data[idx]['status'] = input("Nieuwe status: ")
                data_manager.save_data(data)
            except: print("[FOUT] Ongeldig ID.")

        elif keuze == '3':
            try:
                idx = int(input("ID voor verwijderen: "))
                data.pop(idx)
                data_manager.save_data(data)
            except: print("[FOUT] Ongeldig ID.")

        elif keuze == '4':
            zoek_bedrijf(data)

        elif keuze == '5':
            exporteer_naar_pdf(data)

        elif keuze == '6':
            break

if __name__ == "__main__":
    main()
