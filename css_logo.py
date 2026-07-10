"""
css_logo.py - replace SVG logo with a pure HTML/CSS logo that is
font-timing-proof and renders identically on every page.
"""
from pathlib import Path

# ── what to find ──────────────────────────────────────────────────────────────
OLD_INNER = (
    'class="flex items-center" aria-label="Paycrit home">\n'
    '      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 260 90" height="38" aria-hidden="true">\n'
    '        <text class="logo-text" style="font-family:\'Poppins\',sans-serif;font-weight:700;font-size:60px;fill:#0B2D5E;" x="16" y="72">Paycrit</text>\n'
    '        <circle class="logo-dot" cx="203" cy="30" r="6.5" fill="#00B4A2"/>\n'
    '      </svg>\n'
    '    </a>'
)

# ── what to replace with ──────────────────────────────────────────────────────
NEW_INNER = (
    'class="paycrit-logo" aria-label="Paycrit home">'
    'Paycr<span class="pi-wrap"><span class="pi-i">&#305;</span>'
    '<span class="pi-dot"></span></span>t</a>'
)

# ── CSS to inject before </style> ─────────────────────────────────────────────
LOGO_CSS = (
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
    orig = content

    content = content.replace(OLD_INNER, NEW_INNER)

    # inject CSS only once
    if "pi-dot" not in orig and "pi-dot" in content:
        content = content.replace("</style>", LOGO_CSS + "</style>", 1)

    if content != orig:
        p.write_text(content, encoding="utf-8")
        print(f"UPDATED : {f}")
    else:
        print(f"NO MATCH: {f}")

print("\nDone.")
