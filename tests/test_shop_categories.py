"""The organized shop guide must preserve checkout and report test limits honestly."""
from pathlib import Path
import unittest

TEXT=(Path(__file__).resolve().parents[1]/'index.html').read_text()
CURRENT=TEXT.split('<section id="changelog">',1)[0]
class CategoryGuideChecks(unittest.TestCase):
    def test_categories_and_balances(self):
        for phrase in ['Food:', 'Building:', 'Travel &amp; Animals:', 'Enchanting:', 'Potions &amp; Protection:',
                       'compact 3-by-3 menu', 'your balance', 'Back to Categories', 'Back to Menu', 'all 21 existing products']:
            self.assertIn(phrase,CURRENT)
    def test_navigation_and_confirmation_boundaries(self):
        for phrase in ['quantity <b>Back</b> returns to the categories', 'Cancel</b> keeps the current amount',
                       'final-review Back returns to quantity', 'Bedrock native-form Cancel/close stays closed',
                       'Browsing, Back and Cancel never purchase', 'separate final <b>Confirm purchase</b>',
                       '<code>/shop</code> opens the categories', 'standalone ordinary-item catalog as a fallback']:
            self.assertIn(phrase,CURRENT)
    def test_current_version_and_narrow_phone_confirmation(self):
        self.assertIn('ExcelShops 1.1 is installed.', CURRENT)
        self.assertIn('Mike checked the new shop on his phone on October 14, 2026 and confirmed the flow works.', CURRENT)
        self.assertIn('A live purchase with money movement, and a second player buying from a chest shop, have not been verified yet.', CURRENT)
        for stale in ['ExcelShops 1.0 is installed.', 'Actual phone delivery, touch behavior and live-purchase acceptance remain unverified;', 'Real-device acceptance remains unverified']:
            self.assertNotIn(stale, CURRENT)
    def test_installed_mobile_controls_and_preserved_milestone(self):
        for phrase in ['readable native category and item lists on Bedrock',
                       'Bedrock shop controls (ExcelShops 1.1): read first, then choose the amount',
                       'Installed October 14, 2026.', 'Review purchase', 'Are you sure?']:
            self.assertIn(phrase, CURRENT)
        self.assertNotIn('ExcelShops 1.1 is prepared, not installed.', CURRENT)
        self.assertNotIn('Prepared for 1.1', CURRENT)
        self.assertIn('Installed <b>ExcelShops 0.1.6</b>', TEXT)
        self.assertIn('all 76 production classes are identical to 0.1.6', TEXT)
    def test_item_identity_quantity_back_and_safe_close(self):
        for phrase in ['view details', 'Enter exact amount', 'Review this quantity', 'Back to Food',
                       'same item’s details', 'closing number entry cancels safely', 'Open guarded review',
                       'They have no quantity editor', 'A numeric phone keyboard is not guaranteed',
                       'rather than opening unread inventory controls']:
            self.assertIn(phrase, CURRENT)
    def test_special_purchases_keep_exact_prices(self):
        for row in ['<tr><td>1 Veil Potion (drink later)</td><td>$2,000</td></tr>',
                    '<tr><td>Death Protection (activates immediately)</td><td>$15,000</td></tr>',
                    '<tr><td>1 +Death Protection Potion (drink later)</td><td>$30,000</td></tr>']:
            self.assertIn(row,CURRENT)
        self.assertIn('Spawn Shop → Potions &amp; Protection → Veil Potion',CURRENT)
if __name__=='__main__': unittest.main()

