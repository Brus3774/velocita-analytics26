
#Task7 - data visualization
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns

# Crea la directory 'output' se non esiste già, evitando errori di scrittura sul disco
os.makedirs("output", exist_ok=True)

# Fissiamo il seed per garantire la perfetta corrispondenza dei dati con il Task 6
np.random.seed(42)

N = 80
citta_list = ["Milano", "Roma", "Torino"]
fasce      = ["mattina", "pomeriggio", "sera", "notte"]
date_list  = ["2026-04-01", "2026-04-15", "2026-05-01"]

# Generazione sintetica del campionamento base delle corse
df_corse_base = pd.DataFrame({
    "id_corsa"      : [f"C{str(i).zfill(3)}" for i in range(1, N + 1)],
    "id_bici"       : [f"B{str(np.random.randint(1, 21)).zfill(2)}" for _ in range(N)],
    "id_utente"     : [f"U{str(np.random.randint(1, 26)).zfill(2)}" for _ in range(N)],
    "citta"         : np.random.choice(citta_list, size=N),
    "data_corsa"    : np.random.choice(date_list, size=N),
    "durata_minuti" : np.random.randint(5, 75, size=N).astype(float),
    "km_percorsi"   : np.round(np.random.uniform(0.5, 14.0, size=N), 2),
    "fascia_oraria" : np.random.choice(fasce, size=N),
})

# Iniezione e successiva rimozione controllata dei record duplicati
duplicati = df_corse_base.iloc[[0, 5, 10, 20, 35]].copy()
df = pd.concat([df_corse_base, duplicati], ignore_index=True).drop_duplicates()

# Generazione di anomalie (NaN) e successiva imputazione statistica condizionata
idx_nan = np.random.choice(df.index, size=4, replace=False)
df.loc[idx_nan, "durata_minuti"] = np.nan
df["durata_minuti"] = df["durata_minuti"].fillna(
    df.groupby("citta")["durata_minuti"].transform("median")
)
df["km_percorsi"] = df["km_percorsi"].fillna(df["durata_minuti"] * 0.18)

# Conversione in oggetto Datetime nativo
df["data_corsa"]  = pd.to_datetime(df["data_corsa"])

# Funzioni di supporto logico-tariffario per il Feature Engineering
def classifica_corsa(m):
    if m < 15:   return "breve"
    elif m <= 45: return "media"
    else:         return "lunga"

def calcola_costo(m):
    if m < 15:   return 1.50
    elif m <= 45: return round(2.50 + 0.10 * (m - 15), 2)
    else:         return round(5.00 + 0.08 * (m - 45), 2)

# Applicazione delle funzioni per estrarre le colonne metriche derivate
df["tipo_corsa"]    = df["durata_minuti"].apply(classifica_corsa)
df["velocita_media"] = (df["km_percorsi"] / (df["durata_minuti"] / 60)).round(2)
df["costo_stimato"] = df["durata_minuti"].apply(calcola_costo)

# Creazione delle tabelle anagrafiche per utenti e biciclette
abbonamenti = ["Base", "Premium", "Premium", "Base", "Premium"]
df_utenti = pd.DataFrame({
    "id_utente"       : [f"U{str(i).zfill(2)}" for i in range(1, 26)],
    "tipo_abbonamento": np.random.choice(abbonamenti, size=25),
})

df_bici = pd.DataFrame({
    "id_bici": [f"B{str(i).zfill(2)}" for i in range(1, 21)],
    "tipo"   : np.random.choice(["classica", "elettrica"], size=20),
})

# Denormalizzazione del database tramite Left Join sequenziali
df_merge = df.merge(df_bici, on="id_bici", how="left").merge(df_utenti, on="id_utente", how="left")


# CONFIGURAZIONE  DEL CORREDO GRAFICO 

# Definiamo una palette categorica fissa per garantire coerenza cromatica tra i grafici
COLORI_CITTA = {"Milano": "#1f77b4", "Roma": "#d62728", "Torino": "#2ca02c"}

