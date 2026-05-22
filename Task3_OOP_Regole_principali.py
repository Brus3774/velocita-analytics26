
# Task3_OOP_Regole_principali.py
# VeloCittà Analytics — OOP Parte 2: Ereditarietà, Incapsulamento, Polimorfismo


from Task2_OOP_Record_Dataset import Bicicletta, FlottaBici


# Incapsulamento nella classe base
# Rinominiamo km_percorsi → _km_percorsi e aggiungiamo property + validazione



# CLASSE BASE ESTESA (Ereditarietà ed Incapsulamento)

class Bicicletta(Bicicletta):
    """
    Estende la classe base aggiungendo incapsulamento su _km_percorsi.
    La base usa già _km_percorsi internamente; qui aggiungiamo la property
    in sola lettura e aggiungi_km() con validazione.
    """

    # INCAPSULAMENTO: Gestione controllata delle variabili interne 
    
    @property
    def km_percorsi(self) -> float:
        """
        PROPERTY IN SOLA LETTURA.
        Consente di leggere il valore di self._km_percorsi dall'esterno chiamando semplicemente
        'bici.km_percorsi' (senza parentesi, come fosse un attributo pubblico), ma impedisce 
        l'assegnazione diretta (es. 'bici.km_percorsi = 100' genererà un errore).
        """
        return self._km_percorsi

    def aggiungi_km(self, km: float) -> None:
        """
        METODO DI VALIDAZIONE (Setter logico).
        È l'unico modo concesso per modificare i chilometri percorsi. Prima di aggiornare 
        la variabile interna, esegue un controllo di sicurezza (i chilometri non possono essere negativi).
        """
        if km <= 0:
            # Se i km passati sono 0 o negativi, blocca l'esecuzione lanciando un'eccezione.
            raise ValueError(f"I km da aggiungere devono essere positivi, ricevuto: {km}.")
        # Se il controllo passa, aggiorna la variabile protetta.
        self._km_percorsi += km

    # OVERRIDE: Riscrittura di un metodo della classe base

    def restituisci(self, stazione: str, km_aggiunta: float) -> None:
        """
        Override del metodo restituisci().
        Sfrutta le caratteristiche della programmazione a oggetti: mantiene la logica di restituzione, 
        ma obbliga il programma a usare il nuovo metodo controllato 'aggiungi_km()' anziché 
        modificare la variabile dei chilometri.
        """
        self.disponibile = True
        self.stazione_corrente = stazione
        
        # Invece di fare 'self._km_percorsi += km_aggiunta' (rischioso), chiama la funzione 
        # con la validazione integrata creata sopra.
        self.aggiungi_km(km_aggiunta)
        
        # Libera la bicicletta cancellando il riferimento all'utente che l'aveva presa.
        self._utente_corrente = None


# SOTTOCLASSI SPECIFICHE (Ereditarietà)


class BiciclettaClassica(Bicicletta):
    """Bicicletta tradizionale con attributo taglia."""

    # Variabile di classe (statica): definisce i confini delle taglie accettabili.
    TAGLIE_VALIDE = {"S", "M", "L"}

    def __init__(self, id_bici, stazione_corrente, km_percorsi, taglia="M", disponibile=True):
        # Controllo di integrità sui dati in ingresso specifici di questa sottoclasse
        if taglia not in self.TAGLIE_VALIDE:
            raise ValueError(f"Taglia non valida: '{taglia}'. Scegli tra {self.TAGLIE_VALIDE}.")
        
        # super().__init__() delega l'inizializzazione dei parametri comuni alla classe madre (Bicicletta),
        # passando automaticamente il tipo fisso "classica".
        super().__init__(id_bici, "classica", stazione_corrente, km_percorsi, disponibile)
        
        # Inizializza l'attributo specifico di questa sottoclasse
        self.taglia = taglia

    # --- METODI MAGICI (Dunder Methods) per la rappresentazione testuale ---

    def __str__(self) -> str:
        """Rappresentazione 'user-friendly' dell'oggetto (usata da print() e str())."""
        stato = "✓ disponibile" if self.disponibile else "✗ in uso"
        return (
            f"[{self.id_bici}] classica (taglia {self.taglia}) | "
            f"{self.stazione_corrente} | "
            f"{self.km_percorsi:.1f} km | {stato}"
        )

    def __repr__(self) -> str:
        """Rappresentazione tecnica/developer dell'oggetto (usata nei log o nelle liste)."""
        return (
            f"BiciclettaClassica(id_bici='{self.id_bici}', taglia='{self.taglia}', "
            f"stazione='{self.stazione_corrente}', km={self.km_percorsi})"
        )


