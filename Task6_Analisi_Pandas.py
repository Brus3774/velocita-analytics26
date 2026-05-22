import numpy as np
import pandas as pd
from demo import classifica_corsa

# Blocchiamo il seed del generatore pseudo-casuale per garantire che l'output 
# sia identico ad ogni esecuzione del codice (fondamentale per il testing).
np.random.seed(42)

# Definiamo le costanti di configurazione per la generazione dei dati
N = 80
citta_list      = ["Milano", "Roma", "Torino"]
fasce           = ["mattina", "pomeriggio", "sera", "notte"]
date_list       = ["2026-04-01", "2026-04-15", "2026-05-01"]

#  TABELLA 1: df_corse_base (Il registro dei singoli noleggi) 
df_corse_base = pd.DataFrame({
    # LIST COMPREHENSION + STRING FORMATTING: 
    # Genera codici progressivi univoci formattati con zfill a 3 cifre (es: C001, C002... C080).
    "id_corsa"      : [f"C{str(i).zfill(3)}" for i in range(1, N + 1)],
    
    # Genera identificativi casuali per le biciclette (da B01 a B20). 
    # Essendo N=80, molte biciclette compariranno più volte (relazione Many-to-One).
    "id_bici"       : [f"B{str(np.random.randint(1, 21)).zfill(2)}" for _ in range(N)],
    
    # Associa a caso ogni corsa a uno dei 25 utenti registrati (da U01 a U25).
    "id_utente"     : [f"U{str(np.random.randint(1, 26)).zfill(2)}" for _ in range(N)],
    
    # np.random.choice: Estrae casualmente N elementi dalle liste predefinite.
    "citta"         : np.random.choice(citta_list, size=N),
    "data_corsa"    : np.random.choice(date_list, size=N),
    
    # Genera durate casuali comprese tra 5 e 74 minuti, convertite esplicitamente in float.
    "durata_minuti" : np.random.randint(5, 75, size=N).astype(float),
    
    # np.random.uniform: Genera float continui tra 0.5 e 14.0. 
    # np.round(..., 2) modella il dato simulando la precisione di un GPS (2 cifre decimali).
    "km_percorsi"   : np.round(np.random.uniform(0.5, 14.0, size=N), 2),
    "fascia_oraria" : np.random.choice(fasce, size=N),
})

# ANOMALIA PIANIFICATA 1: Creazione manuale di record duplicati puliti
# .iloc[[...]] estrae le intere righe corrispondenti a quegli indici specifici.
# pd.concat([...], ignore_index=True) appende i duplicati in coda e rigenera l'indice da 0 a 84.
duplicati = df_corse_base.iloc[[0, 5, 10, 20, 35]].copy()
df_corse = pd.concat([df_corse_base, duplicati], ignore_index=True)

# ANOMALIA PIANIFICATA 2: Inserimento di valori mancanti (NaN)
# Scegliamo a caso e senza ripetizioni (replace=False) 4 indici di riga per la durata e 4 per i km.
idx_nan_durata = np.random.choice(df_corse.index, size=4, replace=False)
idx_nan_km     = np.random.choice(df_corse.index, size=4, replace=False)

# L'indicizzatore .loc permette di accedere alle coordinate [righe, colonna] per iniettare 
# il valore sentinella np.nan (Not a Number) di NumPy, che simula la perdita di segnale dei dispositivi.
df_corse.loc[idx_nan_durata, "durata_minuti"] = np.nan
df_corse.loc[idx_nan_km,     "km_percorsi"]   = np.nan


# TABELLA 2: df_bici (Anagrafica hardware dei veicoli) 
df_bici = pd.DataFrame({
    "id_bici"       : [f"B{str(i).zfill(2)}" for i in range(1, 21)], # ID hardware univoci da B01 a B20
    "tipo"          : np.random.choice(["classica", "elettrica"], size=20),
    "citta"         : np.random.choice(citta_list, size=20),
    "anno_acquisto" : np.random.randint(2018, 2025, size=20),
    "costo_acquisto": np.random.choice([299.0, 349.0, 899.0, 1199.0], size=20),
})


# TABELLA 3: df_utenti (Anagrafica dei clienti)
nomi = [
    "Luca Bianchi", "Sara Rossi", "Marco Verdi", "Anna Neri", "Paolo Esposito",
    "Giulia Ricci", "Davide Marino", "Elena Bruno", "Fabio Gallo", "Chiara Conti",
    "Andrea Mancini", "Valentina Costa", "Stefano Greco", "Laura Lombardi", "Roberto Barbieri",
    "Marta Fontana", "Simone Santoro", "Alessia Caruso", "Nicola Ferrara", "Federica Moretti",
    "Tommaso Russo", "Silvia Leone", "Giorgio Colombo", "Irene De Luca", "Emanuele Serra",
]
abbonamenti = ["Base", "Premium", "Premium", "Base", "Premium"]