# Aggiorniamo i parametri globali del motore di rendering di Matplotlib (plt.rcParams)
plt.rcParams.update({
    "font.family"      : "DejaVu Sans",    # Font cross-platform leggibile
    "font.size"        : 11,               # Dimensione base dei testi
    "axes.spines.top"  : False,            # Rimuove il bordo superiore per pulizia visiva
    "axes.spines.right": False,            # Rimuove il bordo destro (Stile minimalista Chartjunk-free)
    "figure.dpi"       : 120,              # Incrementa la definizione del rendering grafico
})

 
# Grafico 1 — Serie temporale corse per città (Line Plot)
# Domanda: l'utilizzo del servizio è uniforme nelle tre città nelle date disponibili?


# Calcoliamo i volumi aggregando per data e città
serie = df.groupby(["data_corsa", "citta"]).size().reset_index(name="n_corse")

# Inizializzazione orientata agli oggetti (Object-Oriented API di Matplotlib)
fig, ax = plt.subplots(figsize=(9, 4))

# Cicliamo sui sotto-gruppi per tracciare una linea indipendente per ogni città
for citta, gruppo in serie.groupby("citta"):
    ax.plot(gruppo["data_corsa"], gruppo["n_corse"],
            marker="o", label=citta, color=COLORI_CITTA[citta], linewidth=2)

# Elementi di finitura semantica del grafico
ax.set_title("Corse giornaliere per città", fontsize=14, fontweight="bold")
ax.set_xlabel("Data", fontsize=12)
ax.set_ylabel("Numero corse", fontsize=12)
ax.legend(title="Città")

# Formattazione avanzata dell'asse X: mostra i giorni col nome abbreviato del mese (es: 01 Apr)
ax.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter("%d %b"))
ax.tick_params(axis="x", labelsize=9)  # riduce il font delle date

fig.tight_layout() # Ottimizza gli spazi bianchi ed evita la sovrapposizione delle etichette
fig.savefig("output/01_serie_temporale.png")
plt.close(fig)     # Libera la memoria RAM occupata dalla figura
print("  ✓ 01_serie_temporale.png")


# Grafico 2 — Distribuzione durate per città (Istogramma con KDE)
# Domanda: le durate delle corse differiscono tra le città o seguono lo stesso pattern?


# Impostiamo uno sfondo neutro con griglia orizzontale tramite Seaborn
sns.set_theme(style="whitegrid")
fig, ax = plt.subplots(figsize=(9, 4))

# Tracciamo l'istogramma integrando la curva di densità kernel stimata (kde=True)
sns.histplot(data=df, x="durata_minuti", hue="citta",
             kde=True, bins=18, alpha=0.45,
             palette=COLORI_CITTA, ax=ax)

ax.set_title("Distribuzione durate corse per città", fontsize=14, fontweight="bold")
ax.set_xlabel("Durata (minuti)")
ax.set_ylabel("Conteggio")
ax.legend(title="Città", labels=citta_list)

fig.tight_layout()
fig.savefig("output/02_distribuzione_durate.png")
plt.close(fig)
print("  ✓ 02_distribuzione_durate.png")


# Grafico 3 — Corse per fascia oraria e tipo bici (Raggruppato - Bar Plot)
# Domanda: le bici elettriche vengono preferite in fasce orarie specifiche?


# Calcolo delle frequenze condizionate incrociate
agg_fascia_tipo = (
    df_merge.groupby(["fascia_oraria", "tipo"])
    .size().reset_index(name="n_corse")
)
# Forziamo l'ordine logico/cronologico delle categorie sull'asse X
ordine_fasce = ["mattina", "pomeriggio", "sera", "notte"]

fig, ax = plt.subplots(figsize=(9, 4))
# Generiamo il grafico a barre raggruppate impostando la variabile 'hue' sul tipo hardware
sns.barplot(data=agg_fascia_tipo, x="fascia_oraria", y="n_corse",
            hue="tipo", order=ordine_fasce,
            palette={"classica": "#5b8db8", "elettrica": "#f4a261"},
            ax=ax)

