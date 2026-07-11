# Paycrit - Payment Provider Intelligence

A static site that pulls live data from Airtable and renders a payment provider
comparison dashboard + matchmaking tool. Hosted free on GitHub Pages.

## How it works

```
Airtable (source of truth)
        |
   build.py  <-- runs daily via GitHub Actions
        |
docs/index.html  <-- GitHub Pages serves this
```

## Local development

1. Copy the env file and fill in your token:
   ```bash
   cp .env.example .env
   ```

2. Load the env and run the build:
   ```bash
   # Windows (PowerShell)
   $env:AIRTABLE_TOKEN="your_token_here"; python build.py

   # Mac / Linux
   export AIRTABLE_TOKEN="your_token_here" && python build.py
   ```

3. Open `docs/index.html` in your browser.

## GitHub Pages setup (one-time)

1. Push this repo to GitHub
2. Go to **Settings > Pages**
3. Set source to **Deploy from a branch**
4. Set branch: `main`, folder: `/docs`
5. Save — your site will be live at `https://<username>.github.io/<repo-name>`

## GitHub Secrets (one-time)

Go to **Settings > Secrets and variables > Actions > New repository secret**

Add these three secrets:

| Secret name           | Value                  |
|-----------------------|------------------------|
| `AIRTABLE_TOKEN`      | Your PAT token         |
| `AIRTABLE_BASE_ID`    | `appfXWwCG9UhEzGGG`    |
| `AIRTABLE_TABLE_ID`   | `tblEcMOTH3Zm5Muue`    |

The workflow will then auto-refresh the site daily and on every push to main.

## Notion weekly research pipeline

Set up and push weekly Paycrit research topics into Notion:

- Setup guide: `research/NOTION_SETUP.md`
- Push script: `research/notion_push_topics.py`
- CSV fallback: `research/export_topics_csv.py`
- Sample payload: `research/data/paycrit_weekly_topics.sample.json`

## Project structure

```
paycrit/
├── .github/workflows/refresh.yml   # Auto-rebuild daily
├── src/template.html               # HTML template with placeholders
├── docs/index.html                 # Generated output (GitHub Pages)
├── build.py                        # Airtable fetch + render script
├── .env.example                    # Local dev env template
├── .gitignore
└── README.md
```
