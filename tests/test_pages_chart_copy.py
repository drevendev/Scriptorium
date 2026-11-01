"""Source-backed clipboard UX for the eight canonical Reader chart permalinks."""
from html.parser import HTMLParser
from pathlib import Path
import shutil
import subprocess
import unittest

ROOT=Path(__file__).resolve().parents[1]

class Controls(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.tags=[]
        self.feed(text)
    def handle_starttag(self, tag, attrs):
        self.tags.append((tag,dict(attrs)))

class ChartCopyTests(unittest.TestCase):
    def test_no_js_and_unverified_json_fail_closed(self):
        html=(ROOT/"index.html").read_text(encoding="utf-8")
        tags=Controls(html).tags
        buttons=[attrs for tag,attrs in tags if tag=="button" and attrs.get("id")=="copy-chart-link"]
        self.assertEqual(len(buttons),1)
        button=buttons[0]
        self.assertEqual(button.get("type"),"button")
        self.assertIn("hidden",button)
        self.assertIn("disabled",button)
        feedback=[attrs for tag,attrs in tags if attrs.get("id")=="copy-chart-feedback"]
        self.assertEqual(len(feedback),1)
        self.assertEqual(feedback[0].get("role"),"status")
        self.assertEqual(feedback[0].get("aria-live"),"polite")
        self.assertIn('id="share-chart" href="?metric=fantlab.dialogue.share_percent#charts"',html)
        css=(ROOT/"assets/pages-reader.css").read_text(encoding="utf-8")
        self.assertIn(".chart-share button[hidden] { display:none !important; }",css)
        self.assertIn(".chart-share button:focus-visible",css)
        self.assertIn("min-height:44px",css)
        js=(ROOT/"assets/pages-reader.js").read_text(encoding="utf-8")
        self.assertIn("verify(incoming); data=incoming;",js)
        self.assertIn("chartCopyButton.hidden=false;",js)
        self.assertIn("chartCopyButton.disabled=false;",js)
        self.assertIn('chartCopyButton.addEventListener("click",copyChartShareUrl);',js)
        self.assertIn('window.navigator?.clipboard?.writeText',js)
        self.assertIn('target.origin!==page.origin || target.pathname!==page.pathname',js)
        self.assertNotIn("innerHTML",js)

    @unittest.skipUnless(shutil.which("node"),"Node.js unavailable; structural checks still run")
    def test_actual_shipped_clipboard_helpers(self):
        for command in (
            ["node","--check",str(ROOT/"assets/pages-reader.js")],
            ["node",str(ROOT/"tests/pages_chart_copy_smoke.cjs")],
        ):
            result=subprocess.run(command,cwd=ROOT,text=True,capture_output=True,check=False)
            self.assertEqual(result.returncode,0,result.stdout+"\n"+result.stderr)

if __name__=="__main__":
    unittest.main()
