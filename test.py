"""Check a running API using a bundled development observation and stdlib HTTP."""

import argparse
import json
import math
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import urlsplit, urlunsplit
from urllib.request import Request, urlopen

EXAMPLE_FILE = Path(__file__).resolve().parent / "examples" / "customer.json"


def request_json(url, payload=None):
    request = Request(
        url,
        data=None if payload is None else json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", "Accept": "application/json"},
    )
    try:
        with urlopen(request, timeout=15) as response:
            return response.status, json.load(response)
    except HTTPError as error:
        return error.code, json.loads(error.read())


def compare_local(payload, probability):
    # Optional dependencies are imported only for the local consistency check.
    import pickle

    import pandas as pd

    from credit_default.paths import MODEL_FILE

    with MODEL_FILE.open("rb") as model_file:
        pipeline = pickle.load(model_file)
    record = pd.DataFrame([payload], columns=pipeline.feature_names_in_)
    expected = float(pipeline.predict_proba(record)[
        0, list(pipeline.classes_).index(1),
    ])

    assert math.isclose(probability, expected, rel_tol=0, abs_tol=1e-7), (
        probability, expected,
    )
    print("HTTP probability matches the local pipeline prediction.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", default="http://127.0.0.1:8000/predict",
                        help="Complete prediction endpoint URL")
    parser.add_argument("--compare-local", action="store_true",
                        help="Also compare with the local fitted model (requires project dependencies)")
    args = parser.parse_args()
    payload = json.loads(EXAMPLE_FILE.read_text())

    endpoint = urlsplit(args.url)
    health_url = urlunsplit(endpoint._replace(
        path=endpoint.path.rsplit("/", 1)[0] + "/health", query="", fragment="",
    ))
    status, health = request_json(health_url)
    assert status == 200 and health == {"status": "ok"}, (status, health)
    print("Health check passed.")

    status, result = request_json(args.url, payload)
    assert status == 200, (status, result)
    assert set(result) == {"default_probability", "default", "threshold"}
    probability = result["default_probability"]
    assert type(probability) in (int, float) and 0 <= probability <= 1, result
    assert type(result["default"]) is bool, result
    assert result["threshold"] == 0.5, result
    assert result["default"] == (probability >= result["threshold"]), result
    print("Prediction:", json.dumps(result))
    if args.compare_local:
        compare_local(payload, probability)

    # Mutations below are intentionally invalid test inputs, not observations.
    missing = payload.copy()
    missing.pop("age")
    invalid_inputs = {
        "missing feature": missing,
        "string instead of integer": {**payload, "age": "invalid"},
        "numeric string": {**payload, "age": "30"},
        "fractional value": {**payload, "age": 30.5},
        "boolean value": {**payload, "age": True},
        "null value": {**payload, "age": None},
        "extra ID field": {**payload, "id": 1},
        "extra target field": {**payload, "default_payment_next_month": 0},
    }
    for case, invalid_payload in invalid_inputs.items():
        status, error = request_json(args.url, invalid_payload)
        assert status == 422, (case, status, error)
        assert error.get("detail"), (case, error)
        print(f"Validation passed: {case} rejected with HTTP 422.")


if __name__ == "__main__":
    main()
