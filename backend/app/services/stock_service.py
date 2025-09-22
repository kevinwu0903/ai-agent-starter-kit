from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict, Tuple

import numpy as np
import pandas as pd
import yfinance as yf
from cachetools import TTLCache, cached

from app.config import get_settings

_settings = get_settings()

_CACHE = TTLCache(maxsize=32, ttl=300)


@dataclass
class StockData:
    symbol: str
    exchange_symbol: str
    company_name: str | None
    history: pd.DataFrame


class StockDataError(Exception):
    """Raised when upstream data cannot be retrieved."""


def _normalize_symbol(symbol: str) -> Tuple[str, str]:
    normalized = symbol.strip().upper()
    if not normalized.endswith(".TW"):
        normalized = f"{normalized}.TW"
    return normalized, normalized  # exchange symbol identical for TWSE on Yahoo


@cached(_CACHE)
def fetch_stock_history(symbol: str) -> StockData:
    """Fetch historical bars for a Taiwan stock symbol."""

    normalized, exchange_symbol = _normalize_symbol(symbol)
    history_window = _settings.history_window
    start_date = datetime.utcnow() - timedelta(days=history_window * 2)

    ticker = yf.Ticker(normalized)
    try:
        hist = ticker.history(start=start_date.strftime("%Y-%m-%d"), end=datetime.utcnow().strftime("%Y-%m-%d"), interval="1d")
    except Exception as exc:  # pragma: no cover - defensive
        raise StockDataError(f"Failed to download history for {symbol}: {exc}") from exc

    if hist.empty:
        raise StockDataError(f"No price data returned for symbol {symbol}")

    hist = hist.reset_index().rename(columns=str.lower)
    hist = hist.rename(columns={"index": "date", "adj close": "adj_close"})
    hist = hist.dropna(subset=["close"])

    company_info = ticker.info if hasattr(ticker, "info") else {}
    company_name = company_info.get("longName") or company_info.get("shortName")

    return StockData(
        symbol=symbol.upper(),
        exchange_symbol=exchange_symbol,
        company_name=company_name,
        history=hist,
    )


def compute_technical_indicators(history: pd.DataFrame) -> Dict[str, float | None]:
    df = history.copy().set_index("date")
    df.sort_index(inplace=True)

    indicators: Dict[str, float | None] = {
        "moving_average_5": df["close"].rolling(window=5).mean().iloc[-1],
        "moving_average_20": df["close"].rolling(window=20).mean().iloc[-1],
        "moving_average_60": df["close"].rolling(window=60).mean().iloc[-1],
    }

    # Relative Strength Index (RSI)
    delta = df["close"].diff()
    up = delta.clip(lower=0)
    down = -1 * delta.clip(upper=0)
    roll_up = up.rolling(14).mean()
    roll_down = down.rolling(14).mean()
    rs = roll_up / roll_down
    rsi = 100 - (100 / (1 + rs))
    indicators["rsi_14"] = float(rsi.iloc[-1]) if not np.isnan(rsi.iloc[-1]) else None

    # MACD
    ema12 = df["close"].ewm(span=12, adjust=False).mean()
    ema26 = df["close"].ewm(span=26, adjust=False).mean()
    macd = ema12 - ema26
    signal = macd.ewm(span=9, adjust=False).mean()
    indicators["macd"] = float(macd.iloc[-1]) if not np.isnan(macd.iloc[-1]) else None
    indicators["macd_signal"] = float(signal.iloc[-1]) if not np.isnan(signal.iloc[-1]) else None

    return indicators


def build_feature_matrix(history: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
    df = history.copy().set_index("date")
    df.sort_index(inplace=True)

    df["return"] = df["close"].pct_change()
    df["ma5"] = df["close"].rolling(window=5).mean()
    df["ma20"] = df["close"].rolling(window=20).mean()
    df["ma60"] = df["close"].rolling(window=60).mean()

    delta = df["close"].diff()
    up = delta.clip(lower=0)
    down = -1 * delta.clip(upper=0)
    roll_up = up.rolling(14).mean()
    roll_down = down.rolling(14).mean()
    rs = roll_up / roll_down
    df["rsi"] = 100 - (100 / (1 + rs))

    df["macd"] = df["close"].ewm(span=12, adjust=False).mean() - df["close"].ewm(span=26, adjust=False).mean()
    df["macd_signal"] = df["macd"].ewm(span=9, adjust=False).mean()

    df.dropna(inplace=True)
    if len(df) < 30:
        raise StockDataError("Insufficient data to build features")

    feature_cols = ["return", "ma5", "ma20", "ma60", "rsi", "macd", "macd_signal", "volume"]
    features = df[feature_cols]
    targets = (df["close"].shift(-1) > df["close"]).astype(int).iloc[:-1]
    features = features.iloc[:-1]

    return features, targets
