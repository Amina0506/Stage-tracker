# Stage Tracker CLI v3.1 (Pro Edition)

## Projectomschrijving
Deze Python-applicatie is ontwikkeld als onderdeel van het portfolio 'Personal Growth'. Het doel van deze tool is het centraliseren en professionaliseren van de stagezoektocht. Op basis van feedback verkregen tijdens de afstudeerbeurs in Gent, werd de noodzaak voor een gestructureerd overzicht van bedrijfscontacten en sollicitatiestatussen duidelijk.

Deze applicatie overstijgt het reguliere curriculum door het toepassen van **modulaire software-architectuur**, **data-persistentie (JSON)** en **input-validatie**.

## Belangrijkste Functionaliteiten
- **Volledige CRUD-ondersteuning**: Gebruikers kunnen stageplaatsen aanmaken (Create), bekijken (Read), updaten (Update) en verwijderen (Delete) via een interactief menu.
- **Data Persistentie**: Gegevens worden automatisch opgeslagen in een `stages.json` bestand, waardoor informatie bewaard blijft na het afsluiten van de applicatie.
- **Input Validatie & Error Handling**:
    - Gebruikers worden gedwongen om valide prioriteitsniveaus (Hoog/Medium/Laag) te kiezen via een validatie-loop.
    - `Try-except` blokken voorkomen dat de applicatie crasht bij ongeldige ID-invoer.
- **Zoekfunctionaliteit**: Snel filteren op bedrijfsnaam binnen de verzamelde stagecontacten.
- **Geavanceerde Visualisatie**: Gebruik van de `tabulate`-library met een `fancy_grid` layout voor een professionele CLI-ervaring.

## Technische Realisatie
Dit project demonstreert vaardigheden in:
1. **Python Scripting**: Gebruik van loops, list comprehensions en functies.
2. **File I/O**: Werken met JSON voor lokale databasefunctionaliteit.
3. **Versiebeheer**: Een gedetailleerde Git-historie die de evolutie van het script (van basis naar Pro) laat zien.

## Installatie & Gebruik
1. Clone deze repository naar een lokale omgeving.
2. Installeer de noodzakelijke afhankelijkheden:
   ```bash
   pip install -r requirements.txt
