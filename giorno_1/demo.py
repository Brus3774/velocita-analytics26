# giorno_1/demo.py
# VeloCittà Analytics — Funzioni di utilità base

# 1. calcola_durata_minuti

def calcola_durata_minuti(ora_inizio: str, ora_fine: str) -> int:
    """
    Calcola la durata in minuti interi tra due orari in formato "HH:MM".

    Parametri
    ----------
    ora_inizio : str  es. "08:30"
    ora_fine   : str  es. "09:15"

    Ritorna
    -------
    int  — numero di minuti (>= 0)

    Eccezioni
    ---------
    ValueError  — se il formato è errato o ora_fine è precedente a ora_inizio
    """
    def _parse(orario: str):
        parti = orario.split(":")
        if len(parti) != 2:
            raise ValueError(f"Formato non valido: '{orario}'. Atteso 'HH:MM'.")
        ore, minuti = parti
        if not (ore.isdigit() and minuti.isdigit()):
            raise ValueError(f"Formato non valido: '{orario}'. Atteso 'HH:MM'.")
        h, m = int(ore), int(minuti)
        if not (0 <= h <= 23 and 0 <= m <= 59):
            raise ValueError(f"Orario fuori intervallo: '{orario}'.")
        return h * 60 + m

    inizio_min = _parse(ora_inizio)
    fine_min = _parse(ora_fine)

    if fine_min < inizio_min:
        raise ValueError(
            f"ora_fine ('{ora_fine}') è precedente a ora_inizio ('{ora_inizio}')."
        )

    return fine_min - inizio_min


# 2. classifica_corsa


def classifica_corsa(durata_minuti: int) -> str:
    """
    Classifica una corsa in base alla sua durata.

    Parametri
    ----------
    durata_minuti : int  — durata della corsa in minuti (>= 0)

    Ritorna
    -------
    str — "breve" | "media" | "lunga"
    """
    if durata_minuti < 15:
        return "breve"
    elif durata_minuti <= 45:
        return "media"
    else:
        return "lunga"



# 3. Riempilogo corse

def riepilogo_corse(lista_durate: list) -> dict:
    """
    Genera statistiche aggregate su una lista di durate (in minuti).

    Parametri
    ----------
    lista_durate : list[int]  — durate delle corse in minuti

    Ritorna
    -------
    dict con chiavi:
        totale  — numero totale di corse
        media   — durata media (float, arrotondata a 2 decimali; 0 se lista vuota)
        max     — durata massima (None se lista vuota)
        min     — durata minima (None se lista vuota)
        brevi   — conteggio corse "breve"
        medie   — conteggio corse "media"
        lunghe  — conteggio corse "lunga"
    """
    totale = len(lista_durate)

    if totale == 0:
        return {
            "totale": 0,
            "media": 0,
            "max": None,
            "min": None,
            "brevi": 0,
            "medie": 0,
            "lunghe": 0,
        }

    media = round(sum(lista_durate) / totale, 2)
    massimo = max(lista_durate)
    minimo = min(lista_durate)

    brevi = sum(1 for d in lista_durate if classifica_corsa(d) == "breve")
    medie = sum(1 for d in lista_durate if classifica_corsa(d) == "media")
    lunghe = sum(1 for d in lista_durate if classifica_corsa(d) == "lunga")

    return {
        "totale": totale,
        "media": media,
        "max": massimo,
        "min": minimo,
        "brevi": brevi,
        "medie": medie,
        "lunghe": lunghe,
    }


# Demo / smoke test


if __name__ == "__main__":
    print("=== VeloCittà Analytics — Giorno 1 Demo ===\n")

    # --- calcola_durata_minuti ---
    print("--- calcola_durata_minuti ---")
    casi = [
        ("08:00", "08:10"),   # 10 min → breve
        ("07:30", "08:15"),   # 45 min → media
        ("09:00", "10:30"),   # 90 min → lunga
        ("23:50", "23:50"),   # 0 min  → breve (edge case)
    ]
    for inizio, fine in casi:
        durata = calcola_durata_minuti(inizio, fine)
        print(f"  {inizio} → {fine} : {durata} min ({classifica_corsa(durata)})")

    # Verifica ValueError
    print()
    try:
        calcola_durata_minuti("10:00", "09:00")
    except ValueError as e:
        print(f"  ValueError catturato correttamente: {e}")

    # --- riepilogo_corse ---
    print("\n--- riepilogo_corse ---")
    durate_esempio = [10, 20, 30, 5, 60, 45, 14, 46, 25]
    riepilogo = riepilogo_corse(durate_esempio)
    for chiave, valore in riepilogo.items():
        print(f"  {chiave:8}: {valore}")

    # Lista vuota
    print("\n  Lista vuota:")
    riepilogo_vuoto = riepilogo_corse([])
    for chiave, valore in riepilogo_vuoto.items():
        print(f"  {chiave:8}: {valore}")
