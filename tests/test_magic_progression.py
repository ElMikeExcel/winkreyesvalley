import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class MagicProgressionTests(unittest.TestCase):
    def test_player_explanation(self):
        html = (ROOT / "index.html").read_text()
        section = html.split('<h4 id="magic-progression">', 1)[1].split('<h4>Combat Attunement', 1)[0]
        for phrase in ("800 SP", "1,600 SP", "1,800 SP", "spends that step", "not a separate per-spell XP",
                       "not every wand upgrade", "Seals separately", "/spellbook", "Server Menu → Spell Book",
                       "proportionally over 60 seconds", "25% rate", "Central-time day",
                       "does not announce a fix"):
            self.assertIn(phrase, section)

    def test_faq_retrieval_is_self_contained(self):
        chunks = json.loads((ROOT / "ai-knowledge.json").read_text())
        faq = next(c for c in chunks if c["id"] == "magic-progression-qa")
        for phrase in ("shared Magic SP", "800 SP", "1,600 SP", "1,800 SP",
                       "/spellbook", "no independent ability-XP meter", "25%", "not announced as fixed"):
            self.assertIn(phrase, faq["text"])

    def test_corpus_matches_generator(self):
        spec = importlib.util.spec_from_file_location("knowledge_builder", ROOT / "scripts/build_ai_knowledge.py")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        self.assertEqual(json.loads((ROOT / "ai-knowledge.json").read_text()),
                         mod.build((ROOT / "index.html").read_text(), (ROOT / "questions.html").read_text()))
