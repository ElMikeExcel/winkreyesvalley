"""Regression checks for the installed two-tier Death Protection instructions."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class DeathProtectionChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = (ROOT / 'index.html').read_text()
        cls.guide = cls.text.split('id="death-protection"', 1)[1].split('</div>', 1)[0]
        cls.current = cls.text.split('<section id="changelog">', 1)[0]
        cls.history = cls.text.split('<section id="changelog">', 1)[1]

    def test_installed_version_has_explicit_acceptance_limits(self):
        for phrase in ['ExcelDeathProtection 0.1.2 is installed, October 13, 2026.',
                       'Java and Bedrock-phone screens, real purchases and gameplay checks are still pending for 0.1.2.',
                       'Successful startup is not a gameplay pass.']:
            self.assertIn(phrase, self.guide)
        self.assertNotIn('Bedrock phone test passed', self.current)
        self.assertNotIn('ExcelDeathProtection 0.1.1 is installed', self.current)
        self.assertIn('<td>ExcelDeathProtection<small class="plugin-next">Created by us</small></td><td>0.1.2</td>', self.current)

    def test_basic_is_immediate_without_item_or_powers(self):
        for phrase in ['Death Protection — $15,000',
                       'protection starts immediately after you confirm the purchase',
                       'You receive no item and have no potion to drink',
                       'no extra powers or potion effects', 'Inventory protected: 1 death']:
            self.assertIn(phrase, self.guide)
        self.assertIn('<tr><td>Death Protection (activates immediately)</td><td>$15,000</td></tr>', self.current)

    def test_premium_is_drink_later_with_explained_benefits(self):
        for phrase in ['+Death Protection Potion — $30,000', 'buy a potion to store and drink later',
                       'Buying it does not activate protection; drink it first.',
                       'underwater breathing, clearer underwater vision, and faster mining',
                       'The mining boost also works on land.', 'blue shell icon can come from other sources']:
            self.assertIn(phrase, self.guide)
        self.assertIn('<tr><td>1 +Death Protection Potion (drink later)</td><td>$30,000</td></tr>', self.current)
        self.assertNotIn('<tr><td>1 Death Protection Potion</td><td>$15,000</td></tr>', self.current)

    def test_quote_requires_same_option_and_price_confirmation(self):
        for phrase in ['first click or tap', "quoted price and charges nothing",
                       'the same option again within 20 seconds', 'confirm and buy at that quoted price',
                       'a changed price needs a fresh confirmation', 'These prices are in-game money.']:
            self.assertIn(phrase, self.guide)
        self.assertIn('use their own two-click price confirmation', self.current)

    def test_shared_limits_and_legacy_entitlements(self):
        for phrase in ['keep your inventory once', "Neither option saves your XP; the server's normal XP rules still apply.",
                       'That death uses up your protection', 'ordinary server restarts',
                       'Only one active protection at a time', 'blocked before you are charged',
                       'you keep the potion', 'An undrunk potion in your inventory is not active protection',
                       'Existing active protection and old Death Protection Potions stay premium, with no extra payment.',
                       '/dp status', 'ExcelDeathProtection/PLAYER-GUIDE.md']:
            self.assertIn(phrase, self.guide)

    def test_new_entry_precedes_preserved_historical_versions(self):
        installed = self.history.index('Installed <b>ExcelDeathProtection 0.1.2</b>')
        previous = self.history.index('Updated <b>ExcelDeathProtection to 0.1.1</b>')
        first = self.history.index('Installed <b>ExcelDeathProtection 0.1.0</b>')
        self.assertLess(installed, previous)
        self.assertLess(previous, first)
        self.assertIn('Bedrock phone test passed', self.history)
        self.assertIn('The earlier 0.1.1 phone test below is historical.', self.history)


if __name__ == '__main__':
    unittest.main()
