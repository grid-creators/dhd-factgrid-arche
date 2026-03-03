#!/usr/bin/env python3
"""
fetch_data.py
=============
Fetches DHd conference data from the FactGrid SPARQL endpoint and saves results as CSV files.

Usage:
    python scripts/fetch_data.py [--output-dir data/] [--query-dir sparql/]

Requirements:
    pip install requests pandas
"""

import requests
import pandas as pd
import os
import argparse
import time
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
log = logging.getLogger(__name__)

ENDPOINT = "https://database.factgrid.de/sparql"
HEADERS = {
    "Accept": "application/sparql-results+json",
    "User-Agent": "DHd-ARCHE-SIP/1.0 (research data archiving; contact: tinghui.duan@example.com)",
}

QUERIES = {
    "conferences":        "sparql/01_conferences.rq",
    "publications":       "sparql/02_publications.rq",
    "authors":            "sparql/03_authors.rq",
    "affiliations":       "sparql/04_affiliations.rq",
    "gender_distribution":"sparql/05_gender_distribution.rq",
    "author_leaderboard": "sparql/06_author_leaderboard.rq",
}


def run_sparql(query: str, endpoint: str = ENDPOINT) -> list[dict]:
    """Execute a SPARQL SELECT query and return results as a list of dicts."""
    log.info(f"Running SPARQL query ({len(query)} chars)...")
    resp = requests.post(
        endpoint,
        data={"query": query},
        headers=HEADERS,
        timeout=120,
    )
    resp.raise_for_status()
    bindings = resp.json()["results"]["bindings"]
    log.info(f"  → {len(bindings)} results")
    return bindings


def bindings_to_df(bindings: list[dict]) -> pd.DataFrame:
    """Convert SPARQL JSON bindings to a flat pandas DataFrame."""
    rows = []
    for b in bindings:
        row = {k: v.get("value", "") for k, v in b.items()}
        rows.append(row)
    return pd.DataFrame(rows)


def load_query(path: str) -> str:
    """Load a SPARQL query from file, stripping comment lines."""
    with open(path, encoding="utf-8") as f:
        lines = [l for l in f if not l.strip().startswith("#")]
    return "".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Fetch DHd data from FactGrid")
    parser.add_argument("--output-dir", default="../data/", help="Directory for CSV output")
    parser.add_argument("--query-dir",  default="",       help="Prefix for query file paths")
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    for name, qpath in QUERIES.items():
        full_path = os.path.join(args.query_dir, qpath) if args.query_dir else qpath
        if not os.path.exists(full_path):
            log.warning(f"Query file not found: {full_path} — skipping")
            continue

        log.info(f"Processing query: {name}")
        query = load_query(full_path)

        try:
            bindings = run_sparql(query)
            df = bindings_to_df(bindings)
            out_path = os.path.join(args.output_dir, f"{name}.csv")
            df.to_csv(out_path, index=False, encoding="utf-8-sig")
            log.info(f"  → Saved {len(df)} rows to {out_path}")
        except Exception as e:
            log.error(f"  Failed to fetch {name}: {e}")

        time.sleep(1)  # polite delay between requests

    log.info("Done. All queries processed.")


if __name__ == "__main__":
    main()
