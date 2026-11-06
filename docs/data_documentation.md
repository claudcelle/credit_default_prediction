# Documentazione dei dati

Riferimento per l'analisi di **Default of Credit Card Clients**. Consultazione della fonte e verifica del file locale: **6 novembre 2026**.

## Provenienza e licenza

- Fonte ufficiale: [UCI, dataset 350](https://archive.ics.uci.edu/dataset/350/default+of+credit+card+clients).
- Autore: I-Cheng Yeh. DOI: [10.24432/C55S3H](https://doi.org/10.24432/C55S3H).
- Licenza dichiarata da UCI: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Citare il dataset quando si condividono dati o risultati.
- Citazione UCI: Yeh, I. (2009). *Default of Credit Card Clients* [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C55S3H.
- Studio introduttivo indicato da UCI: I. Yeh e Che-hui Lien (2009), *The comparisons of data mining techniques for the predictive accuracy of probability of default of credit card clients*, Expert Systems with Applications.

La fonte descrive clienti di carte di credito a Taiwan e un problema di classificazione del default. Le osservazioni mensili coprono aprile–settembre 2005. La data di donazione a UCI (25 gennaio 2016) non è il periodo di osservazione.

## File locale e caricamento

File: `data/default_of_credit_card_clients.xls`; foglio: `Data`.
SHA-256 del file verificato:

```text
30c6be3abd8dcfd3e6096c828bad8c2f011238620f5369220bd60cfc82700933
```

Il foglio contiene due righe di intestazione: la prima usa gli identificatori UCI, la seconda i nomi descrittivi. Usare `header=1` per ottenere le 25 colonne documentate qui sotto.

```python
from pathlib import Path
import pandas as pd

# Dalla root del repository; da notebooks/ usare ../data/.
path = Path("data/default_of_credit_card_clients.xls")
df = pd.read_excel(path, sheet_name="Data", header=1, engine="xlrd")
target = "default payment next month"
X = df.drop(columns=["ID", target])
y = df[target]
```

Le dipendenze necessarie, pandas e xlrd, sono già dichiarate nel progetto. `code/paths.py` espone anche `RAW_DATA_FILE` per centralizzare il percorso.

## Dizionario delle variabili

Definizioni e codifiche in questa sezione derivano dalla [documentazione UCI](https://archive.ics.uci.edu/dataset/350/default+of+credit+card+clients); i nomi descrittivi sono stati verificati nel foglio locale. Gli importi sono in dollari taiwanesi (NT$), senza conversione o adeguamento monetario.

| ID UCI | Colonna locale | Significato / unità |
| --- | --- | --- |
| ID | `ID` | Identificativo; escludere dai predittori |
| X1 | `LIMIT_BAL` | Credito concesso, NT$; comprende credito individuale e familiare supplementare |
| X2 | `SEX` | Sesso: 1 = maschio, 2 = femmina |
| X3 | `EDUCATION` | Istruzione: 1 = graduate school, 2 = università, 3 = scuola superiore, 4 = altro |
| X4 | `MARRIAGE` | Stato civile: 1 = sposato/a, 2 = single, 3 = altro |
| X5 | `AGE` | Età, anni |
| X6 | `PAY_0` | Stato rimborso, settembre 2005 |
| X7 | `PAY_2` | Stato rimborso, agosto 2005 |
| X8 | `PAY_3` | Stato rimborso, luglio 2005 |
| X9 | `PAY_4` | Stato rimborso, giugno 2005 |
| X10 | `PAY_5` | Stato rimborso, maggio 2005 |
| X11 | `PAY_6` | Stato rimborso, aprile 2005 |
| X12 | `BILL_AMT1` | Importo estratto conto, settembre 2005, NT$ |
| X13 | `BILL_AMT2` | Importo estratto conto, agosto 2005, NT$ |
| X14 | `BILL_AMT3` | Importo estratto conto, luglio 2005, NT$ |
| X15 | `BILL_AMT4` | Importo estratto conto, giugno 2005, NT$ |
| X16 | `BILL_AMT5` | Importo estratto conto, maggio 2005, NT$ |
| X17 | `BILL_AMT6` | Importo estratto conto, aprile 2005, NT$ |
| X18 | `PAY_AMT1` | Pagamento effettuato, settembre 2005, NT$ |
| X19 | `PAY_AMT2` | Pagamento effettuato, agosto 2005, NT$ |
| X20 | `PAY_AMT3` | Pagamento effettuato, luglio 2005, NT$ |
| X21 | `PAY_AMT4` | Pagamento effettuato, giugno 2005, NT$ |
| X22 | `PAY_AMT5` | Pagamento effettuato, maggio 2005, NT$ |
| X23 | `PAY_AMT6` | Pagamento effettuato, aprile 2005, NT$ |
| Y | `default payment next month` | Target: 1 = default, 0 = assenza di default nel mese successivo |

Per `PAY_0`, `PAY_2`, …, `PAY_6`, UCI definisce −1 = pagamento regolare; 1–8 = ritardo di altrettanti mesi; 9 = ritardo di almeno nove mesi. La pagina consultata non definisce −2 e 0, pur presenti nel file. Non attribuire loro un significato senza un'ulteriore fonte. Il codice 9 è documentato ma non osservato nel file locale.

Attenzione: `PAY_1` non esiste. Il periodo più recente è `PAY_0`, allineato a `BILL_AMT1` e `PAY_AMT1`; gli indici successivi procedono verso il passato. Il mese target è successivo alla finestra osservata; ottobre 2005 è un'inferenza dalla sequenza temporale e dal nome della colonna. La pagina UCI non precisa una soglia operativa di default in giorni.

## Riscontri sul file locale

Questi risultati sono calcolati sul file presente nel repository, senza pulizia o trasformazioni.

| Controllo | Risultato |
| --- | --- |
| Dimensioni | 30.000 righe × 25 colonne: ID, 23 predittori, target |
| Tipi letti da pandas | Tutte le colonne `int64`; questo non implica che siano tutte quantitative |
| Valori nulli secondo `isna()` | 0 |
| ID | Univoci, da 1 a 30.000 |
| Duplicati su tutte le colonne | 0 |
| Duplicati escludendo solo ID | 35 righe successive alla prima occorrenza |
| Target 0 | 23.364 (77,88%) |
| Target 1 | 6.636 (22,12%) |
| `LIMIT_BAL` | 10.000–1.000.000 NT$ |
| `AGE` | 21–79 anni |

### Codifiche da approfondire

| Colonna / famiglia | Riscontro | Interpretazione per l'analisi |
| --- | --- | --- |
| `EDUCATION` | 0: 14 righe; 5: 280; 6: 51 | Codici non definiti dalla pagina UCI; 345 righe totali |
| `MARRIAGE` | 0: 54 righe | Codice non definito dalla pagina UCI |
| Stati `PAY_*` | −2 e 0 presenti in tutte e sei le colonne | Semantica non definita dalla pagina consultata |
| `BILL_AMT1`–`BILL_AMT6` | Valori negativi presenti; minimo complessivo −339.603, massimo 1.664.089 NT$ | Non trattarli automaticamente come errori o valori mancanti |
| `PAY_AMT1`–`PAY_AMT6` | Minimo complessivo 0, massimo 1.684.259 NT$ | Zero è un valore osservato; non sostituirlo automaticamente con un nullo |

L'assenza di nulli non risolve l'ambiguità dei codici. Le 35 ripetizioni senza ID non dimostrano che si tratti dello stesso cliente: documentare eventuali rimozioni invece di deduplicare automaticamente.

## Indicazioni per EDA e modellazione

1. Conservare il file originale e registrare separatamente ogni ricodifica, soprattutto delle categorie non documentate.
2. Trattare `SEX`, `EDUCATION` e `MARRIAGE` come categorie. Valutare esplicitamente come rappresentare gli stati di rimborso prima di assumere distanze numeriche fra i codici.
3. Esaminare distribuzioni, zeri e valori estremi degli importi prima di applicare trasformazioni. Una trasformazione logaritmica semplice non è definita per importi negativi.
4. Separare train, validation e test prima di apprendere imputazione, scaling, encoding o selezione delle variabili. Escludere ID e target dalle feature.
5. Valutare uno split stratificato sul target e controllare la presenza di profili identici tra le partizioni. Il file non offre una sequenza di coorti sufficiente a simulare da solo una validazione temporale su nuovi mesi.
6. Confrontare le metriche con il riferimento della classe maggioritaria: predire sempre 0 dà il 77,88% di accuracy sull'intero file. Considerare precision, recall, PR-AUC e ROC-AUC; se si stimano probabilità, valutarne anche la calibrazione.
7. Non interpretare associazioni come effetti causali. Il campione storico di Taiwan non dimostra prestazioni su popolazioni o periodi diversi; confrontare gli errori anche per gruppi demografici quando pertinente.

Queste sono indicazioni di lavoro, non decisioni di preprocessing già applicate.

### Riprodurre i controlli principali

Eseguire dalla root con l'ambiente del progetto:

```python
import pandas as pd

df = pd.read_excel(
    "data/default_of_credit_card_clients.xls",
    sheet_name="Data", header=1, engine="xlrd",
)
print(df.shape)
print(df.isna().sum().sum())
print(df["ID"].is_unique)
print(df.duplicated().sum())
print(df.drop(columns="ID").duplicated().sum())
print(df["default payment next month"].value_counts().sort_index())
for column in ["EDUCATION", "MARRIAGE", "PAY_0", "PAY_2", "PAY_3", "PAY_4", "PAY_5", "PAY_6"]:
    print(column, df[column].value_counts().sort_index())
```
