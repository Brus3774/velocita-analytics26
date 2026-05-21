# VeloCittà Analytics
**Davide Bruseghin**

---

## Descrizione

VeloCittà Analytics è un sistema di analisi end-to-end sviluppato per VeloCittà, startup italiana di bike sharing attiva a Milano, Roma e Torino.
Il progetto simula il lavoro di un analista junior: dalla modellazione dei dati con classi OOP, all'interrogazione teorica con SQL, fino all'elaborazione numerica con NumPy e Pandas e alla visualizzazione dei risultati.
I dati utilizzati sono generati sinteticamente con seed fisso per garantire la riproducibilità dei risultati.
Il progetto è stato sviluppato come elaborato finale del corso Part-Time Master in Data Analytics (Boolean).

---

## Struttura del progetto

```
velocita-analytics26/
├── demo.py                        # Task 1 — Funzioni di utilità
├── Task2_OOP_Record_Dataset.py    # Task 2 — OOP: Record e Dataset
├── Task3_OOP_Regole_principali.py # Task 3 — OOP: Ereditarietà, Incapsulamento, Polimorfismo
├── Task5_Numpy.py                 # Task 5 — Analisi NumPy
├── Task6_Pandas.py                # Task 6 — Analisi Pandas
├── Task7_Visualizzazione.py       # Task 7 — Visualizzazione
├── main.py                        # Entry point con menu interattivo
├── output/                        # Grafici generati (PNG)
├── requirements.txt
└── README.md
```

---

## Dipendenze

```
matplotlib  3.10.9
numpy       2.4.4
pandas      3.0.2
pip         26.1
seaborn     0.13.2
```

Installa tutte le librerie con:

```bash
pip install -r requirements.txt
```

---

## Esecuzione

### Opzione 1 — Menu interattivo (consigliata)

Lancia il `main.py` dalla cartella del progetto:

```bash
cd velocita-analytics26
python main.py
```

Dal menu seleziona la task da eseguire oppure `0` per eseguire tutto in sequenza.

### Opzione 2 — Script singoli

Esegui gli script nell'ordine indicato dalla cartella del progetto:

```bash
python demo.py                        # Task 1 — Funzioni di utilità
python Task2_OOP_Record_Dataset.py    # Task 2 — OOP Record e Dataset
python Task3_OOP_Regole_principali.py # Task 3 — OOP Avanzata
python Task5_Numpy.py                 # Task 5 — Analisi NumPy
python Task6_Pandas.py                # Task 6 — Analisi Pandas
python Task7_Visualizzazione.py       # Task 7 — Visualizzazione
```

> **Nota:** Task 4 (SQL Teorico) non prevede esecuzione Python — le query e le spiegazioni sono contenute in un documento separato.

I grafici vengono salvati automaticamente nella cartella `output/`.

---

## Considerazioni

*(da compilare)*

---

## Requisiti di sistema

- Python 3.10+
- Sistema operativo: Windows 10/11, macOS, Linux
