# Run without Docker

A client sends one customer's original features as JSON. FastAPI validates the
request with Pydantic and passes a one-row table through the fitted pipeline.
Uvicorn runs the HTTP server; the model is loaded once at startup.

## Start your own server

For the current distribution, complete the [common setup](../README.md#1-common-setup)
first: clone this repository (unless this Codespace already contains it), install
its environment, download the XLS and generate the model. To use the hosted
service instead, follow [On Fly.io](../README.md#4-on-flyio) without local setup.

This page contains the procedure without Docker. Run it in one machine or
Codespace. In terminal 1, from the repository root:

```bash
uv run --locked uvicorn predict:app --host 127.0.0.1 --port 8000
```

Keep this terminal running and use a second terminal in the same repository root
for requests. A missing artifact stops startup with
instructions to run training. Once trained, the server reads the model, not the
dataset; it does not train during startup.

## Call a running service

Start the server first using the section above. Run the following commands
from the repository root, where `examples/customer.json` exists. This procedure
uses `http://127.0.0.1:8000` for every request.

`127.0.0.1` reaches the machine or Codespace executing curl. To call a server in
another Codespace, use its reachable forwarded URL with the appropriate access
permissions. For the public cloud endpoint, follow
[On Fly.io](../README.md#4-on-flyio). A client calling someone else's running
server needs its URL and JSON; the bundled file and client commands below assume
that you obtained this repository.

```bash
curl --fail http://127.0.0.1:8000/health
curl --fail http://127.0.0.1:8000/predict \
  -H 'Content-Type: application/json' \
  --data-binary @examples/customer.json
```

The complete [example request](../examples/customer.json) is:

```json
{
  "limit_bal": 80000,
  "sex": 2,
  "education": 2,
  "marriage": 2,
  "age": 24,
  "pay_0": 0,
  "pay_2": 0,
  "pay_3": 0,
  "pay_4": 0,
  "pay_5": 0,
  "pay_6": 0,
  "bill_amt1": 75125,
  "bill_amt2": 77353,
  "bill_amt3": 78321,
  "bill_amt4": 73731,
  "bill_amt5": 39643,
  "bill_amt6": 39457,
  "pay_amt1": 3503,
  "pay_amt2": 5001,
  "pay_amt3": 2092,
  "pay_amt4": 1218,
  "pay_amt5": 1445,
  "pay_amt6": 878
}
```

This is the original feature vector of UCI record ID **21754**, the first record
in the development partition with seed 42 and test size 0.2. ID and target are
excluded. It is a bundled public-dataset example, not a fabricated customer.
See [dataset attribution](../README.md#dataset-attribution).

Successful responses use HTTP 200:

| Endpoint | Response |
| --- | --- |
| `GET /health` | `{"status": "ok"}` after model startup succeeds |
| `POST /predict` | `default_probability` (0–1), `default` (boolean), `threshold` (0.5) |

For the example, the selected model returns:

```json
{"default_probability": 0.10377471894025803, "default": false, "threshold": 0.5}
```

`default` is true when the probability is at least the fixed threshold. A score
does not establish probability calibration. `GET /docs` provides interactive
OpenAPI documentation; `GET /openapi.json` provides the machine-readable schema.

## Verify from a Python client

With `test.py` and `examples/customer.json` in their repository layout:

```bash
python test.py --url http://127.0.0.1:8000/predict
```

Only Python standard library is required. The client checks health, the response
contract and eight invalid inputs. Supply the complete `/predict` URL, including
any service path prefix. It derives the adjacent `/health` URL automatically.

If you also have the project environment and a fitted local model:

```bash
uv run --locked python test.py --url http://127.0.0.1:8000/predict --compare-local
```

This compares the HTTP probability with the local pipeline on the same bundled
example. It reads no dataset and computes no held-out metrics. Use a matching
model version on client and server for this optional consistency check.

## Stop the server

Press **Ctrl+C in terminal 1**. This stops the Python service.

## Validation and errors

All 23 fields are required integers, using normalized lowercase names and original
values. Do not pre-encode or scale them. Amounts are in NT$, not another currency;
see [field definitions](data_documentation.md).

Missing fields, strings (including numeric strings), booleans, fractional values,
nulls, and extra fields such as ID or target produce HTTP **422**, with a JSON
`detail` listing validation failures. The client checks each of these cases.

No arbitrary range limits are imposed. Signed balances and undocumented codes
remain accepted; education recoding and unseen-category handling stay inside the
pipeline. Malformed JSON also produces HTTP 422. A failed model load prevents
startup, so `/health` is available only after the application is ready.
