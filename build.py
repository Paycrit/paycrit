"""
build.py - Paycrit site generator
Fetches live data from Airtable, injects it into template.html,
writes the result to docs/index.html ready for GitHub Pages.
"""

import json
import os
import urllib.request
import urllib.parse
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

# ── CONFIG ────────────────────────────────────────────────────────────────────
BASE_ID  = os.environ.get("AIRTABLE_BASE_ID",  "appfXWwCG9UhEzGGG")
TABLE_ID = os.environ.get("AIRTABLE_TABLE_ID", "tblEcMOTH3Zm5Muue")
TOKEN    = os.environ.get("AIRTABLE_TOKEN", "")

LANDING_SRC  = Path("src/landing.html")
TEMPLATE     = Path("src/template.html")
OUTPUT_INDEX = Path("docs/index.html")       # landing page
OUTPUT_DASH  = Path("docs/dashboard.html")   # dashboard

# Walmart network proxy (used locally; GitHub Actions runs in the clear)
PROXY = os.environ.get("HTTPS_PROXY", "") or os.environ.get("HTTP_PROXY", "")


# ── AIRTABLE FETCH ────────────────────────────────────────────────────────────
def make_opener():
    handlers = []
    if PROXY:
        handlers.append(urllib.request.ProxyHandler({"http": PROXY, "https": PROXY}))
    else:
        handlers.append(urllib.request.ProxyHandler({}))  # bypass system proxy on CI
    return urllib.request.build_opener(*handlers)


def fetch_all_records():
    opener  = make_opener()
    headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}
    records = []
    offset  = None

    while True:
        params = {"pageSize": 100}
        if offset:
            params["offset"] = offset
        url = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_ID}?{urllib.parse.urlencode(params)}"
        req = urllib.request.Request(url, headers=headers)

        with opener.open(req, timeout=20) as resp:
            data = json.loads(resp.read().decode())

        records.extend(data.get("records", []))
        offset = data.get("offset")
        print(f"  Fetched {len(records)} records...", flush=True)
        if not offset:
            break

    return records


# ── DATA TRANSFORM ────────────────────────────────────────────────────────────
def safe(val, default=""):
    return val if val is not None else default


def transform(records):
    providers = []
    for rec in records:
        f = rec.get("fields", {})
        name = safe(f.get("Payment service provider", "")).strip()
        if not name:
            continue  # skip blank rows

        raw_score = f.get("Paycrit score")
        try:
            score = float(raw_score) if raw_score is not None else None
        except (ValueError, TypeError):
            score = None

        providers.append({
            "name":   name,
            "score":  score,
            "vol":    safe(f.get("Monthly gross revenue", "")),
            "btype":  safe(f.get("Business Type", "")),
            "target": safe(f.get("Target market", "")),
            "pros":   safe(f.get("Pros", "")),
            "cons":   safe(f.get("Cons", "")),
            "price":  safe(f.get("Pricing", "")),
            "logo":   safe(f.get("Press release - logo", "")),
            "web":    safe(f.get("Company Webpage", "")),
            "kyc":    safe(f.get("KYC", "")),
            "pp":     safe(f.get("Pricing page", "")),
        })

    # Sort by score descending, unscored last
    providers.sort(key=lambda p: p["score"] if p["score"] is not None else -1, reverse=True)
    return providers


# ── BUILD ─────────────────────────────────────────────────────────────────────
def build():
    if not TOKEN:
        raise EnvironmentError(
            "AIRTABLE_TOKEN is not set.\n"
            "Local: copy .env.example to .env and fill in your token.\n"
            "CI:    add AIRTABLE_TOKEN to your GitHub repository secrets."
        )

    print("Fetching Airtable data...", flush=True)
    records   = fetch_all_records()
    providers = transform(records)
    print(f"  {len(providers)} valid providers found.", flush=True)

    template   = TEMPLATE.read_text(encoding="utf-8")
    data_json  = json.dumps(providers, ensure_ascii=False, separators=(",", ":"))
    updated_at = datetime.now(timezone.utc).strftime("%d %b %Y")

    dashboard_html = (
        template
        .replace("__PAYCRIT_DATA__",    data_json)
        .replace("__PROVIDER_COUNT__",  str(len(providers)))
        .replace("__LAST_UPDATED__",    updated_at)
    )

    OUTPUT_INDEX.parent.mkdir(parents=True, exist_ok=True)

    # Write dashboard
    OUTPUT_DASH.write_text(dashboard_html, encoding="utf-8")
    print(f"  Dashboard written to {OUTPUT_DASH}", flush=True)

    # Copy landing page as-is (no placeholders needed)
    landing_html = LANDING_SRC.read_text(encoding="utf-8")
    OUTPUT_INDEX.write_text(landing_html, encoding="utf-8")
    print(f"  Landing page written to {OUTPUT_INDEX}", flush=True)

    print("Build complete.", flush=True)


if __name__ == "__main__":
    build()
