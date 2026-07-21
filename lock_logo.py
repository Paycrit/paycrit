"""
lock_logo.py — applies the official Paycrit wordmark to all pages,
cleans up old SVG/PNG logo markup, and injects the logo CSS.
"""
from pathlib import Path
import re

LOGO_CSS = (
    "  .paycrit-logo{font-family:'Manrope','Segoe UI',system-ui,sans-serif;"
    "font-size:22px;font-weight:800;letter-spacing:-0.5px;"
    "text-decoration:none;line-height:1;display:inline-flex;align-items:center;}\n"
    "  .pc-pay{color:#0B2D5E;}\n"
    "  .pc-crit{color:#2563EB;}\n"
)

# Matches ANY anchor with aria-label="Paycrit home" and everything inside it
LOGO_RE = re.compile(
    r'<a\b[^>]*aria-label="Paycrit home"[^>]*>.*?</a>',
    re.DOTALL
)

FILES = {
    "src/landing.html":   "index.html",
    "src/template.html":  "index.html",
    "docs/index.html":    "index.html",
    "docs/dashboard.html":"index.html",
    "docs/services.html": "index.html",
    "docs/blog.html":     "index.html",
    "docs/privacy.html":  "index.html",
    "docs/terms.html":    "index.html",
    "docs/blog/why-payment-providers-freeze-accounts.html": "../index.html",
}

for f, home_href in FILES.items():
    p = Path(f)
    content = p.read_text(encoding="utf-8")
    orig = content

    new_anchor = (
        f'<a href="{home_href}" class="paycrit-logo" aria-label="Paycrit home">'
        '<span class="pc-pay">Pay</span><span class="pc-crit">crit</span></a>'
    )

    content = LOGO_RE.sub(new_anchor, content, count=1)

    # inject CSS once if not already there
    if ".pc-pay" not in orig and ".pc-pay" in content:
        content = content.replace("</style>", LOGO_CSS + "  </style>", 1)

    # strip leftover legacy Poppins import (no longer needed)
    content = content.replace(
        '&family=Poppins:wght@700&display=swap',
        '&display=swap'
    ).replace(
        '\n<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@700&display=block" rel="stylesheet"/>',
        ''
    )

    if content != orig:
        p.write_text(content, encoding="utf-8")
        print(f"UPDATED : {f}")
    else:
        print(f"NO MATCH: {f}")

print("\nDone.")
