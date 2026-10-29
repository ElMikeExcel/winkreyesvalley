# Excel signature: MikeExcel / WinkReyesValley. Existing contributor and upstream credits preserved.
"""Dependency-free structural and content regression checks."""
import importlib.util
import json
import re
import unittest
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote

ROOT = Path(__file__).resolve().parents[1]
class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.nodes = []
        self.feed(text)
    def handle_starttag(self, tag, attrs):
        self.nodes.append((tag, dict(attrs)))

class SiteChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = (ROOT/'index.html').read_text()
        cls.page = Page(cls.text)
        cls.data = json.loads((ROOT/'data/mcmmo-guide.json').read_text())
        cls.ids = [a['id'] for _,a in cls.page.nodes if 'id' in a]
    def test_unique_ids_and_anchors(self):
        self.assertEqual(len(self.ids), len(set(self.ids)))
        for _,a in self.page.nodes:
            href=a.get('href','')
            if href.startswith('#'):
                self.assertIn(unquote(href[1:]),self.ids)
    def test_aria_targets(self):
        for _,a in self.page.nodes:
            for key in ['aria-controls','aria-labelledby','aria-describedby']:
                for ref in a.get(key,'').split():
                    self.assertIn(ref,self.ids)
    def test_all_skills_render_without_script(self):
        self.assertEqual(len(self.data['skills']),19)
        self.assertEqual(sum(len(s['abilities']) for s in self.data['skills']),82)
        for skill in self.data['skills']:
            nodes=[a for tag,a in self.page.nodes if a.get('id')=='mcmmo-'+skill['id']]
            self.assertEqual(len(nodes),1)
            self.assertNotIn('hidden',nodes[0])
            for a in skill['abilities']:
                self.assertIn(a['type'],['active','passive','manual'])
                self.assertTrue(a['description'])
                self.assertTrue(a['unlockLabel'])
                ranks=a['rankLevelsRetro']
                self.assertEqual(ranks,sorted(set(ranks)))
    def test_source_privacy_and_pinning(self):
        serialized=json.dumps(self.data)
        for private in ['/workspace/', 'shockbyte', 'player_uuid', 'password', 'api_key']:
            self.assertNotIn(private,serialized.lower())
        for skill in self.data['skills']:
            for a in skill['abilities']:
                self.assertTrue(a['sources'])
                for source in a['sources']:
                    self.assertTrue(source.startswith('https://github.com/mcMMO-Dev/mcMMO/blob/'+self.data['baseCommit']+'/'))
    def test_critical_caveats(self):
        for phrase in ['Together and Weekend XP update is installed', 'Salvaging destroys', 'can remove or weaken', 'TNT explodes immediately', 'Effective protection from level 500']:
            self.assertIn(phrase,self.text)
        self.assertNotIn('everyone gets extra skill points', self.text)
        self.assertNotIn('tap and hold) to get ready', self.text)
    def test_reproducible_generation(self):
        spec=importlib.util.spec_from_file_location('guide',ROOT/'scripts/build_guide.py')
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        self.assertEqual(module.render_page(self.text, self.data), self.text)
    def test_existing_guides_and_address(self):
        panels=[a for _,a in self.page.nodes if a.get('role')=='tabpanel']
        self.assertEqual(len(panels),18)
        for name in ['jobs','essentials','griefprevention','coreprotect','elitemobs','shops','shopkeepers','server-menu-compass','leaderboards','no-phantoms','restart-warnings','world-map','player-map','behind-the-scenes']:
            self.assertIn('panel-'+name,self.ids)
        self.assertIn('wrv.duckdns.org:20795',self.text)
    def test_preview_instructions_and_status(self):
        for phrase in ['/playermap list', 'ordinary empty map', 'Add paper to zoom out', 'Add an empty map to make a copy', 'Add a glass pane to make a locked copy', 'main hand', 'fixed, vanilla-aligned', 'does not follow or continuously recenter', 'ExcelPlayerMap 0.2.1 is installed on the family server.', 'not automatically upgraded', 'BlueMap web map removed', '/xpbonus status', '/xpbonus hide', '/xpbonus show', '/xpbonus toggle', 'Installed October 12, 2026.', 'after Mending']:
            self.assertIn(phrase, self.text)
        self.assertNotIn('/playermap get', self.text)
        self.assertNotIn('/playermap scale', self.text)
        self.assertNotIn('<td>BlueMap</td>', self.text)
        self.assertNotIn('Ask Mike for the map link', self.text)
        self.assertIn('Oct 12, 2026', self.text)
        self.assertIn('Oct 11, 2026', self.text)
        self.assertIn('Oct 10, 2026', self.text)
        self.assertIn('Oct 9, 2026', self.text)
    def test_installed_shop_controls_and_acceptance_limits(self):
        shop=self.text.split('id="panel-shops"',1)[1].split('id="panel-shopkeepers"',1)[0]
        for phrase in ['ExcelShops is running on its own (live version 1.3.2; the flow below was checked on 1.1); ChestShop has been removed.', '/excelshop setup', '/excelshop manage', '/wrvshop', 'Confirm purchase', 'Confirm and publish shop', 'The Jobs item shop and two purchasing example menus are paused.', '[Excel Shop]', '[WRV Shop]', 'PLAYER-CHECKLIST.md', 'a second player buying from a player shop']:
            self.assertIn(phrase, shop)
        for stale in ['Preview:', 'Those pauses are not live yet', 'just tap (right-click) the sign', 'To sell to it, hit (left-click)']:
            self.assertNotIn(stale,shop)
        self.assertIn('ChestShop has been removed.',shop)
        self.assertIn('Native Excel shops and Spawn Shop do not require the removed ChestShop plugin.',shop)
        self.assertNotIn('Line 1: leave it empty',shop)
        self.assertNotIn('Confirm Sell',shop)
        self.assertNotIn('no fix is installed yet',shop)
        self.assertIn('Java cursor checks are still open.',shop)
        self.assertIn('update the existing inventory instead of closing and reopening it',shop)
        self.assertNotIn('Chat-number entry is not a verified Java workaround',shop)
        self.assertIn('Chat-number entry is not a verified Java workaround',self.text.split('id="changelog"',1)[1])
        self.assertIn('Both the shop chest and its attached sign open the UI',shop)
        self.assertNotIn('/excelshop amount 19',shop)
        self.assertIn('<td>ExcelShops (WRVShops)<small class="plugin-next">Created by us</small></td><td><span class="pv">1.3.7-analytics-OFFLINE</span>',self.text)
        self.assertNotIn('<td>ChestShop</td>',self.text)
    def test_typed_amount_installed_with_pending_device_checks(self):
        preview=self.text.split('id="shop-amount-preview"',1)[1].split('</div>',1)[0]
        for phrase in ['ExcelShops 1.1 is installed.', 'Mike confirmed the Bedrock phone flow on October 14, 2026; Java display and input checks are still open.', 'Enter Amount', 'Use amount', '0.50', '19', '60 seconds', 'Escape is disabled', 'Bedrock keeps its native number forms', '0322d8ade7fe2a1a29ea20e70e1c8c9ebda6a465', 'AMOUNT-ENTRY-0.1.4.md', 'Other device checks are still open', 'console/controller', 'instead of a Java-only dialog', '70000']:
            self.assertIn(phrase,preview)
        self.assertIn('<td>ExcelShops (WRVShops)<small class="plugin-next">Created by us</small></td><td><span class="pv">1.3.7-analytics-OFFLINE</span>',self.text)
        self.assertNotIn('not installed',preview)
        self.assertNotIn('server still runs 0.1.3',preview)
    def test_installed_xp_status(self):
        xp = self.text.split('id="mcmmo-xp-preview"', 1)[1].split('</section>', 1)[0]
        for phrase in ['Installed October 12, 2026.', 'mcMMO 2.3.003-WRV-XP-2', 'WeekendXP 1.0.2', 'gameplay acceptance checks remain pending']:
            self.assertIn(phrase, xp)
        for stale in ['Not installed', 'awaiting installation', 'prepared update']:
            self.assertNotIn(stale, xp)
        self.assertRegex(self.text, r'<td>ExcelWeekendXP<small[^>]*>Created by us</small></td><td>1\.2\.0</td>')
        self.assertIn('<td>Excel XP (mcMMO)<small class="plugin-next">Modified by us · upstream mcMMO</small></td><td>2.3.003-WRV-XP-2</td>', self.text)
    def test_installed_map_status(self):
        panel = self.text.split('id="panel-player-map"', 1)[1].split('id="panel-world-map"', 1)[0]
        self.assertIn('ExcelPlayerMap 0.2.1 is installed on the family server.', panel)
        self.assertIn('a player reported successful map creation', panel)
        self.assertIn('not a crossplay pass', panel)
        self.assertIn('A later screenshot also shows two player names/markers and terrain.', panel)
        self.assertIn('Off-map edge-arrow behavior still needs a player check.', panel)
        self.assertIn('Sharing, zoom, locking, portals, and wider gameplay checks remain pending.', panel)
        self.assertNotIn('WRVPlayerMap 0.2.0 is not installed', panel)
        self.assertNotIn('prepared prototype', panel)
        self.assertRegex(self.text, r'<td>ExcelPlayerMap \(WRVPlayerMap\)<small[^>]*>Created by us</small></td><td>0\.2\.1</td>')
    def test_excel_names_identify_origin_without_runtime_rename(self):
        pairs = {'BedrockMenu':'ExcelBedrockMenu', 'Leaderboard':'ExcelLeaderboard', 'MenuJoin':'ExcelMenuJoin', 'NoPhantoms':'ExcelNoPhantoms', 'RestartCountdown':'ExcelRestartCountdown', 'ShopVillager':'ExcelShopVillager', 'WealthBoard':'ExcelWealthBoard', 'WeekendXP':'ExcelWeekendXP', 'WRVPlayerMap':'ExcelPlayerMap', 'WRVShops':'ExcelShops'}
        table=self.text.split('id="all-plugins"',1)[1].split('</section>',1)[0]
        for original, label in pairs.items():
            name = label if original in {'Leaderboard', 'NoPhantoms', 'RestartCountdown', 'WealthBoard', 'WeekendXP'} else f'{label} ({original})'
            self.assertIn(f'<td>{name}<small class="plugin-next">Created by us</small></td>', table)
        # New plugins may be added; each original project's attribution remains required above.
        self.assertGreaterEqual(table.count('Created by us</small>'),len(pairs))
        self.assertIn('Modified by us · upstream mcMMO',table)
        self.assertIn('Third-party by Zrips · settings customized',table)
        self.assertIn('built to replace DeluxeMenus', table)
        self.assertNotIn('<td>DeluxeMenus', table)
        self.assertIn('The wider runtime rename has been canceled.',table)
        self.assertNotIn('Planned:',table)
        self.assertNotIn('All remaining Excel renames are still planned.',self.text)
        self.assertNotIn('Planned plugin name:',self.text)
        self.assertIn('Created by us: ExcelProgression.',self.text)
        self.assertIn('nossr50 and the mcMMO Team</a>, who keep full credit for it.', self.text)
    def test_java_menu_removal_keeps_bedrock_pending(self):
        panel=self.text.split('id="panel-server-menu-compass"',1)[1].split('id="panel-leaderboards"',1)[0]
        self.assertIn('removed from the Java menu',panel)
        self.assertIn('Bedrock menu still has that button',panel)
        self.assertIn('removal is prepared but not installed',panel)
        self.assertIn('Jobs earnings, balances and the Spawn Shop’s balance display are unchanged.',panel)
    def test_user_reported_display_acceptance_is_narrow(self):
        panel = self.text.split('id="panel-player-map"', 1)[1].split('id="panel-world-map"', 1)[0]
        xp = self.text.split('id="mcmmo-xp-preview"', 1)[1].split('</section>', 1)[0]
        for phrase in ['compact five-pixel names', 'Appearance passed by owner report, October 12:', 'You do not need to make a replacement map.', '/excelplayermap']:
            self.assertIn(phrase, panel)
        for phrase in ['hides three seconds after your latest gain', 'enables future brief notifications', 'This is a basic user-reported pass']:
            self.assertIn(phrase, xp)
        self.assertNotIn('not installed yet', panel)
        self.assertNotIn('being prepared', xp)
        self.assertIn('The client platform was not supplied', panel)
        self.assertIn('precise timing and edge-case checks remain open', xp)
    def test_live_jobs_difficulty_and_staged_progression(self):
        jobs=self.text.split('id="panel-jobs"',1)[1].split('id="panel-essentials"',1)[0]
        for phrase in ['old points balances are preserved', 'server money and give job experience', 'not installed', 'full Jobs build is still blocked']:
            self.assertIn(phrase,jobs)
        self.assertNotIn('Jobs only pay money',jobs)
        self.assertIn('<b>Difficulty: Hard</b> in the Overworld, Nether, and End',self.text)
        self.assertIn('EliteMobs keeps its separate settings',self.text)
    def test_installed_mobile_wealthboard_instructions(self):
        panel=self.text.split('id="panel-leaderboards"',1)[1].split('id="panel-no-phantoms"',1)[0]
        for phrase in ['ExcelWealthBoard 1.4.0 is installed', 'Wink Reyes Valley',
                       'each full name and balance readable', 'same for Java and Bedrock',
                       'no permanent sidebar', 'no shortened names', '/leaderboard', '/baltop', '/mctop',
                       'No balances yet - go earn!', 'Phone-screen confirmation passed October 13.',
                       'What you should see when you join', 'PLAYER-GUIDE.md']:
            self.assertIn(phrase,panel)
        self.assertIn('<td>ExcelWealthBoard<small class="plugin-next">Created by us</small></td><td>1.4.0</td>',self.text)
        changelog=self.text.split('id="changelog"',1)[1]
        self.assertLess(changelog.index('Oct 13, 2026'),changelog.index('Oct 12, 2026'))
        self.assertIn('WealthBoard 1.3.0-mobile.1',changelog)
        for stale in ['not installed', 'undeployed candidate', 'passed on every device']:
            self.assertNotIn(stale,panel)
    def test_local_assets_exist(self):
        for tag,a in self.page.nodes:
            if tag not in ['script','link']:continue
            link=a.get('src') or a.get('href','')
            if link and not urlsplit(link).scheme and not link.startswith('#'):
                self.assertTrue((ROOT/urlsplit(link).path).is_file(),link)

if __name__=='__main__': unittest.main()

