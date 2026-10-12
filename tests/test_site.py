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
        generated=module.INTRO+'\n'.join(module.render_skill(s) for s in self.data['skills'])+module.OUTRO
        self.assertIn(module.START+'\n'+generated,self.text)
    def test_existing_guides_and_address(self):
        panels=[a for _,a in self.page.nodes if a.get('role')=='tabpanel']
        self.assertEqual(len(panels),15)
        for name in ['jobs','essentials','griefprevention','coreprotect','elitemobs','shops','shopkeepers','server-menu-compass','leaderboards','no-phantoms','restart-warnings','world-map','player-map','behind-the-scenes']:
            self.assertIn('panel-'+name,self.ids)
        self.assertIn('winkreyes.duckdns.org:20795',self.text)
    def test_preview_instructions_and_status(self):
        for phrase in ['/playermap list', 'ordinary empty map', 'Add paper to zoom out', 'Add an empty map to make a copy', 'Add a glass pane to make a locked copy', 'main hand', 'fixed, vanilla-aligned', 'does not follow or continuously recenter', 'WRVPlayerMap 0.2.0 is installed on the family server.', 'not automatically upgraded', 'BlueMap web map removed', '/xpbonus status', '/xpbonus hide', '/xpbonus show', '/xpbonus toggle', 'Installed October 12, 2026.', 'after Mending']:
            self.assertIn(phrase, self.text)
        self.assertNotIn('/playermap get', self.text)
        self.assertNotIn('/playermap scale', self.text)
        self.assertNotIn('<td>BlueMap</td>', self.text)
        self.assertNotIn('Ask Mike for the map link', self.text)
        self.assertIn('Oct 12, 2026', self.text)
        self.assertIn('Oct 11, 2026', self.text)
        self.assertIn('Oct 10, 2026', self.text)
        self.assertIn('Oct 9, 2026', self.text)
    def test_shop_preview_keeps_live_controls_separate(self):
        for phrase in ['WRVShops 0.1.0 is not installed yet.', '/wrvshop amount 19', '/wrvshop amount 12.50', '/wrvshop setup', '/wrvshop manage', 'Confirm purchase', 'Confirm and publish shop', 'not active in the current Spawn Shop yet', 'Line 1: leave it empty', 'B 40']:
            self.assertIn(phrase, self.text)
        self.assertNotIn('<td>WRVShops</td>', self.text)
    def test_installed_xp_status(self):
        xp = self.text.split('id="mcmmo-xp-preview"', 1)[1].split('</section>', 1)[0]
        for phrase in ['Installed October 12, 2026.', 'mcMMO 2.3.003-WRV-XP-1', 'WeekendXP 1.0.2', 'gameplay acceptance checks remain pending']:
            self.assertIn(phrase, xp)
        for stale in ['Not installed', 'awaiting installation', 'prepared update']:
            self.assertNotIn(stale, xp)
        self.assertIn('<td>WeekendXP</td><td>1.0.2</td>', self.text)
        self.assertIn('<td>mcMMO</td><td>2.3.003-WRV-XP-1</td>', self.text)
    def test_installed_map_status(self):
        panel = self.text.split('id="panel-player-map"', 1)[1].split('id="panel-world-map"', 1)[0]
        self.assertIn('WRVPlayerMap 0.2.0 is installed on the family server.', panel)
        self.assertIn('Real Java/Bedrock display and gameplay acceptance checks are still needed.', panel)
        self.assertNotIn('not installed', panel)
        self.assertNotIn('prepared prototype', panel)
        self.assertIn('<td>WRVPlayerMap</td><td>0.2.0</td>', self.text)
    def test_local_assets_exist(self):
        for tag,a in self.page.nodes:
            if tag not in ['script','link']:continue
            link=a.get('src') or a.get('href','')
            if link and not urlsplit(link).scheme and not link.startswith('#'):
                self.assertTrue((ROOT/urlsplit(link).path).is_file(),link)

if __name__=='__main__': unittest.main()
