"""png_logo.py - replace all logo markup with a simple <img> tag pointing to the PNG."""
from pathlib import Path
import re

# CSS we injected — strip it out
CSS_TO_REMOVE = (
    '  .paycrit-logo{'
    "font-family:'Poppins',sans-serif;"
    'font-weight:700;font-size:24px;color:#0B2D5E;'
    'text-decoration:none;line-height:1;letter-spacing:-0.5px;'
    'display:inline-flex;align-items:center;}\n'
    '  .pi-wrap{position:relative;display:inline-block;}\n'
    '  .pi-dot{'
    'position:absolute;width:5.5px;height:5.5px;'
    'background:#00B4A2;border-radius:50%;'
    'top:2px;left:50%;transform:translateX(-50%);}\n'
)

# Match the logo anchor regardless of what's inside it
LOGO_PATTERN = re.compile(
    r'<a[^>]*aria-label="Paycrit home"[^>]*>.*?</a>',
    re.DOTALL
)

FILES = {
    "src/landing.html":   "images/paycrit_logo.png",
    "src/template.html":  "images/paycrit_logo.png",
    "docs/index.html":    "images/paycrit_logo.png",
    "docs/dashboard.html":"images/paycrit_logo.png",
    "docs/services.html": "images/paycrit_logo.png",
    "docs/blog.html":     "images/paycrit_logo.png",
    "docs/privacy.html":  "images/paycrit_logo.png",
    "docs/terms.html":    "images/paycrit_logo.png",
    "docs/blog/why-payment-providers-freeze-accounts.html": "../images/paycrit_logo.png",
}

for f, img_path in FILES.items():
    # href back to home
    home = "../index.html" if f.startswith("docs/blog/") else "index.html"

    NEW_LOGO = (
        f'<a href="{home}" aria-label="Paycrit home" style="display:inline-flex;align-items:center;">'
        f'<img src="{img_path}" alt="Paycrit" height="36" style="display:block;"/>'
        f'</a>'
    )

    p = Path(f)
    content = p.read_text(encoding="utf-8")
    orig = content

    content = LOGO_PATTERN.sub(NEW_LOGO, content, count=1)
    content = content.replace(CSS_TO_REMOVE, "")

    if content != orig:
        p.write_text(content, encoding="utf-8")
        print(f"UPDATED : {f}")
    else:
        print(f"NO MATCH: {f}")

print("\nDone.")