df_utenti = pd.DataFrame({
    "id_utente"       : [f"U{str(i).zfill(2)}" for i in range(1, 26)], # ID clienti da U01 a U25
    "nome"            : nomi,
    "citta"           : np.random.choice(citta_list, size=25),
    "tipo_abbonamento": np.random.choice(abbonamenti, size=25),
    # pd.date_range: Genera una sequenza di date a intervalli regolari di 45 giorni (freq="45D").
    # .strftime("%Y-%m-%d") converte gli oggetti Timestamp in stringhe ISO standard.
    "data_iscrizione" : pd.date_range("2022-01-01", periods=25, freq="45D").strftime("%Y-%m-%d"),
})

print(" DataFrame creati ")
print(f"  df_corse : {df_corse.shape}  (include 5 duplicati e 8 NaN)")
print(f"  df_bici  : {df_bici.shape}")
print(f"  df_utenti: {df_utenti.shape}")


# PULIZIA DATI 

print("\n Prima della pulizia ")
print(df_corse.info()) # Ispezione strutturale: mostra tipi di colonne e conteggi dei record non nulli
print(df_corse[["durata_minuti", "km_percorsi"]].describe()) # Statistiche descrittive delle colonne numeriche sporse

# Creiamo una copia di lavoro indipendente per evitare il warning 'SettingWithCopyWarning'
df = df_corse.copy()

# FASE 1: RIMOZIONE DUPLICATI 
# .drop_duplicates() elimina le righe che hanno valori identici in tutte le colonne, mantenendo il primo record.
df = df.drop_duplicates()
print(f"\n  Righe dopo drop_duplicates: {len(df)} (rimosse {len(df_corse) - len(df)})")

# FASE 2: IMPUTAZIONE CONTESTUALE DELLE DURATE MANCANTI
# Sfruttiamo il metodo split-apply-combine tramite groupby.
# Per ogni riga in cui 'durata_minuti' è NaN, andiamo a calcolare non la media globale,
# ma la MEDIANA specifica della città di appartenenza della corsa.
# .transform("median") assicura che il risultato mantenga la stessa dimensionalità del DataFrame originale.
df["durata_minuti"] = df["durata_minuti"].fillna(
    df.groupby("citta")["durata_minuti"].transform("median")
)

# FASE 3: IMPUTAZIONE DETERMINISTICA DEI KM MANCANTI (Basata su correlazione)
# Se la distanza è assente, applichiamo un modello matematico deterministico: assumiamo una 
# velocità forfettaria di 0.18 km al minuto (circa 10.8 km/h) e compiliamo il vuoto moltiplicando per i minuti.
df["km_percorsi"] = df["km_percorsi"].fillna(df["durata_minuti"] * 0.18)

# FASE 4: CONVERSIONE TIPOLOGICA (Cast dei dati)
# Trasformiamo la stringa 'data_corsa' in un tipo Datetime reale. Questo ottimizza la memoria 
# e abilita le funzioni del sottomodulo temporale di Pandas (.dt).
df["data_corsa"] = pd.to_datetime(df["data_corsa"])

# FASE 5: FEATURE ENGINEERING TEMPORALE
df["mese"] = df["data_corsa"].dt.month # Estrazione numerica del mese (es: 4 per aprile)

# .dt.day_name() restituisce il nome testuale del giorno in inglese (es: "Monday").
# .map(GIORNI_ITA) agisce come un traduttore, sostituendo le chiavi inglesi con i valori italiani.
GIORNI_ITA = {
    "Monday": "Lunedì", "Tuesday": "Martedì", "Wednesday": "Mercoledì",
    "Thursday": "Giovedì", "Friday": "Venerdì", "Saturday": "Sabato", "Sunday": "Domenica",
}
df["giorno_settimana"] = df["data_corsa"].dt.day_name().map(GIORNI_ITA)

print("\n Dopo la pulizia ")
print(df.info()) # Verifichiamo che i valori non-null siano tornati al 100% (80 su 80)
print(df[["durata_minuti", "km_percorsi"]].describe())


# APPLY E COLONNE DERIVATE (Calcoli riga per riga e Tariffazione)

print("\n Colonne derivate ")

# .apply() con espressione lambda: esegue una funzione personalizzata su ciascun elemento.
# Prende il valore float dei minuti, lo casta a intero e lo passa alla funzione di categorizzazione.
df["tipo_corsa"] = df["durata_minuti"].apply(lambda m: classifica_corsa(int(m)))

# Calcolo vettorizzato della velocità media. Poiché i minuti sono espressi in base 60, 
# la formula corretta è: Spazio / (Tempo / 60). Il tutto viene arrotondato a due decimali (.round(2)).
df["velocita_media"] = (df["km_percorsi"] / (df["durata_minuti"] / 60)).round(2)

# Definiamo un algoritmo per la simulazione della tariffazione aziendale a scaglioni
def calcola_costo(minuti: float) -> float:
    if minuti < 15:
        return 1.50 # Sotto i 15 minuti si applica una quota fissa d'ingresso
    elif minuti <= 45:
        return round(2.50 + 0.10 * (minuti - 15), 2) # Scaglione intermedio: tariffa base + 10 cent/minuto
    else:
        return round(5.00 + 0.08 * (minuti - 45), 2) # Scaglione lungo: tariffa fissa cumulativa + 8 cent/minuto

