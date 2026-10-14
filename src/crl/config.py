"""Paths and global settings. Everything can be overridden with environment variables."""
import os
from pathlib import Path

ROOT = Path(os.environ.get("CRL_ROOT", Path(__file__).resolve().parents[2]))
DATA_DIR = Path(os.environ.get("CRL_DATA_DIR", ROOT / "data"))
HYPOTHESES_DIR = ROOT / "hypotheses"
RESULTS_DIR = ROOT / "results"
REPORTS_DIR = ROOT / "reports"
CONFIG_DIR = ROOT / "config"
STATE_DIR = Path(os.environ.get("CRL_STATE_DIR", DATA_DIR / "state"))

USER_AGENT = "crypto-research-labs/0.1 (+https://github.com/f1devbin/crypto-research-labs)"