ax.set_title("Corse per fascia oraria e tipo bicicletta", fontsize=14, fontweight="bold")
ax.set_xlabel("Fascia oraria")
ax.set_ylabel("Numero corse")
ax.legend(title="Tipo bici")

fig.tight_layout()
fig.savefig("output/03_fasce_orarie.png")
plt.close(fig)
print("  ✓ 03_fasce_orarie.png")


# Grafico 4 — Scatter durata vs. velocità con linea di tendenza (Regressione)
# Domanda: le corse più lunghe tendono ad avere velocità media più bassa?


# Riaffermiamo la rimozione dei bordi esterni per sicurezza estetica
plt.rcParams["axes.spines.top"]   = False
plt.rcParams["axes.spines.right"] = False

fig, ax = plt.subplots(figsize=(8, 5))
# Rappresentazione a dispersione multi-colore differenziata per area urbana
for citta in citta_list:
    sub = df[df["citta"] == citta]
    ax.scatter(sub["durata_minuti"], sub["velocita_media"],
                label=citta, color=COLORI_CITTA[citta], alpha=0.65, s=50)

# INTERPOLAZIONE MATEMATICA (Linea di Tendenza Lineare Globale)
# np.polyfit(X, Y, 1): Calcola i coefficienti (pendenza e intercetta) del polinomio di 1° grado (y = mx + q)
coef = np.polyfit(df["durata_minuti"], df["velocita_media"], 1)
# np.linspace: Crea 200 punti equidistanti tra il minimo e il massimo per una linea continua e fluida
x_line = np.linspace(df["durata_minuti"].min(), df["durata_minuti"].max(), 200)
# np.polyval: Valuta i punti X calcolati applicando i coefficienti della retta stimata
ax.plot(x_line, np.polyval(coef, x_line),
        color="black", linewidth=1.5, linestyle="--", label="Tendenza")

ax.set_title("Durata vs. velocità media", fontsize=14, fontweight="bold")
ax.set_xlabel("Durata (minuti)")
ax.set_ylabel("Velocità media (km/h)")
ax.legend(title="Città")

fig.tight_layout()
fig.savefig("output/04_scatter_durata_velocita.png")
plt.close(fig)
print("  ✓ 04_scatter_durata_velocita.png")


# Grafico 5 — Dashboard riepilogativa (Layout a matrice 2×2 Subplots)

# Inizializziamo una griglia complessa multi-grafico di 2 righe e 2 colonne
fig, axes = plt.subplots(2, 2, figsize=(13, 9))
fig.suptitle("VeloCittà Analytics — Dashboard riepilogativa", fontsize=16, fontweight="bold")

# --- SUBPLOT [0, 0]: In alto a sinistra — Volumi assoluti (Bar Chart) ---
corse_citta = df.groupby("citta").size()
axes[0, 0].bar(corse_citta.index, corse_citta.values,
               color=[COLORI_CITTA[c] for c in corse_citta.index])
axes[0, 0].set_title("Corse per città")
axes[0, 0].set_xlabel("Città")
axes[0, 0].set_ylabel("Numero corse")
# DATA LABELS: Ciclo per posizionare il valore numerico esatto sopra ogni barra verticale
for i, v in enumerate(corse_citta.values):
    axes[0, 0].text(i, v + 0.3, str(v), ha="center", fontsize=10)

# --- SUBPLOT [0, 1]: In alto a destra — Quote abbonati (Pie Chart) ---
abb_counts = df_merge["tipo_abbonamento"].value_counts()
axes[0, 1].pie(abb_counts.values, labels=abb_counts.index,
               autopct="%1.1f%%", startangle=90, # Mostra le percentuali con un decimale
               colors=["#4c9be8", "#e8834c"])
axes[0, 1].set_title("Distribuzione abbonamenti utenti")

