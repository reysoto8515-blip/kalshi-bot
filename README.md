# Kalshi Trading Bot

Python-based, modular Kalshi trading bot with multi-sport support for NBA, NFL, MLB, MMA, Esports, and Soccer.

## Features

- Kalshi API client (`kalshi/client.py`) with auth, market retrieval, orders, portfolio, and retry/rate-limit handling.
- Multi-sport data modules (`data/`) and shared cache.
- Sport-specific model scaffolding (`models/`) with training/backtest utilities.
- EV engine (`engine/ev.py`) for +EV opportunity filtering/ranking.
- Risk management (`engine/risk.py`) with fractional Kelly and exposure controls.
- Trading executor (`engine/executor.py`) with paper trading default.
- Performance tracking (`tracking/performance.py`) with summary metrics and CSV export.
- CLI entrypoint (`main.py`) with `scan`, `trade`, `backtest`, `status`.

## Quick Start

1. Create a virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Configure credentials:

- Copy `.env.example` to `.env` and set values.
- Edit `config.yaml` for sports/risk/model/trading settings.

3. Run commands:

```bash
python main.py scan
python main.py trade
python main.py backtest
python main.py status
```

## Architecture

- `kalshi/`: API client and order models
- `data/`: sport-specific data ingestion modules + cache layer
- `models/`: per-sport model classes and serialization helpers
- `engine/`: EV, risk, and execution logic
- `tracking/`: trade history, performance metrics, CSV export
- `config.py` + `config.yaml`: app settings and environment overrides

## Safety Defaults

- Paper trading is enabled by default (`trading.paper: true`).
- Risk limits are enabled by config.

## Disclaimer

This software is for educational/research purposes only and does not guarantee profitability. Trading and prediction markets involve significant risk. Ensure legal/regulatory compliance in your jurisdiction before use.
