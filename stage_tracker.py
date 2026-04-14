import os
import datetime
from tabulate import tabulate
import data_manager
from fpdf import FPDF
from colorama import Fore, Style, init

# Initialiseer colorama
init(autoreset=True)

def clear_screen():
    """Maakt de terminal leeg voor een propere interface."""
    os.system('cls' if os.name == 'nt' else 'clear')

def toon_tabel(data, titel="ACTUEEL OVERZICHT"):
    """Universele functie om data in tabelvorm te tonen."""
    if not data:
        print("\n[INFO] De tracker is nog leeg.")
        return

    headers = ["ID", "BEDRIJF", "CONTACT", "EMAIL", "TELEFOON", "STATUS", "PRIORITEIT", "ALERT"]
    tabel_data = []
    vandaag = datetime.date.today()

    # We halen de originele data op om de juiste index (ID) te behouden
    originele_data = data_manager.load_data()

    for d in data:
        # Zoek het ID op basis van de index in de originele opgeslagen lijst
        try:
            echt_id = originele_data.index(d)
        except ValueError:
            echt_id = "?" # Voor het geval er iets misgaat

        last_date_str = d.get('datum', str(vandaag))
        try:
            last_date = datetime.datetime.strptime(last_date_str, '%Y-%m-%d').date()
        except:
            last_date = vandaag

        dagen_geleden = (vandaag - last_date).days

        status_raw = d.get('status', '-')
        status_check = status_raw.lower().strip()

        if "gecontacteerd" in status_check:
            status = f"{Fore.YELLOW}{status_raw}{Style.RESET_ALL}"
        elif "in gesprek" in status_check:
            status = f"{Fore.MAGENTA}{status_raw}{Style.RESET_ALL}"
        elif "bevestigd!" in status_check:
            status = f"{Fore.BLUE}{status_raw}{Style.RESET_ALL}"
        else:
            status = status_raw

        alert = ""
        if "gecontacteerd" in status_check and dagen_geleden > 7:
            alert = f"{Fore.RED}{Style.BRIGHT}/!\\ FOLLOW-UP ({dagen_geleden}d){Style.RESET_ALL}"

        tabel_data.append([
            echt_id, # DIT IS NU HET VASTE ID
            d.get('bedrijf', '-'),
            d.get('contact', '-'),
            d.get('email', '-'),
            d.get('telefoon', '-'),
            status,
            d.get('prioriteit', '-'),
            alert
        ])

    print(f"\n--- {titel} ---")
    print(tabulate(tabel_data, headers=headers, tablefmt="fancy_grid"))

def sorteer_data(data):
    """Sorteert de lijst op basis van prioriteit of status."""
    print("\nSORTEER OPTIES:")
    print("1. Prioriteit (Hoog -> Laag)")
    print("2. Prioriteit (Laag -> Hoog)")
    print("3. Status (Alfabetisch)")

    keuze = input("\nHoe wil je sorteren? ")

    if keuze == '1' or keuze == '2':
        volgorde = {"Hoog": 1, "Medium": 2, "Laag": 3}
        data.sort(key=lambda x: volgorde.get(x.get('prioriteit', 'Laag'), 4), reverse=(keuze == '2'))
        print("\n[SUCCES] Tijdelijk gesorteerd op prioriteit.")
    elif keuze == '3':
        data.sort(key=lambda x: x.get('status', '').lower())
        print("\n[SUCCES] Tijdelijk gesorteerd op status.")

    # We slaan de gesorteerde lijst NIET op, zodat de ID's in de JSON hetzelfde blijven
    # Zo blijft ID 0 altijd hetzelfde bedrijf, waar het ook in de tabel staat.
    input("\nSortering toegepast op huidige weergave. Druk op Enter...")

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
    """Genereert een PDF rapport."""
    if not data:
        print("[FOUT] Geen data om te exporteren.")
        return

    pdf = FPDF(orientation='L', unit='mm', format='A4')
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, txt="Gedetailleerd Stage-Tracker Overzicht", ln=True, align='C')
    pdf.ln(10)

    pdf.set_font("Arial", 'B', 10)
    pdf.cell(35, 10, "Bedrijf", 1)
    pdf.cell(35, 10, "Contact", 1)
    pdf.cell(50, 10, "Email", 1)
    pdf.cell(35, 10, "Telefoon", 1)
    pdf.cell(45, 10, "Status", 1)
    pdf.cell(30, 10, "Datum", 1)
    pdf.ln()

    pdf.set_font("Arial", size=9)
    for d in data:
        pdf.cell(35, 10, str(d.get('bedrijf', '-')), 1)
        pdf.cell(35, 10, str(d.get('contact', '-')), 1)
        pdf.cell(50, 10, str(d.get('email', '-')), 1)
        pdf.cell(35, 10, str(d.get('telefoon', '-')), 1)
        pdf.cell(45, 10, str(d.get('status', '-')), 1)
        pdf.cell(30, 10, str(d.get('datum', '-')), 1)
        pdf.ln()

    pdf.output("Stage_Rapport.pdf")
    print("\n[SUCCES] Rapport gegenereerd: Stage_Rapport.pdf")
    input("Enter...")

def main():
    # Belangrijk: we werken met een lokale 'weergave' van de data
    originele_data = data_manager.load_data()

    while True:
        clear_screen()
        print("="*125)
        print("                                     STAGE-TRACKER CRM")
        print("="*125)

        toon_tabel(originele_data)

        print("\nOPTIES:")
        print("1. Toevoegen | 2. Update Status | 3. Verwijderen | 4. Zoeken | 5. Export PDF | 6. Sorteren | 7. Exit")
        print("-" * 125)

        keuze = input("Maak een keuze: ")

        if keuze == '1':
            bedrijf = input("Bedrijf: ")
            contact = input("Contactpersoon: ")
            email = input("Email: ")
            telefoon = input("Telefoon: ")
            status = "Gecontacteerd"
            prioriteit = input("Prioriteit (Hoog/Medium/Laag): ").capitalize()
            vandaag = str(datetime.date.today())

            nieuwe_entry = {
                "bedrijf": bedrijf, "contact": contact, "email": email,
                "telefoon": telefoon, "status": status, "prioriteit": prioriteit,
                "datum": vandaag
            }
            originele_data.append(nieuwe_entry)
            data_manager.save_data(originele_data)

        elif keuze == '2':
            try:
                idx = int(input("ID voor status update: "))
                print("\nBESCHIKBARE OPTIES:")
                print(f"- {Fore.YELLOW}Gecontacteerd{Style.RESET_ALL}")
                print(f"- {Fore.MAGENTA}In gesprek{Style.RESET_ALL}")
                print(f"- {Fore.BLUE}Bevestigd!{Style.RESET_ALL}")

                originele_data[idx]['status'] = input("\nNieuwe status: ")
                originele_data[idx]['datum'] = str(datetime.date.today())
                data_manager.save_data(originele_data)
            except: print("[FOUT] Ongeldig ID.")

        elif keuze == '3':
            try:
                idx = int(input("ID voor verwijderen: "))
                originele_data.pop(idx)
                data_manager.save_data(originele_data)
            except: print("[FOUT] Ongeldig ID.")

        elif keuze == '4':
            zoek_bedrijf(originele_data)

        elif keuze == '5':
            exporteer_naar_pdf(originele_data)

        elif keuze == '6':
            sorteer_data(originele_data)

        elif keuze == '7':
            break

if __name__ == "__main__":
    main()
