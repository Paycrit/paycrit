# Paycrit Notion Setup (Weekly Research Pipeline)

## 1) Create Notion integration (personal account)
1. Open: https://www.notion.so/my-integrations
2. Click **New integration**
3. Name: `Paycrit Research Assistant`
4. Copy token (`secret_...`)

## 2) Create the Notion database
Create a database named: `Paycrit Content Research`

Add these properties exactly:

| Property | Type |
|---|---|
| Topic Title | Title |
| Category | Select |
| Audience | Multi-select |
| Merchant Pain Point | Rich text |
| Paycrit Angle | Rich text |
| LinkedIn Hook | Rich text |
| Post Draft | Rich text |
| CTA | Rich text |
| Status | Select |
| Research Date | Date |
| Sources | Rich text |

Then click **Share** and invite your integration (`Paycrit Research Assistant`).

## 3) Set env vars locally
PowerShell:

```powershell
$env:NOTION_TOKEN="secret_xxx"
$env:NOTION_DATABASE_ID="your_database_id"
```

## 4) Push topics to Notion

```powershell
python research/notion_push_topics.py --input research/data/paycrit_weekly_topics.sample.json
```

If successful, each topic will be inserted as a new row in your Notion DB.

## 5) CSV fallback (if Notion API blocked)

```powershell
python research/export_topics_csv.py --input research/data/paycrit_weekly_topics.sample.json --output research/data/paycrit_weekly_topics.sample.csv
```

Then import CSV into Notion manually.

---

## Weekly flow
1. Generate/update weekly topic JSON
2. Push via `notion_push_topics.py`
3. If blocked, export CSV and import manually
