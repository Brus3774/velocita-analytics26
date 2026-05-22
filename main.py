# main

# VeloCittà Analytics — Entry point
# Menu interattivo: esegui le task singolarmente o tutte in sequenza.

import sys
import os

# CONFIGURAZIONE DINAMICA DEL PATH DI SISTEMA:
# os.path.dirname(__file__) individua la cartella fisica che contiene questo main.py.
# Os.path.join unisce il percorso alla sottocartella "velocita_analytics" dove risiedono i moduli.
# sys.path.insert(0, ...) inserisce questo percorso in cima all'indice di ricerca di Python (index 0).
# In questo modo, le istruzioni 'from demo import...' o 'import TaskX...' funzioneranno perfettamente
# sia se lanciamo il programma dalla root directory, sia dall'interno della cartella stessa.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "velocita_analytics"))


# Runner per ogni task (Funzioni orchestratrici dei singoli moduli)


def run_task1():
    print("\n" + "=" * 55)
    print("  TASK 1 — Funzioni di utilità (demo.py)")
    print("=" * 55)
    
    # Importazione tardiva: Importiamo le funzioni solo se e quando l'utente 
    # seleziona la Task 1, ottimizzando l'uso iniziale della memoria RAM.
    from demo import (
        calcola_durata_minuti,
        classifica_corsa,
        riepilogo_corse,
    )

    # Caso di test 1: Validazione del calcolo differenziale dei tempi e categorizzazione
    casi = [("08:00", "08:10"), ("07:30", "08:15"), ("09:00", "10:30")]
    for inizio, fine in casi:
        durata = calcola_durata_minuti(inizio, fine)
        print(f"  {inizio} → {fine} : {durata} min ({classifica_corsa(durata)})")

    # Caso di test 2: Verifica della robustezza del codice (Error Handling)
    # Gestiamo l'eccezione lanciata intenzionalmente passando un orario di fine antecedente all'inizio.
    try:
        calcola_durata_minuti("10:00", "09:00")
    except ValueError as e:
        print(f"  ValueError (atteso): {e}")

    # Caso di test 3: Analisi aggregata delle durate mediante dizionari di sintesi
    durate = [10, 20, 30, 5, 60, 45, 14, 46, 25]
    riepilogo = riepilogo_corse(durate)
    print("\n  Riepilogo corse:")
    for k, v in riepilogo.items():
        # Formattazione con padding a destra {:8} per allineare verticalmente i due punti
        print(f"    {k:8}: {v}")


def run_task2():
    print("\n" + "=" * 55)
    print("  TASK 2 — OOP: Record e Dataset")
    print("=" * 55)
    from Task2_OOP_Record_Dataset import Bicicletta, FlottaBici

    # Simulazione di un payload JSON/Dizionario proveniente da un database transazionale
    dati = [
        {"id": "MI-001", "tipo": "elettrica", "stazione": "Cadorna",   "km": 342.5},
        {"id": "MI-002", "tipo": "classica",  "stazione": "Duomo",     "km": 128.0},
        {"id": "MI-003", "tipo": "classica",  "stazione": "Garibaldi", "km": 87.3},
        {"id": "MI-042", "tipo": "elettrica", "stazione": "Loreto",    "km": 510.0},
    ]
    # Inizializzazione della flotta tramite Factory Method statico (.da_lista)
    flotta = FlottaBici.da_lista("Milano", dati)
    print(f"\n  {flotta}")
    for bici in flotta.biciclette:
        print(f"  {bici}") # Sfrutta il metodo magico __str__ ridefinito nella classe Bicicletta

    # Simulazione del ciclo di vita del noleggio hardware
    bici = flotta.cerca_per_id("MI-001")
    print(f"\n  {bici.noleggia('Davide')}") # Cambia lo stato interno del veicolo in occupato
    bici.restituisci("Moscova", 12.4)       # Rilascia la bici, aggiorna la stazione e incrementa i km
    print(f"  Dopo restituzione: {bici}")

    print("\n  Statistiche flotta:")
    for k, v in flotta.statistiche().items():
        print(f"    {k:22}: {v}")


def run_task3():
    print("\n" + "=" * 55)
    print("  TASK 3 — OOP: Ereditarietà, Incapsulamento, Polimorfismo")
    print("=" * 55)
    from Task3_OOP_Regole_principali import (
        BiciclettaClassica,
        BiciclettaElettrica,
        BiciclettaCargo,
        stampa_flotta,
        riepilogo_polimorfismo,
    )

    # Istanziazione di oggetti della gerarchia delle sottoclassi
    classica  = BiciclettaClassica("MI-010", "Duomo",    200.0, taglia="M")
    elettrica = BiciclettaElettrica("MI-020", "Cadorna", 512.0, batteria_percentuale=78)
    scarica   = BiciclettaElettrica("MI-021", "Loreto",  90.0,  batteria_percentuale=15)
    cargo     = BiciclettaCargo("MI-030", "Centrale",   340.0, capacita_kg=80.0)

    # Dimostrazione di Polimorfismo: la stessa funzione processa oggetti diversi esaminandone lo stato
    print("\n  stampa_flotta (polimorfismo):")
    stampa_flotta([classica, elettrica, scarica, cargo])

    # Dimostrazione di Incapsulamento (Proprietà Read-Only)
    classica.aggiungi_km(15.3)
    print(f"\n  {classica.id_bici} dopo aggiungi_km(15.3): {classica.km_percorsi} km")

    # Intercettiamo il tentativo vietato di sovrascrittura diretta di una proprietà privata (@property)
    try:
        classica.km_percorsi = 0
    except AttributeError as e:
        print(f"  AttributeError (sola lettura): {e}")

    # Esecuzione di logiche esclusive di una specifica sottoclasse (BiciclettaElettrica)
    print(f"\n  Ricarica {elettrica.id_bici}: {elettrica.batteria_percentuale}% → ", end="")
    elettrica.ricarica(10)
    print(f"{elettrica.batteria_percentuale}%")

    print("\n  riepilogo_polimorfismo:")
    riepilogo_polimorfismo([classica, elettrica, scarica, cargo])


