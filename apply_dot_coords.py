"""apply_dot_coords.py - lock in the correct dot coordinates across all pages."""
from pathlib import Path

OLD = 'cx="209.5" cy="33" r="6.5" fill="#00B4A2"'
NEW = 'cx="203" cy="30" r="6.5" fill="#00B4A2"'

FILES = [
    "src/landing.html",
    "src/template.html",
    "docs/services.html",
    "docs/blog.html",
    "docs/privacy.html",
    "docs/terms.html",
    "docs/index.html",
    "docs/dashboard.html",
    "docs/blog/why-payment-providers-freeze-accounts.html",
]

for f in FILES:
    p = Path(f)
    content = p.read_text(encoding="utf-8")
    if OLD in content:
        p.write_text(content.replace(OLD, NEW), encoding="utf-8")
        print(f"UPDATED: {f}")
    else:
        print(f"SKIPPED: {f}")

print("Done.")
