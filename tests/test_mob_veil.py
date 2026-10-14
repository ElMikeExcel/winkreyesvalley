"""Player-facing contract for the Veil Potion guide."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class MobVeilChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = (ROOT / 'index.html').read_text()
        cls.guide = cls.text.split('id="mob-veil"', 1)[1].split('</div>', 1)[0]

    def test_price_and_drink_later(self):
        self.assertIn('<tr><td>1 Veil Potion (drink later)</td><td>$2,000</td></tr>', self.text)
        for phrase in ['$2,000 in-game money', 'one stored potion',
                       'Buying or carrying it does not activate the veil; drink it first.', '/veil buy']:
            self.assertIn(phrase, self.guide)

    def test_separate_purchase_confirmation(self):
        for phrase in ['price, balance and money left or shortfall',
                       'separate <b>Confirm</b>',
                       'Opening the review, repeating the buy command, going Back or closing it does not buy anything.']:
            self.assertIn(phrase, self.guide)

    def test_stacking_and_real_time(self):
        for phrase in ['Every drink adds eight real-time minutes', 'whatever time remains',
                       'about sixteen minutes', '/veil status',
                       'offline and through ordinary server restarts']:
            self.assertIn(phrase, self.guide)

    def test_farming_and_armor(self):
        for phrase in ['standard mobs ignore you, even in armor',
                       'Other players can still see your armor and held items.',
                       'Harvesting, planting, tilling, chopping, mining and air swings keep the effect.',
                       'Passive Thorns retaliation also keeps it.']:
            self.assertIn(phrase, self.guide)

    def test_attacks_and_removal_end_all_time(self):
        for phrase in ['Attacking ends all accumulated time.', 'offensive projectile',
                       'Milk, death, expiry', 'removing/replacing invisibility',
                       'ordinary invisibility effect can block', 'Do not brew Veil Potions']:
            self.assertIn(phrase, self.guide)

    def test_first_version_limits(self):
        for phrase in ['not invulnerability', 'Existing projectiles', 'environmental hazards',
                       'EliteMobs custom boss scripts and Ender Dragon behavior',
                       'outside the first-version targeting guarantee',
                       'Wardens', 'investigate sounds', 'nearby darkness',
                       'separate from Death Protection']:
            self.assertIn(phrase, self.guide)

    def test_acceptance_not_overclaimed(self):
        self.assertIn('Real Java/Bedrock screens, live purchases and the full live plugin combination remain unverified.', self.guide)
        self.assertNotIn('all tests passed', self.guide.lower())
        self.assertNotIn('all mobs', self.guide.lower())

    def test_installed_status_and_preserved_history(self):
        self.assertIn('ExcelMobVeil 0.1.0 is installed, October 13, 2026.', self.guide)
        self.assertIn('<td>ExcelMobVeil<small class="plugin-next">Created by us</small></td><td>0.1.0</td>', self.text)
        history = self.text.split('<section id="changelog">', 1)[1]
        self.assertLess(history.index('Installed <b>ExcelMobVeil 0.1.0</b>'),
                        history.index('Installed <b>ExcelDeathProtection 0.1.3</b>'))
        self.assertIn('Installed <b>ExcelDeathProtection 0.1.2</b>', history)
        self.assertIn('Updated <b>ExcelDeathProtection to 0.1.1</b>', history)

    def test_source_guide_link(self):
        self.assertIn('ExcelMobVeil/PLAYER-GUIDE.md', self.guide)
        self.assertIn('rel="noopener noreferrer"', self.guide)


if __name__ == '__main__':
    unittest.main()
