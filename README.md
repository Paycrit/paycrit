# Paycrit - Payment Provider Intelligence

A static site that pulls live data from Airtable and renders a payment provider
comparison dashboard + matchmaking tool. Hosted free on GitHub Pages.

## Brand lock (permanent)

- Logo format: `Pay` + `crit` wordmark (full word `Paycrit`)
- Logo font: **Manrope**
- Logo colors: `Pay = #0B2D5E`, `crit = #2563EB`
- Theme accents: blue scale (`#2563EB`, `#1D4ED8`, `#EFF6FF`, `#93C5FD`)
- Legacy teal/Poppins should not be reintroduced in production pages.

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
