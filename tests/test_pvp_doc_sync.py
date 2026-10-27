"""Regression checks for the Oct 26 live-file documentation reconciliation."""
import importlib.util
import json
from pathlib import Path
import unittest
ROOT = Path(__file__).resolve().parents[1]

class PvpDocumentationChecks(unittest.TestCase):
    def test_current_guide_does_not_advertise_pvp(self):
        text = (ROOT / 'index.html').read_text()
        current = text.split('<section id="changelog"', 1)[0]
        self.assertIn('Player-vs-player fighting is off on this server.', current)
        self.assertNotIn('it works in PvP outside your party', current)
        self.assertNotIn('On this server it only works against other players', current)
        self.assertEqual(current.count('Player targets only (Limit Break PvE disabled), never mobs. PvP is off on this server, so this is a reference mechanic, not an available damage bonus.'), 8)
        self.assertNotIn('Player-vs-player fighting is on', current)
        self.assertEqual(current.count('This is a player-versus-player bonus, not a bonus against monsters.'), 8)
        self.assertIn('Historical entry, superseded October 26', text)
        self.assertIn('id="cl-pvp-live-doc-sync"', text)
    def test_assistant_corpus_matches_current_pages(self):
        spec = importlib.util.spec_from_file_location('ai_knowledge', ROOT/'scripts/build_ai_knowledge.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.assertEqual(json.loads((ROOT/'ai-knowledge.json').read_text()),
                         module.build((ROOT/'index.html').read_text(), (ROOT/'questions.html').read_text()))
