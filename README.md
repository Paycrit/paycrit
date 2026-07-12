# Paycrit - Payment Provider Intelligence

A static site that pulls live data from Airtable and renders a payment provider
comparison dashboard + matchmaking tool. Hosted free on GitHub Pages.


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
