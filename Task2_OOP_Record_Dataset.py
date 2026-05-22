
# Task2_OOP_Record_dataset.py
# VeloCittà Analytics — OOP Parte 1: Record e Dataset

 
# CLASSE BASE: Bicicletta (Modello dei Dati / Entity)


class Bicicletta:
    """Rappresenta una singola bicicletta della flotta VeloCittà."""
 
    # Variabile di classe (Statica): definisce a priori i tipi di veicolo ammessi.
    # Evita errori di battitura o l'inserimento di veicoli non previsti dal software.
    TIPI_VALIDI = {"classica", "elettrica"}
 
    def __init__(
        self,
        id_bici: str,
        tipo: str,
        stazione_corrente: str,
        km_percorsi: float,
        disponibile: bool = True,
    ):
        """Costruttore dell'oggetto: inizializza lo stato iniziale di ogni bici."""
        
        # VALIDAZIONE DI SICUREZZA: Blocca subito la creazione dell'oggetto 
        # se il tipo passato non fa parte del set 'TIPI_VALIDI'.
        if tipo not in self.TIPI_VALIDI:
            raise ValueError(f"Tipo non valido: '{tipo}'. Scegli tra {self.TIPI_VALIDI}.")
        
        # Attributi pubblici (accessibili e modificabili liberamente dall'esterno)
        self.id_bici = id_bici
        self.tipo = tipo
        self.stazione_corrente = stazione_corrente
        self.disponibile = disponibile
        
        # INCAPSULAMENTO (Convenzione): Il prefisso con singolo underscore '_' indica 
        # che questi attributi sono protetti. Non dovrebbero essere modificati direttamente 
        # dall'esterno, ma solo attraverso i metodi della classe (es. restituisci()).
        self._km_percorsi = km_percorsi
        
        # Stato dell'utente: None significa che la bici è ferma in stazione.
        # Diventerà una stringa (il nome dell'utente) quando la bici viene noleggiata.
        self._utente_corrente: str | None = None
 
    #  METODI PRINCIPALI  
 
    def noleggia(self, utente: str) -> str:
        """Cambia lo stato della bici in 'in uso' ed assegna l'utente."""
        # Controllo di stato: se la bici è già occupata, impedisce il doppio noleggio.
        if not self.disponibile:
            raise ValueError(
                f"Bicicletta {self.id_bici} già in uso da '{self._utente_corrente}'."
            )
        
        # Aggiornamento dello stato interno
        self.disponibile = False
        self._utente_corrente = utente
        return f"Bicicletta {self.id_bici} noleggiata a '{utente}'."
 
    def restituisci(self, stazione: str, km_aggiunta: float) -> None:
        """Chiude il noleggio corrente, aggiorna la posizione e i chilometri totali."""
        self.disponibile = True
        self.stazione_corrente = stazione
        
        # Aggiorna il contatore interno accumulando i chilometri dell'ultima corsa
        self._km_percorsi += km_aggiunta
        
        # Svuota il riferimento all'utente, rendendo la bici di nuovo libera per tutti
        self._utente_corrente = None
 
    # RAPPRESENTAZIONE STRINGA
 
    def __str__(self) -> str:
        """Crea una stringa elegante e leggibile pensata per l'utente finale o i report."""
        stato = "✓ disponibile" if self.disponibile else "✗ in uso"
        return (
            f"[{self.id_bici}] {self.tipo} | "
            f"{self.stazione_corrente} | "
            f"{self._km_percorsi:.1f} km | "  # Arrotonda visivamente a 1 cifra decimale
            f"{stato}"
        )
 
    def __repr__(self) -> str:
        """Crea una stringa tecnica. Utile per il debug (es. quando guardi una lista di oggetti)."""
        return (
            f"Bicicletta(id_bici='{self.id_bici}', tipo='{self.tipo}', "
            f"stazione_corrente='{self.stazione_corrente}', "
            f"km_percorsi={self._km_percorsi}, disponibile={self.disponibile})"
        )
 
 
#  CLASSE CONTENITORE: FlottaBici 

