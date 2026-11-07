"""Serve the fitted credit-default pipeline through a small HTTP API."""

import pickle
from contextlib import asynccontextmanager

import pandas as pd
from fastapi import FastAPI, Request
from pydantic import BaseModel, ConfigDict, Field

from credit_default.model import DECISION_THRESHOLD
from credit_default.paths import MODEL_FILE


class CustomerFeatures(BaseModel):
    """Original, unencoded features accepted by the fitted pipeline."""

    # Reject coercion (e.g. strings or booleans as integers) and extra fields.
    # Preserve all integer codes and signed amounts without arbitrary bounds.
    model_config = ConfigDict(strict=True, extra="forbid")

    limit_bal: int
    sex: int
    education: int
    marriage: int
    age: int
    pay_0: int
    pay_2: int
    pay_3: int
    pay_4: int
    pay_5: int
    pay_6: int
    bill_amt1: int
    bill_amt2: int
    bill_amt3: int
    bill_amt4: int
    bill_amt5: int
    bill_amt6: int
    pay_amt1: int
    pay_amt2: int
    pay_amt3: int
    pay_amt4: int
    pay_amt5: int
    pay_amt6: int


class Prediction(BaseModel):
    default_probability: float = Field(ge=0, le=1)
    default: bool
    threshold: float


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load once at startup. A missing/incompatible artifact stops startup
    # rather than leaving a running service that cannot make predictions.
    try:
        with MODEL_FILE.open("rb") as model_file:
            app.state.pipeline = pickle.load(model_file)
    except FileNotFoundError as error:
        raise RuntimeError(
            "Model artifact missing. Run `uv run --locked python train.py` "
            "before starting the service or building the Docker image."
        ) from error
    app.state.positive_class_index = list(app.state.pipeline.classes_).index(1)
    yield


app = FastAPI(title="Credit Card Default Prediction", lifespan=lifespan)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/predict", response_model=Prediction)
def predict(customer: CustomerFeatures, request: Request) -> Prediction:
    # Convert one JSON record into a one-row DataFrame with training columns.
    # The stored pipeline handles every preprocessing step internally.
    pipeline = request.app.state.pipeline
    record = pd.DataFrame(
        [customer.model_dump()], columns=pipeline.feature_names_in_,
    )
    probability = float(pipeline.predict_proba(record)[
        0, request.app.state.positive_class_index,
    ])
    return Prediction(
        default_probability=probability,
        default=probability >= DECISION_THRESHOLD,
        threshold=DECISION_THRESHOLD,
    )
