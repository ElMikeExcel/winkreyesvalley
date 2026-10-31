# Excel signature: MikeExcel / WinkReyesValley. Existing contributor and upstream credits preserved.
from pathlib import Path
import json, re, unittest
ROOT = Path(__file__).resolve().parents[1]

def row(t, name):
    return t.split('<tr><td>' + name, 1)[1].split('</tr>', 1)[0]

class ConsolidatedOctober31(unittest.TestCase):
    def test_oct31_block_is_newest_and_open(self):
        t = (ROOT / 'index.html').read_text()
        i31 = t.find('<summary>Oct 31, 2026</summary>')
        i30 = t.find('<summary>Oct 30, 2026</summary>')
        self.assertTrue(0 < i31 < i30)
        for x in ['Halloween is live through Nov 5', 'Lost &amp; Found: cheaper, longer, no daily cap',
                  'BossTrial 0.2.11: the phase fix', 'Paper and Geyser rode along', 'Paper 26.3-234']:
            self.assertIn(x, t)

    def test_oct30_block_additions(self):
        t = (ROOT / 'index.html').read_text()
        block = t.split('<summary>Oct 30, 2026</summary>', 1)[1].split('</details>', 1)[0]
        for x in ['Seal alerts reach Mike again', 'Aim Assist toggle in the Server Menu',
                  'Wand bars 0.3.5: arrange your bar', 'Magic tune: Shackle and Boon breathe again',
                  'Server updates: shared XP, Shopkeepers and the menus',
                  'These two notes replace what the earlier Oct 30 entries said about mana not refilling']:
            self.assertIn(x, block)

    def test_maker_sentence_restored(self):
        t = (ROOT / 'index.html').read_text()
        item = t.split('id="cl-oct29-maintenance-fixes"', 1)[1].split('</li>', 1)[0]
        self.assertIn('Wand history checks avoid unnecessary item copying.', item)

    def test_lostfound_current_rules(self):
        t = (ROOT / 'index.html').read_text()
        r = row(t, 'ExcelDeathRecord')
        for x in ['in the last 14 days', 'Each recovery costs $10,000', 'no daily limit',
                  "Spawn Shop's Potions &amp; Protection page opens Lost &amp; Found"]:
            self.assertIn(x, r)
        for x in ['in the last 7 days', 'costs $16,000', 'one recovery a day']:
            self.assertNotIn(x, r)
        hist = t.split("Lost &amp; Found, Maker's mark", 1)[1].split('</li>', 1)[0]
        self.assertIn('Launch terms', hist)
        self.assertIn('changed Oct 31, 2026: $10,000, 14 days, no daily limit', hist)

    def test_spell_entries_phase12_truth(self):
        t = (ROOT / 'index.html').read_text()
        boon = t.split('<b>Boon</b>', 1)[1].split('</li>', 1)[0]
        self.assertIn('mana pool is cut in half', boon)
        self.assertIn('refills keep running', boon)
        self.assertNotIn('does not refill', boon)
        shackle = t.split('<b>Storm Shackle</b>', 1)[1].split('</li>', 1)[0]
        self.assertIn('keeps refilling during the channel', shackle)
        self.assertNotIn('does not refill', shackle)

    def test_listing_versions_current(self):
        t = (ROOT / 'index.html').read_text()
        for name, ver in [('Excel Projectile Assist (ExcelAimAssist)', '0.1.4'),
                          ('ExcelBedrockMenu (BedrockMenu)', '1.5.27'),
                          ('ExcelBossTrial', '0.2.11'),
                          ('ExcelMenu', '0.1.8'),
                          ('ExcelMenuJoin (MenuJoin)', '1.4.3'),
                          ('ExcelTogether', '0.4.3'),
                          ('ExcelRewardGuard', '1.6'),
                          ('Geyser-Spigot', '2.12.1-b1279'),
                          ('ExcelWandBars', '0.3.5'),
                          ('Halloween (Halloween_Softici)', '3.4.0')]:
            r = row(t, name)
            self.assertEqual(re.search(r'<span class="pv">(.*?)</span>', r)[1], ver, name)
        self.assertIn('<td>2.28.1</td>', row(t, 'Shopkeepers'))

    def test_halloween_section_and_row(self):
        t = (ROOT / 'index.html').read_text()
        sec = t.split('<div class="howto" id="halloween">', 1)[1].split('</ul>', 1)[0]
        for x in ['Witching Hour, 7 PM to 2 AM Central', '/halloween disable', 'Pumpkin Zombie Boss',
                  'Pumpkin Skeleton Boss', 'Grave ritual', 'Pumpkin Trader']:
            self.assertIn(x, t.split('<div class="howto" id="halloween">', 1)[1].split('Still to check in game', 1)[0])

    def test_boss_rewards_auto_open_documented(self):
        t = (ROOT / 'index.html').read_text()
        howto = t.split('id="personal-boss-rewards"', 1)[1].split('</div>', 1)[0]
        self.assertIn('opens on its own right after a boss verdict', howto)

    def test_mana_glyph_qa(self):
        q = (ROOT / 'questions.html').read_text()
        sec = q.split('id="magic-mana-wait-qa"', 1)[1].split('</section>', 1)[0]
        self.assertIn('mana-wait indicator', sec)
        self.assertIn('not a cooldown', sec)

    def test_knowledge_carries_new_truths(self):
        t = json.dumps(json.loads((ROOT / 'ai-knowledge.json').read_text()))
        for x in ['mana-wait indicator', 'Witching Hour', 'Wand history checks avoid unnecessary item copying',
                  'Each recovery costs $10,000', 'in the last 14 days', 'Aim Assist toggle in the Server Menu',
                  'Halloween is live through Nov 5', 'mana pool is cut in half']:
            self.assertIn(x, t)

    def test_no_current_surface_states_old_lostfound_rules(self):
        t = (ROOT / 'index.html').read_text()
        r = row(t, 'ExcelDeathRecord')
        self.assertNotIn('$16,000', r)

if __name__ == '__main__':
    unittest.main()
