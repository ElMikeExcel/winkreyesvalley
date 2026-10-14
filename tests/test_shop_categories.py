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
    def test_current_version_and_unverified_real_clients(self):
        self.assertIn('ExcelShops 1.0 is installed.',CURRENT)
        self.assertNotIn('ExcelShops 0.1.5',CURRENT)
        self.assertIn('Actual phone delivery, touch behavior and live-purchase acceptance remain unverified;',CURRENT)
        self.assertIn('no new player test is being requested',CURRENT)
        self.assertNotIn('All-device checks are pending',CURRENT)
        self.assertNotIn('Cursor update installed; player retest pending',CURRENT)
    def test_version_only_milestone_and_mobile_boundary(self):
        self.assertIn('readable native category and item lists on Bedrock', CURRENT)
        self.assertIn('ExcelShops 1.1 is prepared, not installed.', CURRENT)
        self.assertIn('item-specific details and an explicit category Back button', CURRENT)
        self.assertIn('holding to read descriptions felt clunky', CURRENT)
        self.assertIn('Installed <b>ExcelShops 0.1.6</b>', TEXT)
        self.assertIn('all 76 production classes are identical to 0.1.6', TEXT)
    def test_item_identity_quantity_back_and_safe_close(self):
        for phrase in ['view details', 'Enter exact amount', 'Review this quantity', 'Back to Food',
                       'same item’s details', 'Closing number entry cancels safely', 'Open guarded review',
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

