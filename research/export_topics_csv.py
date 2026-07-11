"""Export Paycrit topic JSON to CSV for manual Notion import fallback.

Usage:
  python research/export_topics_csv.py \
    --input research/data/paycrit_weekly_topics.sample.json \
    --output research/data/paycrit_weekly_topics.sample.csv
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Export Paycrit topics JSON to CSV")
    parser.add_argument("--input", required=True, help="Input JSON file")
    parser.add_argument("--output", required=True, help="Output CSV file")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    topics = json.loads(input_path.read_text(encoding="utf-8"))
    if not isinstance(topics, list):
        raise ValueError("Input JSON must be a list")

    fields = [
        "title",
        "category",
        "audience",
        "pain_point",
        "paycrit_angle",
        "linkedin_hook",
        "post_draft",
        "cta",
        "status",
        "research_date",
        "sources",
    ]

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for t in topics:
            row = dict(t)
            row["audience"] = "; ".join(row.get("audience", []) or [])
            row["sources"] = "\n".join(row.get("sources", []) or [])
            writer.writerow({k: row.get(k, "") for k in fields})

    print(f"CSV exported: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
