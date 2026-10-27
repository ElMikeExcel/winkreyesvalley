"""October 15 guide corrections, live-version boundaries and canonical navigation."""
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
import re
import unittest

TEXT = (Path(__file__).resolve().parents[1] / 'index.html').read_text()
CURRENT, HISTORY = TEXT.split('<section id="changelog">', 1)
SHOPS = CURRENT.split('id="panel-shops"', 1)[1].split('id="panel-shopkeepers"', 1)[0]
BOARDS = CURRENT.split('id="panel-leaderboards"', 1)[1].split('id="panel-no-phantoms"', 1)[0]
MOBILE = SHOPS.split('id="mobile-shop-controls"', 1)[1].split('</div>', 1)[0]


def plain(value):
    return unescape(re.sub('<[^>]*>', '', value))


class AnchorParents(HTMLParser):
    def __init__(self, value):
        super().__init__()
        self.stack = []
        self.parents = {}
        self.feed(value)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.parents[attrs['id']] = tuple(self.stack)
        if tag not in {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}:
            self.stack.append(tag)

    def handle_endtag(self, tag):
        if tag in self.stack:
            self.stack = self.stack[:len(self.stack) - 1 - self.stack[::-1].index(tag)]


class GuideCleanupChecks(unittest.TestCase):
    def test_installed_11_exact_status_and_limits(self):
        for value in [
            'Bedrock shop controls (ExcelShops 1.1): read first, then choose the amount',
            'Installed October 14, 2026. On a phone or console, each item opens its own details screen before you choose an amount. Mike checked this flow on his phone on October 14 and confirmed it works.',
            'Mike checked the new shop on his phone on October 14, 2026 and confirmed the flow works.',
            'A live purchase with money movement, and a second player buying from a player shop, have not been verified yet.',
        ]:
            self.assertIn(value, plain(SHOPS))
        for stale in ['Prepared for 1.1', 'prepared 1.1', 'Not installed yet', 'ExcelShops 1.2', '3-tap']:
            self.assertNotIn(stale, SHOPS)

    def test_one_canonical_ordinary_item_walkthrough(self):
        steps = re.findall(r'<li>(.*?)</li>', MOBILE, re.S)
        self.assertEqual(len(steps), 5)
        for step, label in zip(steps, ['Item details:', 'Review this quantity:', 'Review purchase:', 'Are you sure?', 'Confirm purchase']):
            self.assertIn(label, plain(step))
        self.assertIn('Continue to confirmation', steps[2])
        self.assertIn('Only this action can move money or items.', steps[4])
        self.assertEqual(SHOPS.count('Are you sure?'), 1)
        self.assertGreaterEqual(SHOPS.count('href="#mobile-shop-controls"'), 4)
        self.assertIn('They have no quantity editor.', MOBILE)

    def test_shop_and_canonical_anchors_are_reachable(self):
        page = AnchorParents(CURRENT)
        for anchor in ['shops', 'shops-preview', 'mobile-shop-controls']:
            self.assertIn(anchor, page.parents)
            # Oct 23, 2026: the whole plugin guide sits in one section fold
            # (details.sec-fold); guide.js opens every fold around a linked
            # anchor. No other details may hide these anchors.
            self.assertLessEqual(page.parents[anchor].count('details'), 1)
        self.assertIn('<details class="sec-fold" id="guide-more">', CURRENT)
        self.assertIn('open every fold around the target', (Path(__file__).resolve().parents[1] / 'guide.js').read_text())
        self.assertIn('<h3 id="shops">', SHOPS)
        self.assertIn('id="shops-preview"', SHOPS)

    def test_exact_amounts_have_current_status(self):
        value = plain(SHOPS)
        for phrase in ['On Bedrock, the Spawn Shop uses item details → Enter exact amount',
                       'The Bedrock category-shop route instead closes safely if its native forms are unavailable.',
                       'Mike confirmed the Bedrock phone flow on October 14, 2026; Java display and input checks are still open.']:
            self.assertIn(phrase, value)
        self.assertNotIn('Real Java/Bedrock display and input behavior remains unverified', SHOPS)

    def test_audit_details_live_in_history(self):
        for phrase in ['Automated and partial native-plugin integration checks passed',
                       'isolated Geyser transport testing was limited by unavailable Minecraft discovery/auth services',
                       'Chat-number entry is not a verified Java workaround because closing the inventory clears its input context']:
            self.assertNotIn(phrase.lower(), CURRENT.lower())
            self.assertIn(phrase.lower(), HISTORY.lower())

    def test_wealthboard_version_and_historical_versions(self):
        self.assertIn('ExcelWealthBoard 1.4.0 is installed', BOARDS)
        self.assertIn('<td>ExcelWealthBoard<small class="plugin-next">Created by us</small></td><td>1.4.0</td>', CURRENT)
        self.assertIn('Updated WealthBoard to 1.3.0-mobile.7: welcome-title timing fix for the join popup.', HISTORY)
        self.assertIn('WealthBoard to 1.3.0-mobile.6', HISTORY)
        self.assertIn('WealthBoard 1.3.0-mobile.1', HISTORY)

    def test_nine_boards_with_platform_status(self):
        self.assertIn('/leaderboard opens the boards menu: Top Miner, Top Builder, Most Playtime, Top Slayer, Top Traveler, Most Deaths, Richest, mcMMO Power, Jobs Levels and Land Claimed. Land Claimed ranks everyone by how much land they have claimed, and every row also shows how many claim blocks that player can still claim. On a phone it is a button list; on Java it is a clickable chat menu. Mike confirmed the phone version works on October 15; the Java chat-menu check is still to come.', plain(BOARDS))
        self.assertNotIn('reopens the full wealth and mcMMO boards', BOARDS)

    def test_join_steps_are_expectations(self):
        join = BOARDS.split('id="wealthboard-mobile-check"', 1)[1].split('</div>', 1)[0]
        self.assertIn('What you should see when you join', join)
        self.assertEqual(join.count('<li>'), 3)
        for task in ['Leave and rejoin', 'Watch the rankings', 'confirm each name', 'Type <code>']:
            self.assertNotIn(task, join)

    def test_guild_is_not_open(self):
        elite = CURRENT.split('id="panel-elitemobs"', 1)[1].split('id="panel-shops"', 1)[0]
        self.assertIn("hall stands built, but it is sealed:", elite)
        self.assertNotIn('There are also adventure areas to explore', elite)
        self.assertIn('Phase 2 is still pending', HISTORY)

    def test_requested_small_wording(self):
        value = plain(CURRENT)
        for phrase in ['If a setup was canceled, look at the attached ordinary sign and use /excelshop setup to pick up where you left off.',
                       'ExcelPlayerMap and ExcelShops already use their Excel names',
                       'These trade stands are different from the green Spawn Shop villager, who opens the Spawn Shop menu instead of trading.',
                       'Our ExcelAcrobatics add-on feeds extra XP into this same skill for water landings and fatal falls.']:
            self.assertIn(phrase, value)
        self.assertNotIn('Stock an empty chest first.', SHOPS)


if __name__ == '__main__':
    unittest.main()
