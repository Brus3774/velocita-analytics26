# VeloCittà Analytics
**Davide Bruseghin**

---

## Descrizione

VeloCittà Analytics è un sistema di analisi end-to-end sviluppato per VeloCittà, startup italiana di bike sharing attiva a Milano, Roma e Torino.
Il progetto simula il lavoro di un analista junior: dalla modellazione dei dati con classi OOP, all'interrogazione teorica con SQL, fino all'elaborazione numerica con NumPy e Pandas e alla visualizzazione dei risultati.
I dati utilizzati sono generati sinteticamente con seed fisso per garantire la riproducibilità dei risultati.
Il progetto è stato sviluppato come elaborato finale del corso Python per analisi dei dati di Masamune.

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

Nell'esecuzione del programma ci sono stati alcune difficoltà, la prima relativa alla lunghezza del codice, che per essere spiegato e commentato bene ha richiesto diverso tempo e ricerca, soprattutto nelle task 5, 6 e 7. In secondo luogo la parte di pulizia dati e visualizzazione è stata sicuramente la più complessa, nel primo caso soprattutto nella parte di preparazione dei dati e dell'aggregazione, su cui ho dovuto soffermarmi parecchio; mentre nel secondo caso più per una questione di dettagli grafici, su cui si può mettere ampiamente mano e di cui non sono completamente soddisfatto. Proprio questa è la parte che migliorerei perchè di fatto il grafico è il veicolo essenziale per "narrare" i dati dopo averli eleborati e più gli stessi sono chiari meglio comunichi ciò che i dati stanno ad indicare. Per quanto riguarda i dati, generati sinteticamente con seed fisso, mostrano una distribuzione uniforme delle corse tra Milano, Roma e Torino senza città dominanti. Le durate si concentrano prevalentemente nella fascia 15–45 minuti con code simili in tutte le città, e non emergono preferenze orarie significative per tipo di bicicletta. La correlazione tra durata e costo è molto alta per costruzione, mentre velocità e durata risultano scarsamente correlate a causa del fattore random introdotto nella generazione dei km. In un contesto reale ci si aspetterebbe pattern più marcati: picchi orari, differenze tra città e una maggiore domanda di elettriche su percorsi più lunghi.

---

## Requisiti di sistema

- Python 3.10+
- Sistema operativo: Windows 10/11, macOS, Linux
