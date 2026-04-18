from __future__ import annotations

from dataclasses import dataclass
import time
from typing import Any, Dict, Optional

import requests


class KalshiAPIError(RuntimeError):
    pass


@dataclass
class TradeRequest:
    market_id: str
    side: str
    action: str
    count: int
    price_cents: int


class KalshiClient:
    def __init__(
        self,
        base_url: str,
        environment: str = "demo",
        email: str = "",
        password: str = "",
        api_key: str = "",
        timeout_seconds: int = 15,
        min_request_interval_seconds: float = 0.2,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.environment = environment
        self.email = email
        self.password = password
        self.api_key = api_key
        self.timeout_seconds = timeout_seconds
        self.min_request_interval_seconds = min_request_interval_seconds
        self._last_request_at = 0.0
        self._token: Optional[str] = None
        self.session = requests.Session()

    def authenticate(self) -> None:
        if self.api_key:
            self.session.headers.update({"Authorization": f"Bearer {self.api_key}"})
            return
        if not self.email or not self.password:
            raise KalshiAPIError("Missing credentials: provide API key or email/password")

        payload = {"email": self.email, "password": self.password}
        response = self._request("POST", "/trade-api/v2/login", json=payload, auth_required=False)
        token = response.get("token")
        if not token:
            raise KalshiAPIError("Authentication response did not contain token")
        self._token = token
        self.session.headers.update({"Authorization": f"Bearer {token}"})

    def _rate_limit(self) -> None:
        elapsed = time.time() - self._last_request_at
        if elapsed < self.min_request_interval_seconds:
            time.sleep(self.min_request_interval_seconds - elapsed)

    def _request(
        self,
        method: str,
        path: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        retries: int = 3,
        auth_required: bool = True,
    ) -> Dict[str, Any]:
        if auth_required and not (self.api_key or self._token):
            self.authenticate()

        url = f"{self.base_url}{path}"
        last_error: Optional[Exception] = None

        for attempt in range(1, retries + 1):
            self._rate_limit()
            try:
                resp = self.session.request(
                    method=method,
                    url=url,
                    params=params,
                    json=json,
                    timeout=self.timeout_seconds,
                )
                self._last_request_at = time.time()
                if resp.status_code >= 500 and attempt < retries:
                    time.sleep(0.5 * attempt)
                    continue
                resp.raise_for_status()
                if not resp.content:
                    return {}
                return resp.json()
            except requests.RequestException as exc:
                last_error = exc
                if attempt < retries:
                    time.sleep(0.5 * attempt)
                    continue
                break

        raise KalshiAPIError(f"Kalshi request failed: {last_error}")

    def fetch_markets(self, sport: str | None = None, category: str | None = None) -> list[dict]:
        params: Dict[str, str] = {}
        if sport:
            params["sport"] = sport
        if category:
            params["category"] = category
        response = self._request("GET", "/trade-api/v2/markets", params=params)
        return response.get("markets", [])

    def get_market_details(self, market_id: str) -> dict:
        return self._request("GET", f"/trade-api/v2/markets/{market_id}")

    def get_order_book(self, market_id: str) -> dict:
        return self._request("GET", f"/trade-api/v2/markets/{market_id}/orderbook")

    def get_pricing(self, market_id: str) -> dict:
        details = self.get_market_details(market_id)
        return {
            "yes_ask": details.get("yes_ask"),
            "yes_bid": details.get("yes_bid"),
            "no_ask": details.get("no_ask"),
            "no_bid": details.get("no_bid"),
        }

    def place_trade(self, order: TradeRequest) -> dict:
        payload = {
            "market_id": order.market_id,
            "side": order.side.lower(),
            "action": order.action.lower(),
            "count": order.count,
            "price": order.price_cents,
        }
        return self._request("POST", "/trade-api/v2/orders", json=payload)

    def get_positions(self) -> list[dict]:
        response = self._request("GET", "/trade-api/v2/portfolio/positions")
        return response.get("positions", [])

    def get_balance(self) -> float:
        response = self._request("GET", "/trade-api/v2/portfolio/balance")
        balance = response.get("balance", 0)
        try:
            return float(balance)
        except (TypeError, ValueError):
            return 0.0
