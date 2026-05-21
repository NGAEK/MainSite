"""One-off: extract vision panel JS from git HEAD base.html into static/js/vision-panel.js."""
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
text = subprocess.check_output(
    ["git", "show", "HEAD:templates/base.html"],
    cwd=ROOT,
    encoding="utf-8",
)
idx = text.find("VISION ACCESSIBILITY PANEL")
if idx < 0:
    raise SystemExit("VISION ACCESSIBILITY PANEL not found in HEAD base.html")
start = text.rfind("/*", 0, idx)
end = text.find("</script>", start)
js = text[start:end].strip()
js = re.sub(
    r"/\*[\s\S]*?══════════════════════════════════════════════════════════ \*/\s*",
    "",
    js,
    count=1,
)
old = (
    "        statusBar.innerHTML =\n"
    "            '<span class=\"status-item\">' + label + '</span>' +\n"
    "            '<span class=\"status-item\">' + fontLabel + ': ' + fontSize + 'px</span>' +\n"
    "            '<span class=\"status-item\">' + contrastLabel + ': ' + contrast + '</span>';"
)
new = (
    "        statusBar.textContent = '';\n"
    "        [label, fontLabel + ': ' + fontSize + 'px', contrastLabel + ': ' + contrast].forEach(function (txt) {\n"
    "            var span = document.createElement('span');\n"
    "            span.className = 'status-item';\n"
    "            span.textContent = txt;\n"
    "            statusBar.appendChild(span);\n"
    "        });"
)
if old in js:
    js = js.replace(old, new)
out = ROOT / "static" / "js" / "vision-panel.js"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(js, encoding="utf-8")
print(f"wrote {out} ({len(js)} bytes)")
