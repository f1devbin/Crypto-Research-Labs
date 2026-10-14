"""Read cached data as pandas series. All dates are naive UTC calendar days.

A feature value dated D describes day D. Rules must lag features themselves
(see engine/rules.py) — the store never shifts anything.
"""
import json
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

from crl.config import DATA_DIR


def _utc_days(ms) -> pd.DatetimeIndex:
    t = np.asarray(ms, dtype="int64")
    t = np.where(t > 10**14, t // 1000, t)  # Binance switched some files to microseconds in 2025
    return pd.to_datetime(t, unit="ms").normalize()


class DataStore:
    """Single access point for every series a study may need."""

    def __init__(self, root: Path = DATA_DIR):
        self.root = Path(root)
        self._cache: dict = {}

    # ── prices ──────────────────────────────────────────────────────
    def daily(self, symbol: str) -> pd.DataFrame:
        """Daily OHLC (columns o, h, l, c) indexed by UTC date."""
        key = ("daily", symbol)
        if key not in self._cache:
            self._cache[key] = self._load_klines(symbol)
        return self._cache[key]

    def close(self, symbol: str) -> pd.Series:
        return self.daily(symbol)["c"]

    def _load_klines(self, symbol: str) -> pd.DataFrame:
        files = sorted((self.root / "klines" / "1d" / symbol).glob("*.zip"))
        chunks = []
        for f in files:
            try:
                with zipfile.ZipFile(f) as z, z.open(z.namelist()[0]) as fh:
                    df = pd.read_csv(fh, header=None, usecols=[0, 1, 2, 3, 4])
            except (zipfile.BadZipFile, IndexError, ValueError, pd.errors.EmptyDataError):
                continue
            df.columns = ["t", "o", "h", "l", "c"]
            df = df.apply(pd.to_numeric, errors="coerce").dropna()  # drops a header row if present
            chunks.append(df)
        if not chunks:
            raise FileNotFoundError(f"no daily klines for {symbol} under {self.root} — run `crl data refresh`")
        df = pd.concat(chunks, ignore_index=True)
        df.index = _utc_days(df.pop("t"))
        df = df[~df.index.duplicated(keep="last")].sort_index()
        df.index.name = "date"
        return df

    # ── external series ─────────────────────────────────────────────
    def feature(self, name: str) -> pd.Series:
        """Raw daily feature series by name (see FEATURES)."""
        key = ("feature", name)
        if key not in self._cache:
            if name not in FEATURES:
                raise KeyError(f"unknown feature '{name}', known: {sorted(FEATURES)}")
            self._cache[key] = FEATURES[name](self)
        return self._cache[key]

    def _json(self, *parts) -> object:
        return json.loads((self.root.joinpath(*parts)).read_text())

    def stablecoin_supply(self) -> pd.Series:
        total = None
        for name in ("stable_usdt", "stable_usdc"):
            rows = self._json("external", f"{name}.json")
            s = pd.Series([float(r["totalCirculating"]["peggedUSD"]) for r in rows],
                          index=pd.to_datetime([int(r["date"]) for r in rows], unit="s").normalize())
            s = s[~s.index.duplicated(keep="last")].sort_index()
            total = s if total is None else total.add(s, fill_value=0.0)
        return total.asfreq("D").ffill()

    def funding_daily(self, symbol: str = "BTCUSDT") -> pd.Series:
        """Mean funding rate per UTC day (one print per 8 h on Binance/OKX)."""
        base = self.root / "funding" / symbol
        parts = []
        for fz in sorted(base.glob("*.zip")):
            with zipfile.ZipFile(fz) as z, z.open(z.namelist()[0]) as fh:
                df = pd.read_csv(fh)
            parts.append(pd.DataFrame({"t": pd.to_numeric(df["calc_time"], errors="coerce"),
                                       "rate": pd.to_numeric(df["last_funding_rate"], errors="coerce")}))
        recent = base / "recent.json"
        if recent.exists():
            parts.append(pd.DataFrame(json.loads(recent.read_text())))
        if not parts:
            raise FileNotFoundError(f"no funding data for {symbol}")
        df = pd.concat(parts, ignore_index=True).dropna()
        df["t"] = (df["t"] // 1000).astype("int64") * 1000
        df = df.drop_duplicates("t").sort_values("t")
        df["d"] = _utc_days(df["t"])
        return df.groupby("d")["rate"].mean().asfreq("D")

    def fear_greed(self) -> pd.Series:
        rows = self._json("external", "fear_greed.json")["data"]
        s = pd.Series([float(r["value"]) for r in rows],
                      index=pd.to_datetime([int(r["timestamp"]) for r in rows], unit="s").normalize())
        s = s[~s.index.duplicated(keep="last")].sort_index()
        return s.asfreq("D").ffill(limit=3)

    def etf_flow(self) -> pd.Series:
        rows = self._json("external", "etf_flow_btc.json")
        s = pd.Series([float(r["etfFlow"]) for r in rows], index=pd.to_datetime([r["d"] for r in rows]))
        return s[~s.index.duplicated(keep="last")].sort_index()


def _exchange_flows(asset: str) -> pd.DataFrame:
    from crl.config import DATASETS_DIR
    df = pd.read_csv(DATASETS_DIR / "exchange_flows.csv", parse_dates=["date"])
    df = df[df["asset"] == asset].set_index("date").sort_index()
    return df[["inflow", "outflow"]].astype(float).asfreq("D")


def _netflow_7d(asset: str) -> pd.Series:
    """Coins moved TO exchanges minus coins moved OUT over 7 days (native units).
    Positive = net deposits (often read as coming sell pressure); negative = net withdrawals."""
    f = _exchange_flows(asset)
    return (f["inflow"] - f["outflow"]).rolling(7, min_periods=6).sum()


FEATURES = {
    # 7-day growth of USDT+USDC supply
    "stablecoin_growth_7d": lambda st: (lambda s: s / s.shift(7) - 1)(st.stablecoin_supply()),
    # 7-day mean BTC perpetual funding rate
    "funding_btc_7d": lambda st: st.funding_daily("BTCUSDT").rolling(7, min_periods=5).mean(),
    "fear_greed": lambda st: st.fear_greed(),
    # net spot-BTC-ETF flow over the last 5 US trading days
    "etf_flow_btc_5d": lambda st: st.etf_flow().rolling(5).sum().asfreq("D").ffill(limit=5),
    # 7-day net flow of BTC / ETH into exchanges (Coin Metrics, accumulated in datasets/)
    "exnetflow_btc_7d": lambda st: _netflow_7d("btc"),
    "exnetflow_eth_7d": lambda st: _netflow_7d("eth"),
}


class MemoryStore(DataStore):
    """In-memory store for tests and notebooks: pass ready-made series."""

    def __init__(self, closes: dict, features: dict | None = None):
        super().__init__(Path("/nonexistent"))
        self._closes = closes
        self._features = features or {}

    def daily(self, symbol: str) -> pd.DataFrame:
        c = self._closes[symbol]
        return pd.DataFrame({"o": c, "h": c, "l": c, "c": c})

    def feature(self, name: str) -> pd.Series:
        return self._features[name]