# --- SUBPLOT [1, 0]: In basso a sinistra — Monetizzazione (Currency Formatted Bar Chart) ---
costo_citta = df.groupby("citta")["costo_stimato"].sum().round(2)
bars = axes[1, 0].bar(costo_citta.index, costo_citta.values,
                      color=[COLORI_CITTA[c] for c in costo_citta.index])
axes[1, 0].set_title("Costo totale stimato per città")
axes[1, 0].set_xlabel("Città")
axes[1, 0].set_ylabel("€")
# FORMATTER VALUTARIO: Forza l'asse Y a mostrare il simbolo dell'Euro senza decimali
axes[1, 0].yaxis.set_major_formatter(mticker.FormatStrFormatter("€%.0f"))
for bar, val in zip(bars, costo_citta.values):
    axes[1, 0].text(bar.get_x() + bar.get_width() / 2, val + 1,
                    f"€{val:.0f}", ha="center", fontsize=10)

# --- SUBPLOT [1, 1]: In basso a destra — Analisi degli outlier (Boxplot) ---
# Mostra la distribuzione statistica (mediana, quartili e baffi) dei tempi d'uso
sns.boxplot(data=df, x="tipo_corsa", y="durata_minuti",
            hue="tipo_corsa", order=["breve", "media", "lunga"],
            palette={"breve": "#74c476", "media": "#fd8d3c", "lunga": "#de2d26"},
            legend=False, ax=axes[1, 1])
axes[1, 1].set_title("Distribuzione durate per tipo corsa")
axes[1, 1].set_xlabel("Tipo corsa")
axes[1, 1].set_ylabel("Durata (minuti)")

fig.tight_layout()
fig.savefig("output/05_dashboard.png")
plt.close(fig)
print("  ✓ 05_dashboard.png")


# Grafico 6 (extra) — Heatmap correlazione variabili numeriche
# Domanda: quali variabili numeriche sono più correlate tra loro?


fig, ax = plt.subplots(figsize=(6, 5))
# Generiamo la matrice dei coefficienti di correlazione lineare di Pearson (R)
corr = df[["durata_minuti", "km_percorsi", "velocita_media", "costo_stimato"]].corr()

# Disegniamo la mappa di calore impostando la scala simmetrica ancorata tra -1 e 1
sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm",
            vmin=-1, vmax=1, linewidths=0.5, ax=ax)
ax.set_title("Heatmap correlazioni variabili numeriche", fontsize=13, fontweight="bold")

fig.tight_layout()
fig.savefig("output/06_heatmap_correlazioni.png")
plt.close(fig)
print("  ✓ 06_heatmap_correlazioni.png")


# Grafico 7 (extra) — Costo medio per fascia oraria e città (Multi-bar plot)
# Domanda: ci sono differenze di spesa media tra le fasce orarie nelle tre città?


# Aggregazione per estrarre la spesa media (KPI di profittabilità per sessione)
costo_fascia_citta = (
    df.groupby(["fascia_oraria", "citta"])["costo_stimato"]
    .mean().reset_index()
)
fig, ax = plt.subplots(figsize=(9, 4))
sns.barplot(data=costo_fascia_citta, x="fascia_oraria", y="costo_stimato",
            hue="citta", order=ordine_fasce,
            palette=COLORI_CITTA, ax=ax)

ax.set_title("Costo medio per fascia oraria e città", fontsize=14, fontweight="bold")
ax.set_xlabel("Fascia oraria")
ax.set_ylabel("Costo medio (€)")
# Forziamo la formattazione dei decimali in valuta (€0.00)
ax.yaxis.set_major_formatter(mticker.FormatStrFormatter("€%.2f"))
ax.legend(title="Città")

fig.tight_layout()
fig.savefig("output/07_costo_fascia_citta.png")
plt.close(fig)
print("  ✓ 07_costo_fascia_citta.png")

print("\nTutti i grafici salvati in output/") 