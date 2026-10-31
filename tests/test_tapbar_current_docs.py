from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]


class TapBarCurrentDocsTests(unittest.TestCase):
    def test_current_controls_do_not_promise_failed_gestures(self):
        html = (ROOT / "index.html").read_text()
        block = html.split('<div id="tap-bar-current">', 1)[1].split('</div>', 1)[0]
        for text in ("select an empty hotbar slot", "one wand slot", "at least one empty exit slot",
                     "no more than seven abilities", "does not have to be slot 8",
                     "My spell bar (change it)", "/spellbar", "/spellbook",
                     "not claimed fixed", "deferred until Seal 2", "normal Minecraft XP"):
            self.assertIn(text, block)

    def test_current_version_and_historical_label(self):
        html = (ROOT / "index.html").read_text()
        row = html.split("<tr><td>ExcelWandBars", 1)[1].split("</tr>", 1)[0]
        self.assertIn('<span class="pv">0.3.5</span>', row)
        self.assertIn("0.3.4-sp-display-candidate", row)
        self.assertIn("Historical WandBars versions", row)
        self.assertIn("not current control guarantees", row)

    def test_progression_and_ports_preserved(self):
        html = (ROOT / "index.html").read_text()
        self.assertIn('id="magic-progression"', html)
        self.assertIn('id="cl-magic-progression-explained"', html)
        faq = (ROOT / "questions.html").read_text()
        self.assertIn('id="magic-progression-qa"', faq)
        self.assertIn("20795", faq)
        self.assertIn("25622", faq)
