# Post-Quantum VPN / WireGuard Concept Evaluator

An educational, rules-based prototype for inspecting example telemetry associated with post-quantum VPN and WireGuard design discussions. It consists of two Python evaluation interfaces, a local REST API, and a standalone browser demonstration.

**Scope:** This repository does **not** establish VPN tunnels, implement Noise handshakes or ML-KEM, rotate cryptographic keys, test side-channel resistance, or demonstrate compliance with NIST standards. The thresholds (25 and 12 for the primary Python worker set) and status keywords are illustrative application rules, not standardized cryptographic limits.

## Browser demonstration

The static evaluator works offline after its assets load and requires no backend, login, or keys. It evaluates two numeric fields, a critical flag, and a descriptor against the same threshold/keyword rules used by the primary Python workers.

To run locally (ES modules require an HTTP origin):

```bash
python -m http.server 8080 --directory web
```

Open `http://127.0.0.1:8080/`. Review the results in the console or export a JSON report. There are no network requests from the app and no generated HMAC audit signatures.

## Python installation

Requirements: Python 3.10+, pip. Clone this repository, then run:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[api,dev]"
python -m pytest -q
node --test tests/test_web.mjs  # optional: Node.js 18+
```

The package provides two compatible command-line entry points:

- `post-quantum-vpn-wireguard-agent` — primary Pydantic-based supervisor (`cli.py`)
- `post-quantum-vpn-wireguard-engine` — separate dataclass-based concept engine (`pqc_wireguard/cli.py`)

Example commands:

```bash
post-quantum-vpn-wireguard-agent audit --task-id TASK-001 --target KEY-01 --primary 28.5 --secondary 14.2 --critical --status DISCORDANT
post-quantum-vpn-wireguard-agent chat "What is the configuration?"
post-quantum-vpn-wireguard-agent batch -i sample.csv -o results.csv
post-quantum-vpn-wireguard-agent verify-audit
python simulator.py --tasks 100
```

For batch CSVs, `is_critical_flag` accepts true/false, 1/0 and yes/no (case insensitive). Input and output must be different files. The JSON example is in `sample_payload.json`.

## Local API

```bash
post-quantum-vpn-wireguard-agent serve --host 127.0.0.1 --port 8000
```

Visit `http://127.0.0.1:8000/` for the static local evaluator when running from the repository source tree. API docs are at `http://127.0.0.1:8000/docs`.

| Endpoint | Description |
| --- | --- |
| `GET /health` | Service status |
| `GET /metrics` | JSON task and audit counters (not Prometheus format) |
| `POST /api/audit` | Evaluate a `SystemTaskPayload` |
| `POST /api/chat` | Deterministic mock response; no external LLM |
| `GET /api/audit/logs` | In-memory HMAC hash-chain metadata and verification result |

The Python audit trail signs chained metadata with HMAC-SHA256, and verification recomputes every signature. It is **in-memory only**, so entries are lost on process restart; setting `AUDIT_SECRET_KEY` does not make log storage persistent. The pattern-based identifier guard is not a complete privacy or de-identification solution.

The API has **no authentication** and must only be bound to a trusted loopback interface or placed behind an appropriately authenticated reverse proxy. Never expose it directly to the internet or submit real sensitive information.

## Docker

```bash
docker compose up --build
```

Compose binds host port 8000 to `127.0.0.1` only. A `.env` file is optional. To keep an HMAC key consistent for a process, copy `.env.example` to `.env` and set `AUDIT_SECRET_KEY` to a suitably random value. Do not commit secrets.

## Architecture and limitations

- `agents/`: primary Pydantic models, three deterministic evaluation workers, audit ledger, supervisor, and FastAPI integration
- `pqc_wireguard/`: alternate dataclass-based concept evaluator with its own CLI and API factory
- `enrichment.py`: demonstration threshold-based scoring for named verification/compliance concepts; not formal proofs or validated compliance tests
- `web/`: static HTML/CSS/JavaScript evaluator that does not depend on Python or WASM
- `tests/`: Python and browser-evaluator regression tests
- `.github/workflows/`: CI and static-site publishing workflow

The app is designed for modern browsers supporting JavaScript ES modules, including current Chromium, Firefox, and Safari. Mobile and keyboard layouts are supported; formal cross-browser E2E testing is not yet established.

## Privacy

The static browser app stores results in tab memory only and makes no network requests. JSON exports are generated locally. The Python server retains audit metadata and dossiers in memory; do not assume it is safe for sensitive data without further assessment.

## License

MIT — see [LICENSE](LICENSE).
