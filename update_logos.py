"""
update_logos.py - swaps the old P-box logo for the new SVG wordmark across all pages.
Run once, then delete.
"""
from pathlib import Path

OLD_FONT = "family=Inter:wght@400;500;600;700;800;900&display=swap"
NEW_FONT = "family=Inter:wght@400;500;600;700;800;900&family=Poppins:wght@700&display=swap"

# The inner part is identical across all remaining files — only the outer <a> href differs.
# We match the common inner block and also fix the wrapper class in one pass.
OLD_INNER = (
    'class="flex items-center gap-2.5 no-underline">\n'
    '      <div class="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">\n'
    '        <span class="text-white font-black text-sm">P</span>\n'
    '      </div>\n'
    '      <span class="font-black text-slate-900 text-lg tracking-tight">Paycrit</span>\n'
    '    </a>'
)

NEW_INNER = (
    'class="flex items-center" aria-label="Paycrit home">\n'
    '      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 260 90" height="38" aria-hidden="true">\n'
    "        <text style=\"font-family:'Poppins',sans-serif;font-weight:700;font-size:60px;fill:#0B2D5E;\" x=\"16\" y=\"72\">"
    '<tspan class="logo-prefix">Paycr</tspan><tspan class="logo-i">&#305;</tspan>t</text>\n'
    '        <circle class="logo-dot" cx="188" cy="34" r="5" fill="#00B4A2"/>\n'
    '      </svg>\n'
    '    </a>'
)

# src/landing.html already updated — skip it
OLD_LOGO = None
def new_logo(href): return None

JS_SNIPPET = (
    '<script>\n'
    'document.fonts.ready.then(function(){\n'
    "  document.querySelectorAll('.logo-prefix').forEach(function(prefix){\n"
    "    var dot = prefix.closest('svg').querySelector('.logo-dot');\n"
    "    var x = parseFloat(prefix.closest('text').getAttribute('x') || 16);\n"
    '    dot.setAttribute("cx", x + prefix.getComputedTextLength() + prefix.nextElementSibling.getComputedTextLength() / 2);\n'
    '  });\n'
    '});\n'
    '</script>'
)

FILES = {
    "src/template.html":  "index.html",
    "docs/services.html": "index.html",
    "docs/blog.html":     "index.html",
    "docs/privacy.html":  "index.html",
    "docs/terms.html":    "index.html",
    "docs/blog/why-payment-providers-freeze-accounts.html": "../index.html",
}

for rel_path, href in FILES.items():
    p = Path(rel_path)
    content = p.read_text(encoding="utf-8")
    original = content

    content = content.replace(OLD_FONT, NEW_FONT)
    content = content.replace(OLD_INNER, NEW_INNER)

    if "logo-prefix" in content and JS_SNIPPET not in content:
        content = content.replace("</body>", JS_SNIPPET + "\n</body>")

    if content != original:
        p.write_text(content, encoding="utf-8")
        print(f"  UPDATED: {rel_path}")
    else:
        print(f"  NO CHANGE: {rel_path}")

print("\nDone.")
