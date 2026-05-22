
# Task5_Analisi_numpy.py
# VeloCittà Analytics — Analisi con NumPy

import numpy as np


# Generazione dati (Vettorizzazione e distribuzioni statistici)

# Blocchiamo il generatore di numeri casuali per rendere l'output replicabile ad ogni esecuzione.
np.random.seed(42)

# np.random.normal(28, 12, size=500): Genera 500 numeri basati su una distribuzione normale (Gaussiana) 
# con media di 28 minuti e deviazione standard di 12.
# .astype(int): Converte i decimali generati in numeri interi (le durate delle corse).
# np.clip(..., 1, None): Taglia i valori estremi. Se la distribuzione genera numeri negativi o inferiori a 1 
# (possibile con una deviazione standard alta), li forza a diventare 1. 'None' indica che non c'è un limite massimo.
durate = np.clip(np.random.normal(28, 12, size=500).astype(int), 1, None)

# np.random.uniform(0.15, 0.25, size=500): Genera 500 coefficienti casuali (velocità al minuto in km).
# Calcoliamo la distanza moltiplicando l'array delle durate per questo array di fattori casuali.
# np.round(..., 2): Arrotonda matematicamente ogni distanza a 2 cifre decimali.
km = np.round(durate * np.random.uniform(0.15, 0.25, size=500), 2)

# VETTORIZZAZIONE IN AZIONE: Calcoliamo la velocità in km/h. 
# Dividiamo la durata per 60 per trasformarla in ore, poi dividiamo i km per le ore. 
# NumPy esegue questa operazione in parallelo su tutti i 500 elementi senza alcun ciclo 'for'.
velocita = km / (durate / 60)


def riepilogo_array(nome: str, arr: np.ndarray) -> None:
    """Funzione di supporto per calcolare e stampare le statistiche descrittive di un array."""
    # arr.shape: Mostra le dimensioni dell'array (es. (500,)).
    # arr.dtype: Mostra il tipo di dati memorizzato (es. int64, float64).
    print(f"  {nome:10} | shape: {arr.shape} | dtype: {arr.dtype}")
    
    # Sfrutta le funzioni aggregate native di NumPy per calcolare min, max, media e deviazione standard.
    print(f"              min={arr.min():.2f}  max={arr.max():.2f}"
          f"  media={arr.mean():.2f}  std={arr.std():.2f}")


print(" Generazione dati")
# Ciclo compatto per stampare i riepiloghi dei tre vettori generati
for nome, arr in [("durate", durate), ("km", km), ("velocita", velocita)]:
    riepilogo_array(nome, arr)


# Slicing e selezione (Indicizzazione avanzata e filtri booleani)

print("\n Slicing e selezione ")

# SLICING TRADIZIONALE:
# [:10] estrae i primi 10 elementi (dall'indice 0 al 9).
# [-10:] estrae gli ultimi 10 elementi partendo dal fondo.
print(f"\n  Prime 10 corse (durate):  {durate[:10]}")
print(f"  Ultime 10 corse (durate): {durate[-10:]}")

# FANCY INDEXING: 
# Passando una lista di indici specifici ad un array, NumPy estrae esattamente gli elementi 
# posizionati a quelle coordinate in un colpo solo.
indici = [0, 42, 99, 150, 200, 350, 499]
print(f"\n  Fancy indexing {indici}:")
print(f"  durate = {durate[indici]}")

# MASCHERA BOOLEANA (Filtro):
# 'durate > 45' valuta la condizione su ogni elemento e restituisce un array di 500 valori True o False.
maschera_lunghe = durate > 45

# .sum() su un array booleano conta quanti sono i valori True (poiché True=1 e False=0).
n_lunghe = maschera_lunghe.sum()

# Applichiamo la maschera come filtro all'array 'km': estrarrà solo i chilometri delle corse 
# dove la durata era superiore a 45 minuti, calcolandone poi la media (.mean()).
km_medi_lunghe = km[maschera_lunghe].mean()

print(f"\n  Corse con durata > 45 min: {n_lunghe}")
print(f"  Distanza media di queste corse: {km_medi_lunghe:.2f} km")

# ARGMAX / ARGMIN:
# Non restituiscono il valore massimo/minimo, ma la POSIZIONE (l'indice) in cui si trovano.
idx_vel_max = velocita.argmax()
idx_vel_min = velocita.argmin()

