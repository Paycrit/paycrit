"""Apply Paycrit brand theme (navy + blue, Manrope-ready tokens) to HTML pages."""
import re
from pathlib import Path

DOCS = Path(__file__).parent / "docs"

# ── shared CSS vars block to inject at top of every <style> ─────────────────
CSS_VARS = """\
  :root {
    --navy:       #0B2D5E;
    --navy-dark:  #091F42;
    --blue:       #2563EB;
    --blue-dark:  #1D4ED8;
    --blue-light: #EFF6FF;
    --blue-mid:   #93C5FD;
    --teal:       var(--blue);
    --teal-dark:  var(--blue-dark);
    --teal-light: var(--blue-light);
    --teal-mid:   var(--blue-mid);
  }
  h1 { letter-spacing: -1.5px; }
  h2 { letter-spacing: -0.75px; }
  h3 { letter-spacing: -0.5px; }
"""

# ── simple string swaps applied to every file ────────────────────────────────
SWAPS = [
    # nav CTA button
    ("bg-blue-600 text-white font-bold py-2 px-5 rounded-xl text-sm hover:bg-blue-700 transition-colors\">Find My Match",
     "text-white font-bold py-2 px-5 rounded-xl text-sm\" style=\"background:var(--navy)\">Find My Match"),
    # footer "P" icon
    ("w-6 h-6 bg-blue-600 rounded flex items-center justify-center",
     "footer-icon"),
    # hero gradient
    ("radial-gradient(ellipse 80% 60% at 50% -10%, #dbeafe 0%, #f8fafc 70%)",
     "radial-gradient(ellipse 80% 60% at 50% -10%, var(--teal-light) 0%, #f8fafc 70%)"),
    ("radial-gradient(ellipse 80% 60% at 50% -10%, #dbeafe 0%, #ffffff 70%)",
     "radial-gradient(ellipse 80% 60% at 50% -10%, var(--teal-light) 0%, #ffffff 70%)"),
    # badge pill (hero)
    ("bg-blue-50 text-blue-600 text-xs font-bold px-3 py-1 rounded-full border border-blue-100 uppercase tracking-wider",
     "text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider\" style=\"background:var(--teal-light);color:var(--teal-dark);border:1px solid var(--teal-mid);\""),
    # page label (blog/terms/privacy hero "Legal" etc)
    ("text-xs font-bold text-blue-600 uppercase tracking-widest",
     "text-xs font-bold uppercase tracking-widest\" style=\"color:var(--teal)\""),
    ("text-xs font-bold text-blue-600 uppercase tracking-wider",
     "text-xs font-bold uppercase tracking-wider\" style=\"color:var(--teal)\""),
    # active nav link
    ("class=\"text-blue-600 text-sm font-semibold\">Compare",
     "class=\"text-sm font-semibold\" style=\"color:var(--teal)\">Compare"),
    ("class=\"text-blue-600 text-sm font-semibold\">Services",
     "class=\"text-sm font-semibold\" style=\"color:var(--teal)\">Services"),
    # blog post card hover + tag pill
    ("box-shadow: 0 8px  rgba(37,99,235,0.08);\n    border-color: #bfdbfe;",
     "box-shadow: 0 8px 32px rgba(37,99,235,0.10);\n    border-color: var(--teal-mid);"),
    ("background: #eff6ff; color: #2563eb; font-size: 11px; font-weight: 700;\n    padding: 3px 10px; border-radius: 99px; border: 1px solid #bfdbfe;",
     "background: var(--teal-light); color: var(--teal-dark); font-size: 11px; font-weight: 700;\n    padding: 3px 10px; border-radius: 99px; border: 1px solid var(--teal-mid);"),
    # blog read article link + heading hover
    ("class=\"inline-block mt-4 text-blue-600 text-sm font-bold\">Read article",
     "class=\"inline-block mt-4 text-sm font-bold\" style=\"color:var(--teal)\">Read article"),
    ("group-hover:text-blue-600",
     "group-hover:text-slate-900"),
    # blog CTA block
    ("class=\"bg-blue-50 border border-blue-100 rounded-2xl p-8 text-center mt-10\"",
     "class=\"rounded-2xl p-8 text-center mt-10\" style=\"background:var(--teal-light);border:1px solid var(--teal-mid);\""),
    ("class=\"inline-flex items-center gap-2 bg-blue-600 text-white font-bold py-3 px-6 rounded-xl text-sm hover:bg-blue-700 transition-colors\">",
     "class=\"inline-flex items-center gap-2 text-white font-bold py-3 px-6 rounded-xl text-sm\" style=\"background:var(--navy)\">"),
    # prose links (terms / privacy)
    (".prose a { color: #2563eb;",
     ".prose a { color: var(--teal);"),
    (".prose a:hover { color: #1d4ed8;",
     ".prose a:hover { color: var(--teal-dark);"),
    # privacy highlight box
    ("class=\"highlight-box\"",
     "class=\"highlight-box\" style=\"background:var(--teal-light);border-color:var(--teal-mid);\""),
    (".highlight-box p { color: #0369a1;",
     ".highlight-box p { color: var(--teal-dark);"),
    (".highlight-box { background: #f0f9ff; border: 1px solid #bae6fd;",
     ".highlight-box { background: var(--teal-light); border: 1px solid var(--teal-mid);"),
    # services page
    ("check-blue",
     "check-teal"),
    (".check-blue  { background: #dbeafe; color: #2563eb; }",
     ".check-teal  { background: var(--teal-light); color: var(--teal-dark); }"),
    ("tier-card.featured {\n    border-color: #2563eb;\n    box-shadow: 0 0 0 4px rgba(37,99,235,0.08);",
     "tier-card.featured {\n    border-color: var(--teal);\n    box-shadow: 0 0 0 4px rgba(37,99,235,0.08);"),
    (".tier-card:hover { box-shadow: 0 8px 40px rgba(37,99,235,0.10); }",
     ".tier-card:hover { box-shadow: 0 8px 40px rgba(0,180,162,0.12); }"),
    (".benefit-card:hover { box-shadow: 0 4px 24px rgba(37,99,235,0.08); border-color: #bfdbfe; }",
     ".benefit-card:hover { box-shadow: 0 4px 24px rgba(37,99,235,0.10); border-color: var(--teal-mid); }"),
    (".form-input:focus { border-color: #2563eb; box-shadow: 0 0 0 3px rgba(37,99,235,0.10); }",
     ".form-input:focus { border-color: var(--teal); box-shadow: 0 0 0 3px rgba(37,99,235,0.12); }"),
    ("background: #2563eb; color: #fff; font-weight: 700;\n    padding: 14px 32px; border-radius: 12px; font-size: 15px;\n    transition: background 0.15s, transform 0.1s, box-shadow 0.15s;\n    display: inline-flex; align-items: center; gap: 8px; text-decoration: none;\n  }\n  .btn-primary:hover {\n    background: #1d4ed8;\n    box-shadow: 0 4px 20px rgba(37,99,235,0.3);",
     "background: var(--navy); color: #fff; font-weight: 700; letter-spacing:-0.2px;\n    padding: 14px 32px; border-radius: 12px; font-size: 15px;\n    transition: background 0.15s, transform 0.1s, box-shadow 0.15s;\n    display: inline-flex; align-items: center; gap: 8px; text-decoration: none;\n  }\n  .btn-primary:hover {\n    background: var(--navy-dark);\n    box-shadow: 0 4px 20px rgba(11,45,94,0.35);"),
    ("background: #eff6ff; color: #2563eb; font-size: 12px; font-weight: 700;\n    padding: 4px 12px; border-radius: 99px; border: 1px solid #bfdbfe;\n    letter-spacing: 0.04em; text-transform: uppercase;",
     "background: var(--teal-light); color: var(--teal-dark); font-size: 11px; font-weight: 800;\n    padding: 4px 12px; border-radius: 99px; border: 1px solid var(--teal-mid);\n    letter-spacing: 0.08em; text-transform: uppercase;"),
    ("bg-blue-600 text-white text-xs font-bold px-4 py-1 rounded-full tracking-wide\">MOST POPULAR",
     "text-white text-xs font-bold px-4 py-1 rounded-full tracking-wide\" style=\"background:var(--navy)\">MOST POPULAR"),
    ("class=\"bg-blue-50 border border-blue-100 rounded-xl p-4 mb-6 text-sm text-blue-800\"",
     "class=\"rounded-xl p-4 mb-6 text-sm\" style=\"background:var(--teal-light);border:1px solid var(--teal-mid);color:#0B4A44;\""),
    ("hover:border-blue-500 hover:text-blue-600 hover:bg-blue-50 transition-all text-sm\">",
     "transition-all text-sm\" onmouseover=\"this.style.borderColor='var(--teal)';this.style.color='var(--teal)';this.style.background='var(--teal-light)'\" onmouseout=\"this.style.borderColor='#e2e8f0';this.style.color='#334155';this.style.background=''\">"),
    ("class=\"underline hover:text-blue-600\">Terms",
     "class=\"underline\" style=\"color:var(--teal)\">Terms"),
    ("class=\"underline hover:text-blue-600\">Privacy",
     "class=\"underline\" style=\"color:var(--teal)\">Privacy"),
    # footer icon placeholder (added by earlier CSS swap that replaced the div)
]

