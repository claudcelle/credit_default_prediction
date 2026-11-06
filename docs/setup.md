# Environment setup

This document records confirmed setup steps in GitHub Codespaces.

## Installing uv

`uv` will manage the virtual environment and Python dependencies. It was installed with:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

This downloads Astral's installation script and executes it with `sh`. The installer placed `uv` and `uvx` in `/home/codespace/.local/bin`.

Availability was verified with:

```bash
uv --version
```

Observed output:

```text
uv 0.13.7 (x86_64-unknown-linux-gnu)
```

This is the verified tool version, not a minimum requirement or a project version constraint. The installation command does not pin a specific uv version.

## Initializing the project

Git was already configured, with `origin` pointing to <https://github.com/claudcelle/credit_defaulf_prediction>.

The project was initialized with:

```bash
uv init --bare --vcs none
```

This created a minimal `pyproject.toml` without configuring another version control system, initially declaring `requires-python = ">=3.14"` and an empty dependency list. The system interpreter observed during setup was Python 3.14.2.

No `.venv`, `.python-version`, or `uv.lock` was present when initialization was checked.

## Python version

Python 3.13 was selected. Both [scikit-learn](https://pypi.org/project/scikit-learn/) and [XGBoost](https://pypi.org/project/xgboost/) declare support for this Python series.

- `.python-version` selects `3.13` for uv commands.
- `requires-python = ">=3.13,<3.14"` restricts the project to that minor series.

The patch version is not pinned. The virtual environment was created with CPython 3.13.18.

The environment was created and verified from the repository directory with:

```bash
uv venv
uv run python --version
```

The version check returned `Python 3.13.18`. `uv run` uses the project environment without manual activation.

## Dataset dependencies

`pandas` was added for tabular data analysis and `xlrd` for reading the original XLS file:

```bash
uv add pandas xlrd
uv run python -c "import pandas as pd; import xlrd; print('pandas:', pd.__version__); print('xlrd:', xlrd.__version__)"
```

Verified imports returned `pandas: 3.1.1` and `xlrd: 2.0.2`. The installation updated `pyproject.toml` and generated `uv.lock`, which records resolved dependency versions.

uv reported that hardlinks were unavailable and fell back to copying files. Installation completed successfully; no configuration change was needed.

## Recreating the environment

With uv installed and the repository checked out, install the locked dependencies with:

```bash
uv sync --locked
```

uv may download a suitable Python interpreter if needed. Add further dependencies only when required by the next project step.

## Reproducibility

Recording tool versions helps diagnose differences between environments. Reproduction also requires the Python version, dependencies in `pyproject.toml`, and the generated `uv.lock`.

Keep `pyproject.toml`, `.python-version`, and `uv.lock` in version control once created. The local `.venv` directory is already ignored.
