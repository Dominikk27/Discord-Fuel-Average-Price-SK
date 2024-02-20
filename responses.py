import ceny_paliva


def get_response(user_input: str) -> str:
    lowered: str = user_input.lower()

    if lowered == '!info':
        return 'Čekujem vam ceny paliva kokoti!'

    if lowered == '!ceny':
        prices = ceny_paliva.get_fuelPrices()
        if prices:
            cena_nafty = prices.get("Nafta")
            cena_benzin95 = prices.get("Benzin95")
            cena_benzin98 = prices.get("Benzin98")
            cena_LPG = prices.get("LPG")
            response = (f"Aktuálne ceny palív:\n"
                        f"Nafta: {cena_nafty} € \n"
                        f"Benzín 95: {cena_benzin95} € \n"
                        f"Benzín 98: {cena_benzin98} € \n"
                        f"LPG: {cena_LPG} € \n")
            return response
        else:
            return "Nepodarilo sa získať ceny palív."