# METAPROGRAMMAZIONE: Esecuzione dinamica degli script standalone

def _esegui_file(nome_file: str) -> None:
    """Esegue un file .py esterno isolando il runtime, simulando un lancio da terminale."""
    # Ricostruisce il path assoluto del file target per prevenire problemi di posizionamento della working directory
    cartella = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(cartella, nome_file)
    
    with open(path, encoding="utf-8") as f:
        # 1. f.read(): Legge l'intero codice sorgente dello script come stringa.
        # 2. compile(..., "exec"): Compila la stringa in un oggetto codice (bytecode) pronto per l'esecuzione.
        # 3. exec(..., {"__name__": "__main__"}): Esegue il bytecode iniettando un dizionario di globali
        #    fittizio che imposta __name__ a "__main__". Questo forza il trigger dei blocchi 'if __name__ == "__main__":'
        #    all'interno dei file target, garantendo un'esecuzione pulita e isolata ad ogni chiamata.
        exec(compile(f.read(), path, "exec"), {"__name__": "__main__"})


def run_task5():
    print("\n" + "=" * 55)
    print("  TASK 5 — Analisi NumPy")
    print("=" * 55)
    _esegui_file("Task5_Numpy.py")


def run_task6():
    print("\n" + "=" * 55)
    print("  TASK 6 — Analisi Pandas")
    print("=" * 55)
    _esegui_file("Task6_Pandas.py")


def run_task7():
    print("\n" + "=" * 55)
    print("  TASK 7 — Visualizzazione")
    print("=" * 55)
    _esegui_file("Task7_Visualizzazione.py")
    print("  Grafici salvati in output/")


def run_tutto():
    """Batch Processing: Esegue l'intera suite analitica sequenzialmente in un unico blocco."""
    print("\n" + "★" * 55)
    print("  ESECUZIONE COMPLETA — tutte le task in sequenza")
    print("★" * 55)
    # Cicliamo sopra una lista di puntatori a funzione (oggetti di prima classe in Python)
    for runner in [run_task1, run_task2, run_task3, run_task5, run_task6, run_task7]:
        runner()
    print("\n" + "★" * 55)
    print("  Esecuzione completata.")
    print("★" * 55)


# INTERFACCIA UTENTE 

# Stringa multiline stampata a schermo per rappresentare la UI grafica testuale
MENU = """
╔══════════════════════════════════════════╗
║        VeloCittà Analytics — Menu        ║
╠══════════════════════════════════════════╣
║  1  →  Task 1  — Funzioni di utilità    ║
║  2  →  Task 2  — OOP Record & Dataset   ║
║  3  →  Task 3  — OOP Avanzata           ║
║  5  →  Task 5  — NumPy                  ║
║  6  →  Task 6  — Pandas                 ║
║  7  →  Task 7  — Visualizzazione        ║
║  0  →  Esegui tutto                     ║
║  q  →  Esci                             ║
╚══════════════════════════════════════════╝
"""

# DISPATCH PATTERN (Mappatura delle funzioni tramite Dizionario):
# Sostituisce i costrutti nidificati 'if/elif' rendendo il codice O(1) in termini di complessità di ramificazione.
TASK_MAP = {
    "1": run_task1,
    "2": run_task2,
    "3": run_task3,
    "5": run_task5,
    "6": run_task6,
    "7": run_task7,
    "0": run_tutto,
}


def main():
    print(MENU)
    while True:
        # .strip().lower() normalizza l'input dell'utente rimuovendo spazi bianchi e forzando il minuscolo
        scelta = input("  Seleziona un'opzione: ").strip().lower()

        # Condizione di uscita anticipata (Graceful Exit)
        if scelta == "q":
            print("\n  Uscita. Arrivederci!\n")
            sys.exit(0) # Termina il processo Python comunicando al sistema operativo lo stato 0 (nessun errore)

        # Controllo della presenza della chiave nel dizionario delle funzioni
        if scelta in TASK_MAP:
            try:
                TASK_MAP[scelta]() # Invocazione dinamica della funzione agganciata alla chiave
            except Exception as e:
                # Intercetta qualsiasi fallimento a runtime dei file collegati senza far crashare il menu principale
                print(f"\n  ✗ Errore durante l'esecuzione: {e}")
        else:
            print("  Opzione non valida. Riprova.")

        # Gestione del riciclo del menu interattivo
        print("\n" + "-" * 45)
        continua = input("  Tornare al menu? (invio = sì / q = esci): ").strip().lower()
        if continua == "q":
            print("\n  Uscita. Arrivederci!\n")
            sys.exit(0)
        
        print(MENU) # Ristampa il layout del menu per il ciclo successivo


# Assicura che il menu venga avviato solo se lo script viene lanciato direttamente (non se importato)
if __name__ == "__main__":
    main() 