class BiciclettaElettrica(Bicicletta):
    """Bicicletta elettrica con gestione batteria."""

    def __init__(self, id_bici, stazione_corrente, km_percorsi,
                 batteria_percentuale=100, disponibile=True):
        # Validazione dello stato della batteria (deve essere una percentuale reale)
        if not (0 <= batteria_percentuale <= 100):
            raise ValueError("La percentuale batteria deve essere tra 0 e 100.")
        
        # Inizializzazione della classe madre come "elettrica"
        super().__init__(id_bici, "elettrica", stazione_corrente, km_percorsi, disponibile)
        
        # Variabile pseudo-privata per la batteria
        self._batteria_percentuale = batteria_percentuale

    @property
    def batteria_percentuale(self) -> int:
        """Espone la batteria in sola lettura."""
        return self._batteria_percentuale

    def ricarica(self, percentuale: int) -> None:
        """Aggiunge carica al veicolo assicurandosi di non violare le leggi della fisica (max 100%)."""
        if percentuale <= 0:
            raise ValueError("La percentuale di ricarica deve essere positiva.")
        # min(100, ...) impedisce alla batteria di superare il 100% anche se ricarichiamo troppo
        self._batteria_percentuale = min(100, self._batteria_percentuale + percentuale)

    # OVERRIDE CON LOGICA CONDIZIONALE

    def noleggia(self, utente: str) -> str:
        """
        Riscrive il metodo noleggia(). Prima di far partire il noleggio standard,
        controlla che la bici non sia scarica.
        """
        if self._batteria_percentuale < 20:
            raise ValueError(
                f"Batteria insufficiente ({self._batteria_percentuale}%) "
                f"per noleggiare {self.id_bici}. Ricaricare prima."
            )
        # Se la batteria è sufficiente, delega il noleggio alla logica standard della classe madre
        return super().noleggia(utente)

    def __str__(self) -> str:
        stato = "✓ disponibile" if self.disponibile else "✗ in uso"
        return (
            f"[{self.id_bici}] elettrica | "
            f"{self.stazione_corrente} | "
            f"{self.km_percorsi:.1f} km | "
            f"🔋 {self._batteria_percentuale}% | {stato}"
        )

    def __repr__(self) -> str:
        return (
            f"BiciclettaElettrica(id_bici='{self.id_bici}', "
            f"batteria={self._batteria_percentuale}, "
            f"stazione='{self.stazione_corrente}', km={self.km_percorsi})"
        )


class BiciclettaCargo(Bicicletta):
    """Sottoclasse aggiuntiva: bici da carico per consegne pesante."""

    def __init__(self, id_bici, stazione_corrente, km_percorsi,
                 capacita_kg: float = 50.0, disponibile=True):
        if capacita_kg <= 0:
            raise ValueError("La capacità di carico deve essere positiva.")
        super().__init__(id_bici, "classica", stazione_corrente, km_percorsi, disponibile)
        self._capacita_kg = capacita_kg

    @property
    def capacita_kg(self) -> float:
        return self._capacita_kg

    # POLIMORFISMO (Estensione argomenti)

    def noleggia(self, utente: str, peso_carico: float = 0.0) -> str:
        """
        Override di noleggia(). Accetta un parametro opzionale 'peso_carico'.
        Se l'utente prova a caricare più kg di quelli supportati, il noleggio fallisce.
        """
        if peso_carico > self._capacita_kg:
            raise ValueError(
                f"Carico ({peso_carico} kg) supera la capacità massima "
                f"({self._capacita_kg} kg) di {self.id_bici}."
            )
        # Se il peso è corretto, esegue il noleggio standard
        return super().noleggia(utente)

    def __str__(self) -> str:
        stato = "✓ disponibile" if self.disponibile else "✗ in uso"
        return (
            f"[{self.id_bici}] cargo | "
            f"{self.stazione_corrente} | "
            f"{self.km_percorsi:.1f} km | "
            f"⚖️  max {self._capacita_kg} kg | {stato}"
        )

    def __repr__(self) -> str:
        return (
            f"BiciclettaCargo(id_bici='{self.id_bici}', "
            f"capacita_kg={self._capacita_kg}, "
            f"stazione='{self.stazione_corrente}', km={self.km_percorsi})"
        )


# POLIMORFISMO

def stampa_flotta(biciclette: list) -> None:
    """
    Dimostrazione di Polimorfismo: interfaccia comune.
    Questo metodo accetta una lista eterogenea di biciclette (classiche, elettriche, cargo).
    
    Non gli importa sapere di che tipo specifico sia ogni oggetto. Sa solo che sono tutte 'Biciclette'
    e che ognuna risponderà al comando print() usando la propria versione personalizzata di __str__.
    """
    print(f"{'─' * 60}")
    for bici in biciclette:
        print(bici) # Chiama il metodo __str__ specifico della sottoclasse corretta
    print(f"{'─' * 60}")


def riepilogo_polimorfismo(biciclette: list) -> None:
    """
    Dimostrazione di Polimorfismo: comportamento uniforme e gestione errori.
    
    Il programma lancia i comandi generici '.noleggia()' e '.restituisci()'. Sarà l'oggetto stesso, 
    in base alla sua classe di appartenenza, a decidere se far andare a buon fine l'operazione 
    o se sollevare un ValueError (es. se l'elettrica è scarica o la cargo è sovraccarica).
    """
    for bici in biciclette:
        try:
            # Tenta il noleggio polimorfico
            msg = bici.noleggia("test_utente")
            print(f"  ✓ {msg}")
            
            # Se il noleggio ha successo, simula una restituzione immediata 
            # aggiungendo 1 km al contatore attraverso il metodo ereditato/sovrascritto.
            bici.restituisci(bici.stazione_corrente, 1.0)
            
        except ValueError as e:
            # Cattura elegantemente qualsiasi errore di validazione scattato 
            # dentro le specifiche sottoclassi (es. batteria < 20%).
            print(f"  ✗ {bici.id_bici}: {e}") 