CSS_FOOTER_ICON = """\
  .footer-icon { width:24px; height:24px; background:var(--navy); border-radius:6px; display:flex; align-items:center; justify-content:center; }"""


def inject_vars(content: str) -> str:
    """Insert CSS var block right after opening <style> tag."""
    if "--navy:" in content:
        return content  # already patched
    return content.replace("<style>", "<style>\n" + CSS_VARS, 1)


def inject_footer_icon_css(content: str) -> str:
    """Ensure .footer-icon class is defined in the style block."""
    if ".footer-icon" in content:
        return content
    return content.replace("</style>", CSS_FOOTER_ICON + "\n</style>", 1)


def apply_swaps(content: str) -> str:
    for old, new in SWAPS:
        content = content.replace(old, new)
    return content


def process(path: Path) -> None:
    original = path.read_text(encoding="utf-8")
    updated = inject_vars(original)
    updated = inject_footer_icon_css(updated)
    updated = apply_swaps(updated)
    if updated != original:
        path.write_text(updated, encoding="utf-8")
        print(f"   {path.name}")
    else:
        print(f"  ~ {path.name} (no changes)")


targets = [
    DOCS / "services.html",
    DOCS / "blog.html",
    DOCS / "terms.html",
    DOCS / "privacy.html",
]

print("Applying theme to docs/...")
for t in targets:
    process(t)
print("Done!")
