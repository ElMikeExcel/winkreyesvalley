import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class MakersMarkFinderDocs(unittest.TestCase):
    def test_acquisition_not_historical_ownership(self):
        s = (ROOT / "index.html").read_text().split('id="makers-mark"', 1)[1].split('</div>', 1)[0]
        for text in ("first tracked", "older unsigned weapon", "does not reconstruct historical ownership",
                     "Opening a chest alone", "does not replace", "higher value of each counter, not their sum",
                     "both mobs and players", "not an amount of damage prevented"):
            self.assertIn(text, s)

    def test_settings_and_limits(self):
        s = (ROOT / "index.html").read_text().split('id="makers-mark"', 1)[1].split('</div>', 1)[0]
        for text in ("Settings → Maker's Mark", "/mark off", "/mark stats off",
                     "does not erase existing names", "Color milestones are not included",
                     "acceptance still needs checking", "Ambiguous transfers"):
            self.assertIn(text, s)

    def test_faq_in_generated_corpus(self):
        chunks = json.loads((ROOT / "ai-knowledge.json").read_text())
        faq = next(x for x in chunks if x["id"] == "makers-mark-qa")
        self.assertIn("Found by", faq["text"])
        self.assertIn("first tracked", faq["text"])
        self.assertIn("/mark stats off", faq["text"])
