# Reproduce the selected model

`notebooks/training.ipynb` records model comparison and tuning. `train.py` trains
only the selected XGBoost configuration; it does not repeat searches or evaluate
the held-out test. It runs independently of the EDA notebook.

## Train

Complete [setup and original XLS download](setup.md), then from the repository root:

```bash
uv sync --locked
uv run --locked python train.py
```

The script reads the `Data` sheet with `header=1` and `engine="calamine"`, normalizes
names, and excludes ID and target. It reproduces the original non-stratified
80/20 split with seed 42 and fits only the 24,000 development records. Stratified
folds are used in the notebook's model selection, not to change this holdout.

The pipeline contains education recoding, One-Hot Encoding for sex, education and
marriage, unscaled numerical inputs including repayment status, and XGBoost.
The selected settings are 100 trees, depth 6, learning rate 0.05, minimum child
weight 5, row and column sampling 0.8, histogram tree method and seed 42.

## Generated artifacts

| File | Contents |
| --- | --- |
| `models/xgboost_pipeline.pkl` | Complete fitted preprocessing and classifier pipeline |
| `models/xgboost_metadata.json` | Feature names, selected settings, dependency versions, dataset and split fingerprints, threshold 0.5 |

Each training run replaces these generated files; Git excludes them. The script
verifies that saving and loading preserves probabilities on ten development
records. This is a serialization check, not another model evaluation.

## Load and predict

Use the matching locked environment from the repository root:

```python
import json
import pickle
from pathlib import Path
import pandas as pd
from credit_default.paths import MODEL_FILE

with MODEL_FILE.open("rb") as model_file:
    pipeline = pickle.load(model_file)
customer = json.loads(Path("examples/customer.json").read_text())
record = pd.DataFrame([customer], columns=pipeline.feature_names_in_)
positive_class = list(pipeline.classes_).index(1)
probability = float(pipeline.predict_proba(record)[0, positive_class])
print(probability)
```

`pickle` stores fitted Python objects. Load only trusted artifacts. The custom
function remains at `credit_default.model.group_education_codes`; this importable
module must be available when loading both existing and newly generated pickles.

For full model-selection reproduction, restart and run the training notebook
using the development environment. Do not retune the model or threshold from test
results. For inference, continue with [API](api.md) or [Docker](docker.md).
