"""fix_logo_text.py - render Paycrit as one unbroken text node for consistent sizing."""
from pathlib import Path

OLD_SVG = """\
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 260 90" height="38" aria-hidden="true">
        <text style="font-family:'Poppins',sans-serif;font-weight:700;font-size:60px;fill:#0B2D5E;" x="16" y="72"><tspan class="logo-prefix">Paycr</tspan><tspan class="logo-i">&#305;</tspan>t</text>
        <circle class="logo-dot" cx="188" cy="34" r="5" fill="#00B4A2"/>
      </svg>"""

NEW_SVG = """\
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 260 90" height="38" aria-hidden="true">
        <text class="logo-text" style="font-family:'Poppins',sans-serif;font-weight:700;font-size:60px;fill:#0B2D5E;" x="16" y="72">Paycrit</text>
        <circle class="logo-dot" cx="188" cy="34" r="5" fill="#00B4A2"/>
      </svg>"""

OLD_JS = """\
document.fonts.ready.then(function(){
  document.querySelectorAll('.logo-prefix').forEach(function(prefix){
    var dot = prefix.closest('svg').querySelector('.logo-dot');
    var x = parseFloat(prefix.closest('text').getAttribute('x') || 16);
    dot.setAttribute("cx", x + prefix.getComputedTextLength() + prefix.nextElementSibling.getComputedTextLength() / 2);
  });
});"""

NEW_JS = """\
document.fonts.ready.then(function(){
  document.querySelectorAll('.logo-text').forEach(function(t){
    var dot = t.closest('svg').querySelector('.logo-dot');
    var x   = parseFloat(t.getAttribute('x') || 16);
    var pre = t.getSubStringLength(0, 5);
    var iW  = t.getSubStringLength(5, 1);
    dot.setAttribute("cx", x + pre + iW / 2);
  });
});"""

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
    content = content.replace(OLD_SVG, NEW_SVG)
    content = content.replace(OLD_JS, NEW_JS)
    if content != orig:
        p.write_text(content, encoding="utf-8")
        print(f"UPDATED: {f}")
    else:
        print(f"NO CHANGE: {f}")

print("Done.")
