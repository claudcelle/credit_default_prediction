# Run with Docker

An image packages the runtime, dependencies, service code and fitted model.
A container is a running instance. Build the image from this repository after
training; no prebuilt registry image is supplied.

## Prepare and build

Install Docker and start its engine. Follow [setup](setup.md) to obtain the
repository, uv environment and original XLS, then:

```bash
uv run --locked python train.py
docker build -t credit-default:local .
```

Training creates `models/xgboost_pipeline.pkl` and its metadata. They are required
at build time. The Dockerfile uses Python 3.13.18, uv 0.13.7, the locked non-dev
dependencies and `libgomp1` required by XGBoost. The first build requires network
access for base images, OS packages and Python dependencies.

`.dockerignore` includes only the inference files. The image excludes notebooks,
the original dataset, the host `.venv`, examples and the training script. It
includes `credit_default` so pickle can import the education-recoding function.
No training occurs during container startup. Base tags and OS packages are not
pinned to immutable digests, so builds are not claimed to be bit-for-bit identical.

## Start

```bash
docker run --rm --name credit-default-api -p 127.0.0.1:8001:8000 credit-default:local
```

The service listens on `0.0.0.0:8000` inside the container and is published on
`127.0.0.1:8001` on the host. Port 8001 avoids a conflict with a local server on
8000. `EXPOSE` alone does not publish a host port. No volume mounts are required.

Open `http://127.0.0.1:8001/docs`. In Codespaces, forward port 8001 to your browser.

## Verify

From another terminal at the repository root:

```bash
curl --fail http://127.0.0.1:8001/health
curl --fail http://127.0.0.1:8001/predict \
  -H 'Content-Type: application/json' \
  --data-binary @examples/customer.json
python test.py --url http://127.0.0.1:8001/predict
```

The client requires only host Python, `test.py` and the example JSON; it needs no
dataset or ML packages. To additionally compare with the host's matching model:

```bash
uv run --locked python test.py --url http://127.0.0.1:8001/predict --compare-local
```

For a Docker-only host, create the artifacts in a compatible training environment
first and bring them into the build context. The inference container itself
requires no host Python installation.

## Stop and troubleshoot

Press Ctrl+C in the container terminal, or run:

```bash
docker stop credit-default-api
```

`--rm` removes the stopped container; the image remains for later runs.

| Problem | Action |
| --- | --- |
| Docker daemon unavailable | Start Docker and check access to its engine |
| Missing model during build | Run training before `docker build` |
| Model missing at startup | Rebuild with generated artifacts; do not mount an empty models directory |
| Port already allocated | Change the host port and use that port in the client URL |
| Client cannot connect | Check container logs, published port and whether the process is running |

Cloud deployment and registry publication are deferred.