# Usiamo l'indice trovato per estrarre il valore reale corrispondente
print(f"\n  Velocità massima: {velocita[idx_vel_max]:.2f} km/h (indice {idx_vel_max})")
print(f"  Velocità minima:  {velocita[idx_vel_min]:.2f} km/h (indice {idx_vel_min})")


# Statistiche e normalizzazione

print("\n Statistiche e normalizzazione ")

# PERCENTILI:
# np.percentile calcola le soglie sotto le quali ricade una data percentuale di dati.
# Es. il 90° percentile indica il valore di minuti sotto cui si trova il 90% delle corse totali.
percentili = np.percentile(durate, [25, 50, 75, 90])
print(f"\n  Percentili durate:")
for p, v in zip([25, 50, 75, 90], percentili):
    print(f"    {p}° → {v:.1f} min")

# NORMALIZZAZIONE MIN-MAX VETTORIZZATA:
# Applica manualmente la formula (x - min) / (max - min). 
# Tutto l'array viene scalato istantaneamente nell'intervallo [0, 1].
durate_norm = (durate - durate.min()) / (durate.max() - durate.min())
print(f"\n  Normalizzazione min-max:")
print(f"    min={durate_norm.min():.4f}  max={durate_norm.max():.4f}")

# VERIFICA LOGICA CON .all():
# (durate_norm >= 0).all() controlla se OGNI singolo elemento è maggiore o uguale a zero.
# Restituisce True solo se la condizione è soddisfatta al 100%.
print(f"    Valori in [0,1]: {bool((durate_norm >= 0).all() and (durate_norm <= 1).all())}")

# CORRELAZIONE DI PEARSON MANUALE:
# Formula teorica: Covarianza(X, Y) / (DeviazioneStandard(X) * DeviazioneStandard(Y))
# np.cov(durate, km) genera una matrice di covarianza 2x2.
cov_matrix = np.cov(durate, km)
# L'elemento alla posizione [0, 1] (o [1, 0]) è la covarianza incrociata tra le due variabili.
pearson = cov_matrix[0, 1] / (durate.std() * km.std())
print(f"\n  Correlazione di Pearson (durate, km): {pearson:.4f}")
# Un coefficiente vicino a 0.97 indica una fortissima correlazione lineare positiva 
# (com'era prevedibile, all'aumentare dei minuti aumentano proporzionalmente i km).


#  Serie temporale simulata (Algoritmo di Media Mobile)

print("\n Serie temporale (30 giorni) ")

# np.random.randint(80, 200, size=30): Genera un array di 30 numeri interi casuali compresi tra 80 e 199 
# per simulare il volume delle corse quotidiane in un mese.
corse_giornaliere = np.random.randint(80, 200, size=30)

# LOGICA DELLA MEDIA MOBILE A 7 GIORNI CON UNA LIST COMPREHENSION:
# Per ogni giorno 'i' da 0 a 29, calcoliamo la media di una finestra temporale passata.
# max(0, i - 6): Impedisce all'indice di andare in negativo nei primi giorni del mese (giorni da 0 a 5).
# Se siamo al giorno 2 (i=2), la finestra estrarrà i giorni da max(0, -4) ovvero da 0 a 2 (3 giorni disponibili).
# i + 1: Lo slicing esclude l'estremo destro, quindi aggiungiamo +1 per includere il giorno corrente 'i' nel calcolo.
media_mobile = np.array([
    corse_giornaliere[max(0, i - 6): i + 1].mean()
    for i in range(30)
])

# Identifichiamo il giorno del picco massimo e minimo. 
# Aggiungiamo '+1' perché gli indici informatici partono da 0, ma i giorni del calendario partono da 1.
giorno_max = corse_giornaliere.argmax() + 1   
giorno_min = corse_giornaliere.argmin() + 1

print(f"\n  Picco massimo: giorno {giorno_max} ({corse_giornaliere.max()} corse)")
print(f"  Picco minimo:  giorno {giorno_min} ({corse_giornaliere.min()} corse)")

# STAMPA TABELLARE FORMATTATA:
# I modificatori come ':>6' e ':>16.1f' dicono a Python di allineare a destra (>) il testo 
# occupando uno spazio fisso di caratteri (6 o 16), formattando i float a 1 sola cifra decimale (.1f).
print(f"\n  {'Giorno':>6} | {'Corse':>6} | {'Media mobile 7gg':>16}")
print(f"  {'─'*6}-+-{'─'*6}-+-{'─'*16}")
for i in range(30):
    print(f"  {i+1:>6} | {corse_giornaliere[i]:>6} | {media_mobile[i]:>16.1f}")
    