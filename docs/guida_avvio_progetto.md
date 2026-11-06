# Iniziare il progetto da zero

Guida per chi deve avviare un progetto di machine learning tabellare, usando **Credit Card Default Prediction** come esempio concreto. I comandi sono pensati per il terminale Bash di GitHub Codespaces o per Linux/macOS. Su Windows usare WSL per seguire gli stessi comandi.

L'obiettivo iniziale è arrivare a un ambiente riproducibile, scaricare i dati originali e caricarli correttamente in un notebook. Training, API e Docker vengono dopo. Eseguire i comandi un blocco alla volta e controllare l'esito prima di continuare.

## 1. Definire il problema e scegliere i dati

Prima di installare librerie, scrivere nel README:

- Che cosa si vuole prevedere e a chi serve la previsione.
- Che cosa rappresenta una riga e qual è la variabile target.
- Quali informazioni saranno disponibili al momento della previsione.
- Da dove arrivano i dati, come scaricarli e quali condizioni di utilizzo hanno.

In questo progetto si vuole prevedere il default nel mese successivo per clienti di carte di credito. La fonte è [Default of Credit Card Clients, UCI](https://archive.ics.uci.edu/dataset/350/default+of+credit+card+clients). Il file contiene 30.000 osservazioni, 23 predittori, un ID e il target. UCI dichiara la licenza CC BY 4.0: conservare l'attribuzione alla fonte. Definizioni e verifiche locali sono in [Documentazione dei dati](data_documentation.md).

**Da personalizzare per il proprio dataset:** fonte, licenza, unità di osservazione, target, periodo osservato, formato dei file e dimensione del download. Se il download richiede un account o una chiave API, documentare il procedimento e mantenere le credenziali fuori da Git.

## 2. Preparare lo spazio di lavoro

Servono Git, un terminale, accesso a Internet e un editor. Con GitHub Codespaces il codice e i comandi vengono eseguiti nell'ambiente remoto; non occorre installare Python sul proprio computer per lavorare nel Codespace.

Scegliere **uno** dei due percorsi.

### Percorso A — Ripartire da questo repository

In GitHub aprire il repository e scegliere **Code → Codespaces → Create codespace**. In alternativa, da un terminale locale:

```bash
git clone https://github.com/claudcelle/credit_defaulf_prediction.git
cd credit_defaulf_prediction
```

Il clone crea una cartella con il nome del repository: mantenerne la grafia anche se contiene `defaulf`. Nel Codespace si è normalmente già nella cartella del progetto. Verificarlo con:

```bash
pwd
ls -a
git status
```

Devono essere visibili `README.md`, `pyproject.toml` e `uv.lock`. Proseguire con l'installazione di uv e poi con il punto 4A.

### Percorso B — Creare un repository nuovo

Creare su GitHub un repository per il proprio progetto e aprirlo in Codespaces, oppure creare una cartella locale:

```bash
mkdir credit-default-prediction
cd credit-default-prediction
git init
```

Questo inizializza soltanto il repository locale. Per pubblicarlo sarà necessario collegarlo al proprio repository GitHub. Proseguire con i punti 3 e 4B.

## 3. Installare e verificare uv

uv gestisce Python, l'ambiente virtuale e le dipendenze. Verificare prima se è disponibile:

```bash
uv --version
```

Solo se il comando non esiste, installarlo seguendo la [documentazione ufficiale di uv](https://docs.astral.sh/uv/getting-started/installation/). Su Linux/macOS:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Il comando scarica ed esegue lo script ufficiale di installazione. Riaprire il terminale e ripetere `uv --version`. Se uv resta non disponibile, controllare che la directory indicata dall'installer sia nel `PATH`.

## 4. Configurare Python e le dipendenze

Eseguire i comandi dalla cartella principale del progetto. L'ambiente virtuale `.venv` isola le librerie da quelle di altri progetti.

### 4A — Repository già esistente

```bash
uv sync --locked
uv run python --version
uv run python -c "import pandas as pd; import xlrd; print(pd.__version__); print(xlrd.__version__)"
```

Il repository seleziona Python 3.13 tramite `.python-version` e richiede `>=3.13,<3.14` in `pyproject.toml`. `uv sync --locked` ricrea l'ambiente usando il lockfile e segnala un errore se non è coerente con il progetto. Non eseguire nuovamente `uv init` e non sostituire il lockfile per aggirare un errore.

### 4B — Progetto nuovo

```bash
uv init --bare --vcs none
uv python install 3.13
uv python pin 3.13
```

`uv init` crea `pyproject.toml`; `--vcs none` evita di inizializzare nuovamente Git. Il pin crea `.python-version`. Aprire poi `pyproject.toml` e impostare il requisito Python, senza cancellare gli altri campi:

```toml
requires-python = ">=3.13,<3.14"
```

Per usare lo stesso dataset XLS del progetto:

```bash
uv add pandas xlrd
uv run python --version
uv run python -c "import pandas as pd; import xlrd; print(pd.__version__); print(xlrd.__version__)"
```

`uv add` aggiorna le dipendenze dichiarate, il lockfile e l'ambiente. Se si usa un altro formato, scegliere le librerie del punto 7. Python 3.13 è la scelta di questo progetto: per altri stack verificarne la compatibilità prima di adottarla.

### File da conoscere

| File o cartella | Funzione | Da versionare? |
| --- | --- | --- |
| `pyproject.toml` | Requisito Python e dipendenze dichiarate | Sì |
| `uv.lock` | Versioni risolte delle dipendenze | Sì |
| `.python-version` | Versione Python selezionata | Sì |
| `.venv/` | Interprete e librerie installate localmente | No |

Usare `uv run ...` per eseguire i comandi nell'ambiente del progetto, senza doverlo attivare manualmente. Dettagli nella [guida ufficiale ai progetti uv](https://docs.astral.sh/uv/guides/projects/).

## 5. Organizzare le cartelle — step consigliato

Una struttura iniziale semplice è sufficiente:

```text
progetto/
├── README.md
├── pyproject.toml
├── uv.lock
├── .python-version
├── .gitignore
├── data/               # dati originali, esclusi da Git
├── notebooks/          # esplorazione e analisi
├── code/               # codice Python riutilizzabile
├── docs/               # guida, fonti e dizionario dei dati
└── models/             # artefatti dei modelli, quando necessari
```

Nel repository attuale si usa `code/`; `code/paths.py` centralizza i percorsi. Evitare `import code` per importare il proprio codice, perché Python ha già un modulo standard con questo nome. Per un progetto nuovo si può scegliere un package dedicato, per esempio `src/credit_default/`, quando serve organizzare più moduli.

Per creare le cartelle iniziali mancanti:

```bash
mkdir -p data notebooks code docs
```

Creare `models/` quando si salva il primo modello. Git non registra directory vuote.

Per dataset con più fasi di elaborazione, valutare in seguito `data/raw/`, `data/interim/` e `data/processed/`. Se si adotta questa struttura, aggiornare tutti i percorsi nel codice: gli esempi di questa guida e il repository attuale usano direttamente `data/`.

Prima di aggiungere dati o credenziali, controllare `.gitignore`. In un progetto nuovo inserire almeno:

```gitignore
.venv/
__pycache__/
.ipynb_checkpoints/
.env
/data/
/models/
*.zip
```

Il repository esistente ha già regole per XLS e ZIP: verificare quelle presenti prima di aggiungerne altre. Queste regole non rimuovono file già tracciati. Versionare gli script di download e la documentazione della fonte permette di ricreare i dati senza caricarli nel repository.

## 6. Scaricare e controllare i dati

### Passaggi specifici per il dataset UCI di questo progetto

Il download pubblico non richiede credenziali. Dalla root, creare `data/`, poi scaricare l'archivio **solo se non è già presente**:

```bash
mkdir -p data
curl --fail --location 'https://archive.ics.uci.edu/static/public/350/default+of+credit+card+clients.zip' --output default+of+credit+card+clients.zip
```

Controllare il contenuto prima dell'estrazione:

```bash
uv run python -m zipfile -l default+of+credit+card+clients.zip
```

Deve comparire `default_of_credit_card_clients.xls`. Se il file non è già in `data/`, estrarre l'archivio:

```bash
uv run python -m zipfile -e default+of+credit+card+clients.zip data
ls -lh data/default_of_credit_card_clients.xls
```

Il modulo `zipfile` fa parte di Python: non serve installare una libreria per estrarre questo ZIP. Il comando di estrazione può sovrascrivere file omonimi: non ripeterlo su dati modificati. Conservare l'originale senza trasformazioni.

Per confrontare il file con quello già verificato nel progetto:

```bash
uv run python -c "from pathlib import Path; import hashlib; print(hashlib.sha256(Path('data/default_of_credit_card_clients.xls').read_bytes()).hexdigest())"
```

SHA-256 atteso per il file originale locale documentato:

```text
30c6be3abd8dcfd3e6096c828bad8c2f011238620f5369220bd60cfc82700933
```

Una differenza richiede di controllare origine e versione del file prima di confrontare i risultati. Il confronto identifica il contenuto; non sostituisce la verifica della fonte.

### Qui inserire i passaggi specifici per il proprio dataset

Se si sceglie un altro dataset, sostituire la procedura precedente con queste informazioni concrete:

1. Pagina ufficiale e URL di download, oppure procedura tramite account/API.
2. Nome dell'archivio e dei file attesi dopo l'estrazione.
3. Cartella di destinazione e spazio necessario.
4. Formato effettivo: CSV, XLS, XLSX, Parquet, JSON o altro.
5. Parametri di lettura: foglio, intestazione, separatore, encoding, tipi e valori mancanti.
6. Controllo di integrità e dimensioni attese, se disponibili dalla fonte.
7. Licenza, attribuzione, data del download e versione dei dati.

Non basta cambiare l'estensione del file: il lettore e i suoi parametri devono corrispondere al contenuto.

## 7. Installare le dipendenze in base al formato

Installare solo ciò che serve ai dati scelti. Per le opzioni Excel consultare [pandas.read_excel](https://pandas.pydata.org/docs/reference/api/pandas.read_excel.html).

| Formato | Installazione con uv | Lettura di esempio | Cosa verificare |
| --- | --- | --- | --- |
| CSV | `uv add pandas` | `pd.read_csv(path)` | Separatore, encoding, decimali, date, zeri iniziali negli ID |
| Excel `.xls` originale UCI | `uv add pandas xlrd` | `pd.read_excel(path, engine="xlrd", sheet_name="Data", header=1)` | Seconda riga come intestazione; nome del foglio |
| Excel `.xlsx` | `uv add pandas openpyxl` | `pd.read_excel(path, engine="openpyxl")` | Foglio e posizione dell'intestazione |
| Parquet | `uv add pandas pyarrow` | `pd.read_parquet(path, engine="pyarrow")` | Tipi delle colonne e file partizionati |
| JSON / JSON Lines | `uv add pandas` | `pd.read_json(path)` / `pd.read_json(path, lines=True)` | Struttura annidata e un record per riga |

`pd` indica `import pandas as pd`; `path` va sostituito con il percorso reale. Per CSV, ad esempio, `sep=";"`, `decimal=","` o `encoding="utf-8"` vanno scelti dopo aver ispezionato il file. Non sono impostazioni universali.

Nel progetto attuale `xlrd` è già dichiarato e la lettura funziona, ma il notebook segnala un avviso di deprecazione del lettore. La scelta è mantenuta qui per riprodurre l'ambiente esistente; un eventuale cambio di motore richiede di verificare nuovamente intestazioni, tipi e valori.

## 8. Eseguire il primo caricamento

Per questo dataset, dalla root del repository:

```bash
uv run python - <<'PY'
from pathlib import Path
import pandas as pd

path = Path("data/default_of_credit_card_clients.xls")
if not path.is_file():
    raise FileNotFoundError(f"Dataset non trovato: {path.resolve()}")

with pd.ExcelFile(path, engine="xlrd") as workbook:
    print("Fogli:", workbook.sheet_names)
    df = pd.read_excel(workbook, sheet_name="Data", header=1)

print("Dimensioni:", df.shape)
print("Colonne:", df.columns.tolist())
print(df.head())
print("Valori mancanti:", df.isna().sum().sum())
print(df["default payment next month"].value_counts().sort_index())

assert df.shape == (30000, 25)
assert df["ID"].is_unique
assert set(df["default payment next month"].unique()) == {0, 1}
PY
```

L'esito atteso sul file documentato è `(30000, 25)`, zero valori nulli per pandas e un target con 23.364 zeri e 6.636 uno. `header=1` serve perché i nomi descrittivi sono sulla seconda riga Excel; `header=0` leggerebbe l'intestazione sbagliata.

Il nome originale del target è `default payment next month`. Nel notebook del repository le colonne vengono normalizzate in minuscolo e con underscore: da quel punto il nome diventa `default_payment_next_month`. Usare il nome coerente con la fase del codice.

**Per altri dati:** riscrivere questo blocco con il proprio lettore e controlli motivati dalla fonte. Non riutilizzare le dimensioni e i conteggi UCI.

## 9. Preparare VS Code e il notebook

In VS Code servono le estensioni **Python** e **Jupyter**, installate nell'ambiente in cui gira il codice; con Codespaces, nel Codespace. Per il kernel Python:

```bash
uv add --dev ipykernel
```

Aprire `notebooks/eda.ipynb`, scegliere **Select Kernel → Python Environments** e selezionare il Python di `.venv`. Controllare in una cella:

```python
import sys
import pandas as pd
print(sys.executable)
print(pd.__version__)
```

L'interprete deve appartenere alla `.venv` del progetto. Se non compare, usare **Python: Select Interpreter**, selezionare `.venv/bin/python` e riaprire la selezione del kernel.

Per un progetto nuovo creare `notebooks/eda.ipynb`. All'inizio annotare obiettivo, fonte, percorso dei dati e scelte di lettura. Se si preferisce JupyterLab nel browser, aggiungerlo soltanto in quel caso:

```bash
uv add --dev jupyterlab
uv run jupyter lab
```

I percorsi relativi dipendono dalla directory di lavoro del kernel. Da `notebooks/`, il file è normalmente `../data/default_of_credit_card_clients.xls`; dalla root è `data/default_of_credit_card_clients.xls`. Il notebook esistente gestisce entrambi i casi tramite `code/paths.py`. Controllare `Path.cwd()` se compare `FileNotFoundError`.

## 10. Iniziare l'analisi e preparare le fasi successive

La prima analisi deve verificare tipi, categorie, valori mancanti, duplicati e distribuzione del target. Nel dataset UCI un intero può rappresentare una categoria; inoltre alcuni codici non sono definiti nella fonte e gli importi negativi non vanno cancellati automaticamente. Leggere [la documentazione dei dati](data_documentation.md) prima di ricodificare.

Dopo i controlli iniziali, definire train, validation e test prima di esplorare le relazioni con il target o apprendere trasformazioni. Stabilire come gestire profili ripetuti fra partizioni e mantenere il test per la valutazione finale. Encoding, scaling e imputazione devono essere appresi solo sul training.

Aggiungere le librerie al momento opportuno:

| Fase | Comando indicativo | Risultato da produrre |
| --- | --- | --- |
| Grafici EDA | `uv add matplotlib seaborn` | Distribuzioni e grafici commentati |
| Training | `uv add scikit-learn` | Baseline, split riproducibile e confronto su validation |
| XGBoost, se scelto | `uv add xgboost` | Confronto con le baseline |
| Salvataggio, se si usa joblib | `uv add joblib` | Pipeline di preprocessing e modello salvati insieme |
| API | `uv add fastapi 'uvicorn[standard]' pydantic` | Input validato e risposta di previsione |

Aggiungere `numpy` esplicitamente se il proprio codice lo importa direttamente. Non occorre installare tutto per caricare il dataset. I comandi della tabella sono preparazione delle fasi future: script di training, API e container devono ancora essere sviluppati.

Per il training, documentare seed, feature, preprocessing, iperparametri e metriche. Con classi sbilanciate non fermarsi all'accuracy: confrontare anche precision, recall, PR-AUC e ROC-AUC. Solo dopo una pipeline verificata passare alla serializzazione, al servizio API, ai test delle richieste e a Docker. Docker richiede un runtime separato dalle dipendenze Python. Verificare i criteri ufficiali del corso prima di decidere il deployment.

## 11. Documentare e rendere ripetibile l'avvio

Prima di considerare completato l'avvio, verificare:

- [ ] Il README descrive problema, fonte e modalità di download.
- [ ] Python e uv funzionano e gli import usano la `.venv` corretta.
- [ ] `pyproject.toml`, `uv.lock` e `.python-version` sono coerenti.
- [ ] Il file originale è nella cartella prevista ed escluso da Git.
- [ ] Il caricamento produce colonne, target e dimensioni attesi.
- [ ] Il notebook esegue le celle dall'inizio senza dipendere da variabili di sessioni precedenti.
- [ ] Sono documentate le particolarità del formato e le dipendenze necessarie.

Controllare i file prima di creare un commit:

```bash
git status --short
git diff
```

Aggiungere esplicitamente solo i file desiderati; evitare di includere dati, ambienti virtuali o credenziali. Una seconda persona deve poter clonare il repository, eseguire `uv sync --locked`, seguire il download documentato ed eseguire il primo caricamento.

## Problemi frequenti

| Problema | Controllo da fare |
| --- | --- |
| `uv: command not found` | Riaprire il terminale e controllare il PATH indicato dall'installer |
| `ModuleNotFoundError` nel notebook | Controllare `sys.executable`, kernel selezionato e dipendenze dichiarate |
| Manca `xlrd` o `openpyxl` | Installare il motore relativo al formato, usando `uv add` |
| `FileNotFoundError` | Controllare `pwd` o `Path.cwd()`, nome del file ed estrazione |
| Colonne `Unnamed` o nomi inattesi | Ispezionare le prime righe con `header=None` e scegliere l'intestazione corretta |
| Il CSV finisce in una sola colonna | Verificare il separatore reale prima di usare `sep` |
| `uv sync --locked` fallisce | Leggere l'errore: controllare coerenza del lockfile, Python e accesso alla rete |

## Riferimenti

- [Installazione di uv](https://docs.astral.sh/uv/getting-started/installation/).
- [Gestione dei progetti con uv](https://docs.astral.sh/uv/guides/projects/).
- [Lettura dei file Excel con pandas](https://pandas.pydata.org/docs/reference/api/pandas.read_excel.html).
- [Dataset ufficiale UCI](https://archive.ics.uci.edu/dataset/350/default+of+credit+card+clients).
- [Configurazione registrata nel repository](setup.md) e [dizionario dei dati](data_documentation.md).

Guida redatta il 6 novembre 2026. I comandi di installazione iniziale risolvono le versioni disponibili al momento dell'esecuzione; per riprodurre questo repository usare il suo `uv.lock`.