class FlottaBici:
    """Gestisce e monitora l'insieme delle biciclette presenti in una città."""
 
    def __init__(self, citta: str):
        self.citta = citta
        # Struttura dati interna: una lista vuota che conterrà oggetti di tipo 'Bicicletta'
        self.biciclette: list[Bicicletta] = []
 
    # METODI CRUD BASE 
 
    def aggiungi(self, bici: Bicicletta) -> None:
        """Inserisce una nuova bicicletta all'interno della flotta."""
        self.biciclette.append(bici)
 
    def rimuovi(self, id_bici: str) -> None:
        """Cancella una bicicletta dalla flotta partendo dal suo ID."""
        # Sfrutta il metodo 'cerca_per_id' definito sotto. Se la bici non esiste,
        # quel metodo lancerà un KeyError, interrompendo la rimozione in sicurezza.
        bici = self.cerca_per_id(id_bici)   
        self.biciclette.remove(bici)
 
    def cerca_per_id(self, id_bici: str) -> Bicicletta:
        """Scansiona l'intera flotta. Ritorna l'oggetto Bicicletta se lo trova."""
        for bici in self.biciclette:
            if bici.id_bici == id_bici:
                return bici
        # Se il ciclo finisce senza trovare nulla, lancia un errore esplicito.
        raise KeyError(f"Bicicletta '{id_bici}' non trovata nella flotta di {self.citta}.")
 
    # METODI DI QUERY & AGGREGAZIONE 
 
    def disponibili(self) -> list[Bicicletta]:
        """Usa una list comprehension per estrarre al volo solo i veicoli liberi."""
        return [b for b in self.biciclette if b.disponibile]
 
    def statistiche(self) -> dict:
        """Esegue calcoli aggregati sulla flotta, simulando le funzioni SQL (COUNT, SUM, AVG)."""
        totale = len(self.biciclette)
        n_disponibili = len(self.disponibili())
        
        # Somma i chilometri leggendo l'attributo protetto '_km_percorsi' di ogni bici
        km_totali = sum(b._km_percorsi for b in self.biciclette)
        
        # Ritorna un report strutturato sotto forma di dizionario Python
        return {
            "totale": totale,
            "disponibili": n_disponibili,
            "in_uso": totale - n_disponibili,
            "km_totali_flotta": round(km_totali, 2),
            # Calcolo della media condizionata: evita l'errore matematico ZeroDivisionError 
            # nel caso in cui la flotta fosse momentaneamente vuota.
            "km_medi_per_bici": round(km_totali / totale, 2) if totale else 0,
        }
 
    # COSTRUTTORE ALTERNATIVO 
 
    @classmethod
    def da_lista(cls, citta: str, dati: list[dict]) -> "FlottaBici":
        """
        Permette di istanziare la flotta partendo da dati grezzi (es. estratti da un file JSON o CSV).
        
        - 'cls' rappresenta la classe stessa (FlottaBici).
        - Riceve una lista di dizionari e si occupa di fare il 'parsing' (conversione) dei dati,
          creando gli oggetti reali 'Bicicletta' uno alla volta.
        """
        # Crea l'istanza della flotta usando il costruttore standard (cls equivale a FlottaBici(citta))
        flotta = cls(citta)
        
        for d in dati:
            # Estrae i dati dalle chiavi del dizionario e mappa i parametri
            bici = Bicicletta(
                id_bici=d["id"],
                tipo=d["tipo"],
                stazione_corrente=d["stazione"],
                km_percorsi=d["km"],
            )
            # Inserisce l'oggetto appena creato nella lista della flotta
            flotta.aggiungi(bici)
            
        # Ritorna l'oggetto flotta interamente popolato e pronto all'uso
        return flotta
 
    # INTEGRAZIONE CON LE FUNZIONI DI SISTEMA 
 
    def __len__(self) -> int:
        """Consente di usare il comando standard len() direttamente sulla flotta (es. len(mia_flotta))."""
        return len(self.biciclette)
 
    def __str__(self) -> str:
        """Rappresentazione testuale sintetica della flotta."""
        return f"FlottaBici({self.citta}) — {len(self)} bici"
 
    def __repr__(self) -> str:
        """Rappresentazione tecnica dettagliata per la console di sviluppo."""
        return f"FlottaBici(citta='{self.citta}', n_bici={len(self)})"
 
 