"""Push weekly Paycrit research topics into a Notion database.

Usage (PowerShell):
  $env:NOTION_TOKEN="secret_xxx"
  $env:NOTION_DATABASE_ID="your_database_id"
  python research/notion_push_topics.py --input research/data/paycrit_weekly_topics.sample.json

Notes:
- Uses stdlib only (no third-party dependencies).
- Safe for personal Notion accounts.
- If Notion API is blocked by network policy, use CSV fallback script.
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from datetime import date
from pathlib import Path

NOTION_API_BASE = "https://api.notion.com/v1"
NOTION_VERSION = "2022-06-28"


def _require_env(name: str) -> str:
    import os

    value = os.environ.get(name, "").strip()
    if not value:
        raise ValueError(f"Missing env var: {name}")
    return value


def _read_topics(path: Path) -> list[dict]:
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")

    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("Input JSON must be an array of topic objects.")
    if not data:
        raise ValueError("Input JSON is empty.")
    return data


def _as_rich_text(value: str) -> list[dict]:
    value = (value or "").strip()
    if not value:
        return []
    return [{"type": "text", "text": {"content": value}}]


def _to_notion_properties(topic: dict) -> dict:
    """Maps topic keys -> Notion database properties.

    Expected keys in each topic object:
      title, category, audience(list), pain_point, paycrit_angle,
      linkedin_hook, post_draft, cta, status, research_date, sources(list)
    """
    title = topic.get("title", "Untitled Topic")
    category = topic.get("category", "General")
    audience = topic.get("audience", []) or []
    pain_point = topic.get("pain_point", "")
    paycrit_angle = topic.get("paycrit_angle", "")
    linkedin_hook = topic.get("linkedin_hook", "")
    post_draft = topic.get("post_draft", "")
    cta = topic.get("cta", "")
    status = topic.get("status", "Idea")
    research_date = topic.get("research_date", date.today().isoformat())
    sources = topic.get("sources", []) or []

    source_text = "\n".join(str(s).strip() for s in sources if str(s).strip())

    return {
        "Topic Title": {
            "title": [{"type": "text", "text": {"content": str(title)}}]
        },
        "Category": {"select": {"name": str(category)}},
        "Audience": {
            "multi_select": [{"name": str(item)} for item in audience if str(item).strip()]
        },
        "Merchant Pain Point": {"rich_text": _as_rich_text(str(pain_point))},
        "Paycrit Angle": {"rich_text": _as_rich_text(str(paycrit_angle))},
        "LinkedIn Hook": {"rich_text": _as_rich_text(str(linkedin_hook))},
        "Post Draft": {"rich_text": _as_rich_text(str(post_draft))},
        "CTA": {"rich_text": _as_rich_text(str(cta))},
        "Status": {"select": {"name": str(status)}},
        "Research Date": {"date": {"start": str(research_date)}},
        "Sources": {"rich_text": _as_rich_text(source_text)},
    }


def _create_page(token: str, database_id: str, properties: dict) -> dict:
    payload = {
        "parent": {"database_id": database_id},
        "properties": properties,
    }

    req = urllib.request.Request(
        url=f"{NOTION_API_BASE}/pages",
        data=json.dumps(payload).encode("utf-8"),
        method="POST",
        headers={
            "Authorization": f"Bearer {token}",
            "Notion-Version": NOTION_VERSION,
            "Content-Type": "application/json",
        },
    )

    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description="Push Paycrit weekly topics to Notion")
    parser.add_argument(
        "--input",
        default="research/data/paycrit_weekly_topics.sample.json",
        help="Path to topics JSON array",
    )
    args = parser.parse_args()

    try:
        token = _require_env("NOTION_TOKEN")
        database_id = _require_env("NOTION_DATABASE_ID")
        topics = _read_topics(Path(args.input))
    except Exception as exc:
        print(f"Setup error: {exc}")
        return 1

    created = 0
    for idx, topic in enumerate(topics, start=1):
        try:
            properties = _to_notion_properties(topic)
            result = _create_page(token=token, database_id=database_id, properties=properties)
            created += 1
            print(f"[{idx}/{len(topics)}] Created: {result.get('id', 'unknown-id')}")
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            print(f"[{idx}/{len(topics)}] HTTP {exc.code}: {body}")
        except Exception as exc:
            print(f"[{idx}/{len(topics)}] Error: {exc}")

    print(f"Done. Created {created}/{len(topics)} rows.")
    return 0 if created else 2


if __name__ == "__main__":
    sys.exit(main())
