import os

import requests
from bs4 import BeautifulSoup

from dotenv import load_dotenv


def get_fuelPrices():
    url = os.getenv('website')
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        tables = soup.find_all("table", {"border": "0", "cellspacing": "1", "cellpadding": "1"})

        for table in tables:
            if "Priemerné ceny" in table.text:
                cells_nafta = table.find_all("td", {"id": "ph_nafta"})
                cells_benzin95 = table.find_all("td", {"id": "ph_benzin95"})
                cells_benzin98 = table.find_all("td", {"id": "ph_benzin98"})
                cells_LPG = table.find_all("td", {"id": "ph_lpg"})

                fuel_prices = {}

                if len(cells_nafta) >= 2:
                    cell_nafta = cells_nafta[1]
                    cena_nafty = cell_nafta.find("b").text.strip()
                    fuel_prices["Nafta"] = cena_nafty
                    print("Aktuálna cena nafty:", cena_nafty)

                if len(cells_benzin95) >= 2:
                    cell_benzin95 = cells_benzin95[1]
                    cena_benzin95 = cell_benzin95.find("b").text.strip()
                    fuel_prices["Benzin95"] = cena_benzin95
                    print("Aktuálna cena Benzin95:", cena_benzin95)

                if len(cells_benzin98) >= 2:
                    cell_benzin98 = cells_benzin98[1]
                    cena_benzin98 = cell_benzin98.find("b").text.strip()
                    fuel_prices["Benzin98"] = cena_benzin98
                    print("Aktuálna cena Benzin98:", cena_benzin98)

                if len(cells_LPG) >= 2:
                    cell_LPG = cells_LPG[1]
                    cena_LPG = cell_LPG.find("b").text.strip()
                    fuel_prices["LPG"] = cena_LPG
                    print("Aktuálna cena LPG:", cena_LPG)
        else:
            print("Žiadna tabuľka s aktuálnymi cenami nebola nájdená.")
    else:
        print("Nepodarilo sa načítať zdrojový kód HTML stránky.")

    return fuel_prices