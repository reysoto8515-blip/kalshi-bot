from __future__ import annotations

import argparse
from datetime import datetime, timezone
import time

from config import load_config
from engine.ev import MarketOpportunity, find_positive_ev
from engine.executor import TradingExecutor
from engine.risk import PositionContext, RiskManager
from kalshi.client import KalshiClient
from tracking.performance import PerformanceTracker, TradeRecord


def build_client(cfg):
    return KalshiClient(
        base_url=cfg.kalshi.base_url,
        environment=cfg.kalshi.environment,
        email=cfg.kalshi.email,
        password=cfg.kalshi.password,
        api_key=cfg.kalshi.api_key,
    )


def scan_once(cfg) -> list[MarketOpportunity]:
    opportunities: list[MarketOpportunity] = []
    for sport, enabled in cfg.sports.items():
        if not enabled:
            continue
        opportunities.append(
            MarketOpportunity(
                sport=sport,
                market_id=f"{sport}-sample-market",
                side="yes",
                model_probability=0.55,
                market_price_cents=50,
                confidence=0.6,
            )
        )
    return find_positive_ev(opportunities, cfg.risk.min_edge)


def cmd_scan(args) -> int:
    cfg = load_config(args.config)

    def run_and_print() -> None:
        opportunities = scan_once(cfg)
        if not opportunities:
            print("No +EV opportunities found.")
            return
        for opp in opportunities:
            print(f"{opp.sport}:{opp.market_id} side={opp.side} ev={opp.ev:.4f} confidence={opp.confidence:.2f}")

    if args.interval:
        print(f"Starting periodic scan every {args.interval} seconds. Ctrl+C to stop.")
        try:
            while True:
                run_and_print()
                time.sleep(args.interval)
        except KeyboardInterrupt:
            print("Stopped periodic scanner")
            return 0

    run_and_print()
    return 0


def cmd_trade(args) -> int:
    cfg = load_config(args.config)
    opportunities = scan_once(cfg)
    if not opportunities:
        print("No trade candidates found.")
        return 0

    client = build_client(cfg)
    risk = RiskManager(
        bankroll=cfg.risk.bankroll,
        fractional_kelly=cfg.risk.fractional_kelly,
        max_bankroll_per_trade=cfg.risk.max_bankroll_per_trade,
        daily_loss_limit=cfg.risk.daily_loss_limit,
        max_concurrent_positions=cfg.risk.max_concurrent_positions,
        max_exposure_per_sport=cfg.risk.max_exposure_per_sport,
    )
    executor = TradingExecutor(
        client,
        paper=cfg.trading.paper,
        retry_attempts=cfg.trading.retry_attempts,
        retry_delay_seconds=cfg.trading.retry_delay_seconds,
    )

    tracker = PerformanceTracker()
    opened = 0

    for opp in opportunities:
        ctx = PositionContext(open_positions=opened, sport_exposure=0.0, daily_pnl=0.0)
        if not risk.can_open_position(ctx):
            continue

        size = risk.position_size(opp.model_probability, opp.market_price_cents)
        contract_price = opp.market_price_cents / 100.0
        if size < contract_price:
            continue
        contracts = int(size // contract_price)
        if contracts <= 0:
            continue
        result = executor.execute([opp], contract_count=contracts)[0]
        opened += 1

        expected_pnl = contracts * opp.ev
        tracker.add_trade(
            TradeRecord(
                timestamp=datetime.now(timezone.utc).isoformat(),
                sport=opp.sport,
                market_id=opp.market_id,
                side=opp.side,
                contracts=contracts,
                price_cents=opp.market_price_cents,
                pnl=expected_pnl,
            )
        )
        print(f"{result.status}: {opp.market_id} {contracts} @ {opp.market_price_cents}c ({result.message})")

    tracker.export_csv("tracking/trade_history.csv")
    return 0


def cmd_backtest(args) -> int:
    cfg = load_config(args.config)
    opportunities = scan_once(cfg)
    avg_ev = sum(opp.ev for opp in opportunities) / len(opportunities) if opportunities else 0.0
    print(f"Backtest summary: opportunities={len(opportunities)}, avg_ev={avg_ev:.4f}")
    return 0


def cmd_status(args) -> int:
    cfg = load_config(args.config)
    client = build_client(cfg)
    balance = client.get_balance() if not cfg.trading.paper else cfg.risk.bankroll
    mode = "paper" if cfg.trading.paper else "live"
    print(f"Mode: {mode}")
    print(f"Balance: {balance:.2f}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Kalshi multi-sport trading bot")
    parser.add_argument("--config", default="config.yaml", help="Path to config file")

    sub = parser.add_subparsers(dest="command", required=True)

    scan = sub.add_parser("scan", help="Scan markets for +EV opportunities")
    scan.add_argument("--interval", type=int, default=0, help="Run scan every N seconds")
    scan.set_defaults(func=cmd_scan)

    trade = sub.add_parser("trade", help="Execute recommended trades")
    trade.set_defaults(func=cmd_trade)

    backtest = sub.add_parser("backtest", help="Run backtest summary")
    backtest.set_defaults(func=cmd_backtest)

    status = sub.add_parser("status", help="Show account and trading status")
    status.set_defaults(func=cmd_status)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