# Applichiamo la funzione tariffaria alla colonna temporale per calcolare i ricavi di ogni singola corsa
df["costo_stimato"] = df["durata_minuti"].apply(calcola_costo)

# Visualizzazione di controllo in modalità stringa pulita senza indici di riga intermedi
print(df[["id_corsa", "durata_minuti", "tipo_corsa", "velocita_media", "costo_stimato"]].head(10).to_string(index=False))


#  AGGREGAZIONI E MERGE (Business Intelligence ed estrazione KPI)

print("\n Aggregazioni ")

# 1. AGGREGAZIONE NOMINALE PER CITTÀ (GROUP BY)
# Raggruppa i dati per la colonna geometrica 'citta' ed esegue metriche di sintesi differenti 
# su colonne differenti mediante dizionario esplicito (sintassi con "named aggregation").
agg_citta = df.groupby("citta").agg(
    n_corse       =("id_corsa",       "count"), # Conteggio totale delle transazioni
    durata_media  =("durata_minuti",  "mean"),  # Durata media della sessione d'uso
    km_totali     =("km_percorsi",    "sum"),   # Chilometri complessivi percorsi dalla flotta locale
    costo_totale  =("costo_stimato",  "sum"),   # Fatturato totale generato nella città
).round(2)
print("\n  Per città:")
print(agg_citta.to_string())

# 2. AGGREGAZIONE COMPORTAMENTALE PER FASCIA ORARIA
agg_fascia = df.groupby("fascia_oraria").agg(
    n_corse        =("id_corsa",       "count"),
    velocita_media =("velocita_media", "mean"),
).round(2)
print("\n  Per fascia oraria:")
print(agg_fascia.to_string())

# 3. TABELLA PIVOT (Analisi d'incrocio a due vie)
# Genera una matrice bidimensionale: ripartisce le città sulle righe (index) e le categorie 
# di corsa sulle colonne (columns). All'incrocio conta le occorrenze degli ID corsa (aggfunc="count"). 
# fill_value=0 previene la presenza di NaN laddove non vi siano corse per una data combinazione.
pivot = pd.pivot_table(
    df, index="citta", columns="tipo_corsa", values="id_corsa", aggfunc="count", fill_value=0,
)
print("\n  Pivot (città × tipo_corsa — numero corse):")
print(pivot.to_string())

# 4. MERGE MULTIPLO A CATENA (Risoluzione delle relazioni tra tabelle)
# Unisce le tre tabelle separate simulando delle JOIN SQL tramite la concatenazione di metodi.
# how="left" indica una Left Outer Join: preserva tassativamente tutti i record di 'df' (tabella dei log), 
# aggiungendo i dettagli hardware e anagrafici se l'ID combacia, o inserendo NaN in caso contrario.
df_merge = (
    df
    .merge(df_bici,    on="id_bici",    how="left") # Giunzione sulla chiave esterna id_bici
    .merge(df_utenti,  on="id_utente",  how="left") # Giunzione sulla chiave esterna id_utente
)
print(f"\n  Merge df_corse + df_bici + df_utenti → {df_merge.shape}")
print(f"  Colonne: {list(df_merge.columns)}")

print("\n  Prime 5 righe (colonne chiave):")
cols_preview = ["id_corsa", "id_bici", "tipo", "id_utente", "nome", "tipo_abbonamento", "costo_stimato"]
print(df_merge[cols_preview].head().to_string(index=False))

# 5. ESTRAZIONE TOP-N (Classifiche aziendali)
# Isola le 5 biciclette più utilizzate in assoluto in termini di volume di corse.
top_bici = (
    df.groupby("id_bici")["id_corsa"]
    .count()
    .sort_values(ascending=False) # Ordinamento decrescente (dal valore più alto al più basso)
    .head(5)                      # Isola i primi 5 record della serie ordinata
    .reset_index()                # Ripristina l'ID bici come colonna standard manipolabile
    .rename(columns={"id_corsa": "n_corse"}) # Ridenominazione semantica del conteggio
)
print(top_bici.to_string(index=False))

# Isola i top 3 clienti con abbonamento 'Premium' che hanno generato più valore economico.
top_premium = (
    df_merge[df_merge["tipo_abbonamento"] == "Premium"] # Maschera booleana di filtro a monte
    .groupby(["id_utente", "nome"])["costo_stimato"]    # Raggruppamento multi-chiave (ID + Nome dell'utente)
    .sum()
    .sort_values(ascending=False)
    .head(3)
    .reset_index()
)
print(top_premium.to_string(index=False))

# 6. ANALISI Costi (Confronto delle performance dei modelli hardware)
# Calcola indicatori aggregati multipli basandosi sul tipo di bicicletta (Classica vs Elettrica).
costo_tipo = (
    df_merge.groupby("tipo")["costo_stimato"]
    .agg(["mean", "sum", "count"]) # Calcola contemporaneamente valore medio, somma e conteggio
    .round(2)
    .rename(columns={"mean": "costo_medio", "sum": "costo_totale", "count": "n_corse"})
)
print(costo_tipo.to_string())