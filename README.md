# Credit Card Default Prediction

Explore the **Default of Credit Card Clients** dataset to study credit card default in the following month. The analysis notebook, `notebooks/eda.ipynb`, provides data quality checks, descriptive statistics, and visualizations.

## Getting started

You need Git, curl, [uv](https://docs.astral.sh/uv/getting-started/installation/), an Internet connection, and Bash on Linux, macOS, Windows with WSL, or GitHub Codespaces.

Choose a setup path:

- [Clone the repository](docs/setup.md#path-a-clone-the-repository) to run the existing notebook with the committed dependency versions.
- [Start from scratch](docs/setup.md#path-b-start-from-an-empty-directory) to create an environment and load the dataset independently.

Both paths include dataset download and integrity checks in the [setup guide](docs/setup.md).

## Project structure

| Path | Purpose |
| --- | --- |
| `notebooks/eda.ipynb` | Exploratory analysis notebook |
| `code/paths.py` | Shared project paths |
| `data/` | Original dataset, excluded from Git |
| `docs/setup.md` | Environment setup, data download, and execution |
| `docs/data_documentation.md` | Data dictionary, category codes, and sources |
| `pyproject.toml`, `uv.lock`, `.python-version` | Dependencies and Python selection |

## Dataset and attribution

Source: [UCI Machine Learning Repository, dataset 350](https://archive.ics.uci.edu/dataset/350/default+of+credit+card+clients). See the [data dictionary](docs/data_documentation.md) for variable definitions and reading parameters.

Citation: Yeh, I. (2009). *Default of Credit Card Clients* [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C55S3H.

The dataset is licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
