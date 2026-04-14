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

    headers = ["ID", "BEDRIJF", "CONTACT", "EMAIL", "TELEFOON", "STATUS", "PRIORITEIT", "START DATUM", "ALERT"]
    tabel_data = []
    vandaag = datetime.date.today()

    originele_data = data_manager.load_data()

    for d in data:
        try:
            echt_id = originele_data.index(d)
        except ValueError:
            echt_id = "?"

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
            echt_id,
            d.get('bedrijf', '-'),
            d.get('contact', '-'),
            d.get('email', '-'),
            d.get('telefoon', '-'),
            status,
            d.get('prioriteit', '-'),
            d.get('start_datum', '-'),
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
    print("4. Start Datum (Nieuwste eerst)")

    keuze = input("\nHoe wil je sorteren? ")

    if keuze == '1' or keuze == '2':
        volgorde = {"Hoog": 1, "Medium": 2, "Laag": 3}
        data.sort(key=lambda x: volgorde.get(x.get('prioriteit', 'Laag'), 4), reverse=(keuze == '2'))
    elif keuze == '3':
        data.sort(key=lambda x: x.get('status', '').lower())
    elif keuze == '4':
        data.sort(key=lambda x: x.get('start_datum', ''), reverse=True)

    input("\nSortering toegepast. Druk op Enter...")

def zoek_bedrijf(data):
    """Zoekt naar bedrijven of contactpersonen in de lijst."""
    zoekterm = input("\nVoer een zoekterm in (Bedrijf of Contact): ").lower()
    resultaten = [d for d in data if zoekterm in d['bedrijf'].lower() or zoekterm in d['contact'].lower()]

    if resultaten:
        clear_screen()
        toon_tabel(resultaten, titel=f"ZOEKRESULTATEN VOOR: '{zoekterm}'")
    else:
        print(f"\n[!] Geen resultaten gevonden voor '{zoekterm}'.")
    input("\nDruk op Enter...")

def bekijk_nota(data):
    """Toont en bewerkt nota's voor een specifiek ID."""
    try:
        idx = int(input("\nVoer het ID in om de nota te bekijken/bewerken: "))
        bedrijf = data[idx]
        print(f"\n--- NOTA VOOR {bedrijf['bedrijf']} ---")
        print(f"Huidige nota: {bedrijf.get('nota', 'Geen nota gevonden.')}")

        nieuwe_nota = input("\nNieuwe nota (laat leeg om niet te wijzigen): ")
        if nieuwe_nota:
            data[idx]['nota'] = nieuwe_nota
            data_manager.save_data(data)
            print("[SUCCES] Nota bijgewerkt.")
    except:
        print("[FOUT] Ongeldig ID.")
    input("\nEnter om terug te gaan...")

def exporteer_naar_pdf(data):
    """Genereert een PDF rapport."""
    if not data: return
    pdf = FPDF(orientation='L', unit='mm', format='A4')
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, txt="Gedetailleerd Stage-Tracker Overzicht", ln=True, align='C')
    pdf.ln(10)

    pdf.set_font("Arial", 'B', 8)
    cols = ["Bedrijf", "Contact", "Email", "Telefoon", "Status", "Start Datum"]
    for col in cols: pdf.cell(45, 10, col, 1)
    pdf.ln()

    pdf.set_font("Arial", size=8)
    for d in data:
        pdf.cell(45, 10, str(d.get('bedrijf', '-')), 1)
        pdf.cell(45, 10, str(d.get('contact', '-')), 1)
        pdf.cell(45, 10, str(d.get('email', '-')), 1)
        pdf.cell(45, 10, str(d.get('telefoon', '-')), 1)
        pdf.cell(45, 10, str(d.get('status', '-')), 1)
        pdf.cell(45, 10, str(d.get('start_datum', '-')), 1)
        pdf.ln()

    pdf.output("Stage_Rapport.pdf")
    print("\n[SUCCES] Rapport gegenereerd: Stage_Rapport.pdf")
    input("Enter...")

def main():
    originele_data = data_manager.load_data()

    while True:
        clear_screen()
        print("="*125)
        print("                                     STAGE-TRACKER CRM")
        print("="*125)

        toon_tabel(originele_data)

        print("\nOPTIES:")
        print("1. Toevoegen | 2. Update Status | 3. Verwijderen | 4. Zoeken | 5. Export PDF | 6. Sorteren | 7. Nota's | 8. Exit")
        print("-" * 150)

        keuze = input("Maak een keuze: ")

        if keuze == '1':
            bedrijf = input("Bedrijf: ")
            contact = input("Contactpersoon: ")
            email = input("Email: ")
            telefoon = input("Telefoon: ")
            status = "Gecontacteerd"
            prioriteit = input("Prioriteit (Hoog/Medium/Laag): ").capitalize()
            nota = input("Nota (optioneel): ")
            vandaag = str(datetime.date.today())

            nieuwe_entry = {
                "bedrijf": bedrijf, "contact": contact, "email": email,
                "telefoon": telefoon, "status": status, "prioriteit": prioriteit,
                "start_datum": vandaag,
                "datum": vandaag,
                "nota": nota
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
            bekijk_nota(originele_data)

        elif keuze == '8':
            break

if __name__ == "__main__":
    main()
