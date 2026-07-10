"""verify_and_clean.py - confirm correct dot coords + remove JS repositioner (no longer needed)."""
from pathlib import Path

CORRECT_DOT = 'cx="203" cy="30" r="6.5" fill="#00B4A2"'

OLD_JS_BLOCK = """\
<script>
document.fonts.ready.then(function(){
  document.querySelectorAll('.logo-text').forEach(function(t){
    var dot = t.closest('svg').querySelector('.logo-dot');
    var x   = parseFloat(t.getAttribute('x') || 16);
    var pre = t.getSubStringLength(0, 5);
    var iW  = t.getSubStringLength(5, 1);
    dot.setAttribute("cx", x + pre + iW / 2);
  });
});
</script>
"""

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

    has_dot = CORRECT_DOT in content
    has_js  = OLD_JS_BLOCK in content

    content = content.replace(OLD_JS_BLOCK, "")

    if content != orig:
        p.write_text(content, encoding="utf-8")

    dot_status = "OK" if has_dot else "MISSING - check!"
    js_status  = "removed" if has_js else "not present"
    print(f"{f}")
    print(f"  dot coords : {dot_status}")
    print(f"  JS script  : {js_status}")
    print()

print("Done.")
