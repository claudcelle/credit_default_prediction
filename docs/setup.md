# Setup and reproducibility

Run commands from the repository root. The examples use Bash on Linux, macOS or
Windows with WSL. To call an already running service, skip this setup and use
[API usage](api.md#call-a-running-service).

## Install and clone

Install Git, curl and [uv](https://docs.astral.sh/uv/getting-started/installation/).
For notebook use, install VS Code with Microsoft's Python and Jupyter extensions.

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Reopen the terminal, then:

```bash
git clone https://github.com/claudcelle/credit_defaulf_prediction.git
cd credit_defaulf_prediction
uv sync --locked
```

uv creates `.venv` with Python 3.13 and the versions in `uv.lock`. The default
development group includes the notebook kernel and plotting tools. No manual
kernel installation or environment activation is required when using `uv run`.
For an activated shell, use `source .venv/bin/activate`.

For training and serving without notebook tools, use `uv sync --locked --no-dev`
and prefix commands with `uv run --locked --no-dev`. The Docker image uses this
smaller environment.

## GitHub Codespaces

Open the [repository](https://github.com/claudcelle/credit_defaulf_prediction) and
select **Code → Codespaces**. The repository is already cloned there. Install uv
if needed, reopen the terminal, and run `uv sync --locked`. Use the browser editor
or VS Code Desktop connected to the Codespace. Stop the Codespace when finished.

## Download and verify the dataset

Download the original UCI archive; no credentials are needed:

```bash
mkdir -p data
curl --fail --location 'https://archive.ics.uci.edu/static/public/350/default+of+credit+card+clients.zip' --output data/uci_default.zip
```

Extract and verify the original XLS bytes. An existing XLS is preserved and checked:

```bash
uv run --locked python - <<'PYTHON'
import hashlib
from pathlib import Path
from zipfile import ZipFile
import pandas as pd

path = Path("data/default_of_credit_card_clients.xls")
if not path.exists():
    with ZipFile("data/uci_default.zip") as archive:
        content = archive.read("default of credit card clients.xls")
    with path.open("xb") as output:
        output.write(content)
expected = "30c6be3abd8dcfd3e6096c828bad8c2f011238620f5369220bd60cfc82700933"
if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
    raise ValueError("Dataset checksum mismatch; verify the original UCI file.")
df = pd.read_excel(path, sheet_name="Data", header=1, engine="calamine")
assert df.shape == (30000, 25)
assert df["ID"].is_unique
assert set(df["default payment next month"].unique()) == {0, 1}
print("Dataset verified:", df.shape)
PYTHON
```

The 25 columns contain ID, 23 predictors and the target. Both notebooks and the
training script read this XLS directly using `python-calamine`. No CSV, Parquet
export or prior EDA execution is required. See the [data dictionary](data_documentation.md).

## Run the notebooks

1. Open the repository in VS Code with the Python and Jupyter extensions enabled.
2. Open a notebook and select the repository's `.venv/bin/python` as its kernel.
3. Restart the kernel, then run the cells in order.

- `notebooks/eda.ipynb` explores the original data and feature–target associations.
- `notebooks/training.ipynb` compares repayment encodings, tunes the three models,
  and evaluates the previously selected XGBoost configuration on the held-out test.

Each notebook runs independently from a clean kernel. Saved outputs are provided
for inspection. Running the training notebook repeats the existing searches and
final evaluation; it is unnecessary when you only want to train the selected
pipeline. Never change parameters or the threshold in response to test results.

## Train and serve

```bash
uv run --locked python train.py
uv run --locked uvicorn predict:app --host 127.0.0.1 --port 8000
```

Follow [training](training.md), [API](api.md) or [Docker](docker.md) for the next step.
In Codespaces, forward port 8000 (or Docker's host port 8001) to access `/docs`
from your local browser; use the forwarded address as the base URL.

## Troubleshooting

| Problem | Action |
| --- | --- |
| `uv` not found | Reopen the terminal and check the installer's PATH instructions |
| Lockfile mismatch | Use `pyproject.toml` and `uv.lock` from the same checkout |
| Missing XLS | Complete the download and extraction above |
| Checksum mismatch | Preserve a copy if needed, then obtain the original UCI XLS again |
| Missing `python_calamine` or notebook imports | Run `uv sync --locked` and select the project kernel |
| Kernel missing after `--no-dev` setup | Run `uv sync --locked` to include development dependencies |
| Model artifact missing at service startup | Run `uv run --locked python train.py` first |
| Connection refused | Start the server and check the URL, port and Codespaces forwarding |
