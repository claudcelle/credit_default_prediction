# Keep Python and uv versions aligned with the training environment.
FROM python:3.13.18-slim
COPY --from=ghcr.io/astral-sh/uv:0.13.7 /uv /usr/local/bin/uv

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never \
    PATH="/app/.venv/bin:$PATH"

# XGBoost's Linux binary requires the OpenMP runtime.
RUN apt-get update \
    && apt-get install -y --no-install-recommends libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Install locked runtime/training dependencies; omit notebook development tools.
# The project is imported directly from /app rather than installed as a package.
COPY pyproject.toml uv.lock .python-version ./
RUN uv sync --locked --no-dev --no-install-project --no-cache

COPY predict.py ./
COPY credit_default/ ./credit_default/
COPY models/xgboost_pipeline.pkl ./models/xgboost_pipeline.pkl
COPY models/xgboost_metadata.json ./models/xgboost_metadata.json

# EXPOSE documents the container port; docker run -p publishes it on the host.
EXPOSE 8000
CMD ["uvicorn", "predict:app", "--host", "0.0.0.0", "--port", "8000"]
