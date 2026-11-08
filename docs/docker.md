# Run with Docker

An image packages the runtime, dependencies, service code and fitted model.
A container is a running instance. Build the image from this repository after
training; no prebuilt registry image is supplied.

## Prepare and build

Complete the [common setup](../README.md#1-common-setup), including training,
first. This page contains the Docker procedure. Run it in one machine or
Codespace. A new Codespace needs its own prepared checkout and local image.

Install Docker and start its engine. In terminal 1, from the repository root,
confirm that all build inputs exist, then build:

```bash
ls Dockerfile pyproject.toml models/xgboost_pipeline.pkl models/xgboost_metadata.json
docker build -t credit-default:local .
```

The final `.` means the current directory. It must contain this project's
`Dockerfile`. Continue to the start command only after the build succeeds.
`credit-default:local` is the image tag created on this Docker engine; no image
with that name is published for automatic download.

The common training step creates `models/xgboost_pipeline.pkl` and its metadata.
Both are required at build time. The Dockerfile uses Python 3.13.18, uv 0.13.7, the locked non-dev
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
`127.0.0.1:8001` on the host. All client requests in this procedure use host
port **8001**. `EXPOSE` alone does not publish a host port. No volume mounts are required.

Open `http://127.0.0.1:8001/docs`. In Codespaces, forward port 8001 to your browser.

## Verify

In terminal 2 in the same machine or Codespace, change to the same repository
root and use host port **8001**:

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

## Stop and troubleshoot

Press **Ctrl+C in terminal 1**, or run in terminal 2:

```bash
docker stop credit-default-api
```

`--rm` removes the stopped container; the image remains for later runs.

| Problem | Action |
| --- | --- |
| `Dockerfile` not found | Clone this repository and change to its root before building |
| `pull access denied` for `credit-default` | Complete the local build successfully; this image is not published on a registry |
| Example JSON not found | Run curl from this repository's root, where `examples/customer.json` exists |
| Docker daemon unavailable | Start Docker and check access to its engine |
| Missing model during build | Run training before `docker build` |
| Model missing at startup | Rebuild with generated artifacts; do not mount an empty models directory |
| Port already allocated | Change the host port and use that port in the client URL |
| Client cannot connect | Start the container in the same Codespace and use port 8001; a different Codespace requires a reachable forwarded URL |

To use the already deployed cloud service, follow
[On Fly.io](../README.md#4-on-flyio). No public prebuilt Docker image is supplied
for local use.
