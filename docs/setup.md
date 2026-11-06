# Setup and execution

Choose one setup path, then follow the shared data download and verification steps. Run commands in Bash on Linux, macOS, Windows with WSL, or GitHub Codespaces. Each path ends in its project root; run subsequent commands there.

## Prerequisites

Install Git, curl, and [uv](https://docs.astral.sh/uv/getting-started/installation/). Internet access is required for Python, dependencies, and the dataset. To install uv on Linux, macOS, or WSL:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Reopen the terminal after installation.

## Path A: Clone the repository

```bash
git clone https://github.com/claudcelle/credit_defaulf_prediction.git
cd credit_defaulf_prediction
uv sync --locked
```

In Codespaces, open this repository and run `uv sync --locked` in its root directory; cloning again is unnecessary.

uv creates `.venv` using the committed `uv.lock`. Keep `pyproject.toml` and `uv.lock` from the same checkout. Do not reinitialize the project or add dependencies to reproduce it. To reproduce a specific revision, check out that commit before syncing.

Continue with [Download the dataset](#download-the-dataset).

## Path B: Start from an empty directory

This path creates an independent environment and loads the data. It does not recreate the repository's analysis notebook or shared Python modules.

```bash
mkdir credit-default-prediction
cd credit-default-prediction
git init
uv init --bare --vcs none --name credit-defaulf-prediction --python 3.13
uv python pin 3.13
```

Replace the generated `pyproject.toml` with the project's current dependency declarations:

```bash
cat > pyproject.toml <<'TOML'
[project]
name = "credit-defaulf-prediction"
version = "0.1.0"
requires-python = ">=3.13,<3.14"
dependencies = [
    "matplotlib>=3.11.2",
    "pandas>=3.1.1",
    "seaborn>=0.13.2",
    "xlrd>=2.0.2",
]
TOML
```

Create the working directories and ignore local environments and data:

```bash
mkdir -p data notebooks code docs
cat > .gitignore <<'IGNORE'
.venv/
__pycache__/
.ipynb_checkpoints/
.env
/data/
IGNORE
uv lock
uv sync --locked
```

Keep `pyproject.toml`, `uv.lock`, `.python-version`, and `.gitignore` in version control. Git does not track empty directories.

This path resolves dependencies available when `uv lock` runs and creates a new lockfile. It does not guarantee the same versions as the existing repository. Reuse this generated lockfile with `uv sync --locked` for subsequent installations; use Path A for the repository's locked versions.

## Python and dependency reproducibility

Both paths select Python 3.13 and require `>=3.13,<3.14`; the patch version is not pinned. uv can download a suitable interpreter when needed. `uv run --locked` executes commands in the project environment without manual activation.

The lockfile records resolved library versions. The operating system and Python patch can still differ between machines. See the [uv project guide](https://docs.astral.sh/uv/guides/projects/) for environment management.

## Download the dataset

The public UCI download requires no credentials:

```bash
mkdir -p data
curl --fail --location 'https://archive.ics.uci.edu/static/public/350/default+of+credit+card+clients.zip' --output data/uci_default.zip
```

Extract the original XLS bytes using the filename expected by the project. The ZIP member uses spaces; the local filename uses underscores. An existing destination is preserved:

```bash
uv run --locked python - <<'PYTHON'
from pathlib import Path
from zipfile import ZipFile

output = Path("data/default_of_credit_card_clients.xls")
if not output.exists():
    with ZipFile("data/uci_default.zip") as archive:
        content = archive.read("default of credit card clients.xls")
    with output.open("xb") as destination:
        destination.write(content)
PYTHON
```

Keep the original XLS unchanged. The archive and dataset are excluded from Git in both setup paths.

## Verify and load the data

Run this standalone example in either setup path. It verifies file integrity and loads the table using its descriptive header row:

```bash
uv run --locked python - <<'PYTHON'
import hashlib
from pathlib import Path
import pandas as pd

path = Path("data/default_of_credit_card_clients.xls")
expected_sha256 = "30c6be3abd8dcfd3e6096c828bad8c2f011238620f5369220bd60cfc82700933"
if hashlib.sha256(path.read_bytes()).hexdigest() != expected_sha256:
    raise ValueError("Dataset differs from the reference; verify the UCI download.")
df = pd.read_excel(path, sheet_name="Data", header=1, engine="xlrd")
assert df.shape == (30000, 25)
assert df["ID"].is_unique
assert set(df["default payment next month"].unique()) == {0, 1}

target = "default payment next month"
X = df.drop(columns=["ID", target])
y = df[target]
PYTHON
```

The command should finish without errors. `X` contains the 23 predictors and `y` the binary target; neither is saved to disk. Variable definitions and unresolved codes are in the [data dictionary](data_documentation.md).

## Run the repository notebook

For Path A, start Jupyter from the repository root:

```bash
uv run --locked --with jupyter jupyter lab
```

Open the URL displayed in the terminal and select `notebooks/eda.ipynb`. Use the Python kernel supplied by this Jupyter environment, then choose **Restart Kernel and Run All Cells**. In Codespaces, open Jupyter's port from the **Ports** tab.

The notebook supports execution from the repository root or `notebooks/`. It loads the data, normalizes column names, and produces quality checks, descriptive tables, and plots without requiring intermediate files or models.

Jupyter is supplied temporarily by `--with` and its version is not recorded in the project's lockfile. The project's declared dependencies remain locked. See the [official uv Jupyter guide](https://docs.astral.sh/uv/guides/integration/jupyter/).

## Troubleshooting

| Problem | Action |
| --- | --- |
| `uv: command not found` | Reopen the terminal and check the PATH reported by the installer |
| Lockfile mismatch | Use the configuration and lockfile from the same checkout; for a fresh project, finish generating its lockfile |
| XLS file not found | Complete extraction and check the underscore-separated filename in `data/` |
| Checksum mismatch | Check the download against UCI before proceeding; the extraction step preserves existing files |
| Missing notebook imports | Start Jupyter with the documented command and select its Python kernel |
| pandas warns about `xlrd` deprecation | Keep the declared reader for this setup; the warning does not by itself indicate a loading failure |
