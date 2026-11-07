"""Train the selected pipeline, serialize it, and verify a pickle round trip."""

import hashlib
import json
import pickle
import platform
from importlib.metadata import version

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

from credit_default.model import (
    DECISION_THRESHOLD, RANDOM_STATE, TARGET, TEST_SIZE, build_final_pipeline,
)
from credit_default.paths import MODEL_FILE, MODEL_METADATA_FILE, RAW_DATA_FILE


def main():
    df = pd.read_excel(RAW_DATA_FILE, sheet_name="Data", header=1, engine="calamine")
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    # Reproduce the notebook's original, non-stratified holdout split.
    # Stratification was used inside CV; changing this split would change training.
    df_full_train, _ = train_test_split(
        df, test_size=TEST_SIZE, random_state=RANDOM_STATE,
    )
    X = df_full_train.drop(columns=["id", TARGET])
    y = df_full_train[TARGET]
    if X.shape != (24000, 23):
        raise ValueError(f"Unexpected training shape: {X.shape}")

    pipeline = build_final_pipeline()
    pipeline.fit(X, y)

    # Check serialization with development records, without evaluating holdout data.
    sample = X.head(10)
    expected = pipeline.predict_proba(sample)
    MODEL_FILE.parent.mkdir(parents=True, exist_ok=True)
    with MODEL_FILE.open("wb") as model_file:
        pickle.dump(pipeline, model_file, protocol=pickle.HIGHEST_PROTOCOL)
    with MODEL_FILE.open("rb") as model_file:
        loaded_pipeline = pickle.load(model_file)
    np.testing.assert_array_equal(expected, loaded_pipeline.predict_proba(sample))

    metadata = {
        "model_file": MODEL_FILE.name,
        "training_records": len(X),
        "feature_names": X.columns.tolist(),
        "target": TARGET,
        "decision_threshold": DECISION_THRESHOLD,
        "random_state": RANDOM_STATE,
        "test_size": TEST_SIZE,
        "dataset_sha256": hashlib.sha256(RAW_DATA_FILE.read_bytes()).hexdigest(),
        "training_index_sha256": hashlib.sha256(
            df_full_train.index.to_numpy(dtype="int64").tobytes()
        ).hexdigest(),
        "python_version": platform.python_version(),
        "dependencies": {
            name: version(name)
            for name in ["numpy", "pandas", "scikit-learn", "xgboost", "python-calamine"]
        },
        "model_parameters": pipeline.named_steps["model"].get_params(),
        "serialization_check_records": len(sample),
    }
    MODEL_METADATA_FILE.write_text(json.dumps(metadata, indent=2) + "\n")
    print(f"Trained on {len(X)} development records with {X.shape[1]} predictors.")
    print(f"Pipeline saved to {MODEL_FILE}")
    print(f"Metadata saved to {MODEL_METADATA_FILE}")
    print("Pickle round trip verified: identical probabilities on 10 development records.")
    print("No held-out test metrics were computed.")


if __name__ == "__main__":
    main()
