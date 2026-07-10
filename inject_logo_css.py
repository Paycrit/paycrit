"""inject_logo_css.py - add logo CSS to all pages that are missing it."""
from pathlib import Path

OLD = "  * { font-family: 'Inter', 'Segoe UI', system-ui, sans-serif; }"
NEW = (
    "  * { font-family: 'Inter', 'Segoe UI', system-ui, sans-serif; }\n"
    "  .paycrit-logo{font-size:22px;font-weight:800;letter-spacing:-0.5px;text-decoration:none;line-height:1;display:inline-flex;align-items:center;}\n"
    "  .pc-pay{color:#0B2D5E;}\n"
    "  .pc-crit{color:#00B4A2;}"
)

FILES = [
    "src/landing.html",
    "src/template.html",
    "docs/dashboard.html",
    "docs/services.html",
    "docs/blog.html",
    "docs/privacy.html",
    "docs/terms.html",
    "docs/blog/why-payment-providers-freeze-accounts.html",
]

for f in FILES:
    p = Path(f)
    content = p.read_text(encoding="utf-8")
    if ".pc-pay" not in content and OLD in content:
        p.write_text(content.replace(OLD, NEW, 1), encoding="utf-8")
        print(f"UPDATED : {f}")
    elif ".pc-pay" in content:
        print(f"ALREADY DONE: {f}")
    else:
        print(f"NO MATCH: {f}")

print("\nDone.")
