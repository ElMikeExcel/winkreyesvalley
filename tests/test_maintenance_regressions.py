"""Preserve current instructions when regenerating cards; catch corrected tree errors."""
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('cards', ROOT/'scripts/build_guide.py')
cards = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cards)

class MaintenanceChecks(unittest.TestCase):
    def setUp(self):
        self.page = (ROOT/'index.html').read_text()
        self.data = json.loads((ROOT/'data/mcmmo-guide.json').read_text())

    def test_generation_changes_only_cards(self):
        before, rest = self.page.split(cards.START)
        _, after = rest.split(cards.END)
        self.data['skills'][0]['summary'] += ' TEST CHANGE'
        result = cards.render_page(self.page, self.data)
        self.assertNotEqual(result, self.page)
        self.assertEqual(result.split(cards.START)[0], before)
        self.assertEqual(result.split(cards.END)[1], after)
        for phrase in ['Friday, Saturday and Sunday', 'ExcelWeekendXP 1.2.0', 'PvP is off', '25622', '20795']:
            self.assertIn(phrase, result)

    def test_missing_or_duplicate_markers_fail_closed(self):
        for text in [self.page.replace(cards.START, ''), self.page + cards.START,
                     self.page.replace(cards.END, ''), self.page + cards.END]:
            with self.assertRaises(ValueError):
                cards.render_page(text, self.data)

    def test_generation_is_idempotent(self):
        result = cards.render_page(self.page, self.data)
        self.assertEqual(result, self.page)
        self.assertEqual(cards.render_page(result, self.data), result)

    def test_tree_matches_checked_formula_and_gates(self):
        tree = self.page.split('<span class="st-title">Maces</span>',1)[1]
        for value in ['+1.5 damage at level 100', 'reaching +4.5 before armor',
                      '+1.5 damage at rank 1', 'reaching +6 before armor',
                      '+2.5 damage at level 750 and +4 at level 1000',
                      'Level 50, during Berserk', 'not a bleed effect',
                      'not immunity or guaranteed net healing']:
            self.assertIn(value, tree)
        self.assertNotIn('> Flux Mining</summary>', tree)
        self.assertIn('ranks', self.page.lower())
        self.assertIn('improve the replanted growth stage, not the list of supported crops', self.page)

    def test_hard_is_permanent_not_an_open_trial(self):
        current = self.page.split('<section id="changelog">')[0]
        self.assertIn('owner made Hard permanent on October 25', current)
        self.assertNotIn('family gives its verdict on Monday', current)

    def test_waived_acceptance_is_not_passed(self):
        current = self.page.split('<section id="changelog">')[0]
        self.assertIn('were waived by the server owner on October 13, 2026; they are recorded as unverified, not passed', current)
        self.assertIn('live purchase with money movement', current)
        self.assertIn('have not been verified yet', current)
