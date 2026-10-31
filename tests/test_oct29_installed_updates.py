# Excel signature: MikeExcel / WinkReyesValley. Existing contributor and upstream credits preserved.
from pathlib import Path
import re,json,unittest
ROOT=Path(__file__).resolve().parents[1]
class InstalledOctober29(unittest.TestCase):
 def test_current_rows_have_receipted_versions(self):
  t=(ROOT/'index.html').read_text()
  for name,version in [('Geyser-Spigot','2.12.1-b1279'),('ExcelBossTrial','0.2.11'),('ExcelMenu','0.1.8'),('ExcelShops (WRVShops)','1.3.7-analytics-OFFLINE'),('ExcelMakersMark','0.1.5-lookup-prefilter-OFFLINE')]:
   row=t.split('<tr><td>'+name,1)[1].split('</tr>',1)[0]
   self.assertEqual(re.search(r'<span class="pv">(.*?)</span>',row)[1],version)
 def test_bedrock_current_not_future(self):
  for f in ['index.html','questions.html']:
   t=(ROOT/f).read_text().split('<h2>Change log</h2>',1)[0];self.assertNotIn('Bedrock 26.60, planned for October 27',t);self.assertIn('a natural Bedrock 26.60',t)
 def test_acceptance_remains_bounded(self):
  t=(ROOT/'index.html').read_text()
  for x in ['natural double-chest/hopper activity','Natural real-player refresh/click acceptance remains pending','No live purchase, forced crash or disk-stall','no live performance gain','This confirms that connection only']:
   self.assertIn(x,t)
 def test_prior_features_retained(self):
  t=json.dumps(json.loads((ROOT/'ai-knowledge.json').read_text()))
  for x in ['My Boss Rewards','Silk Touch Warnings','Positive runtime practice-observer acquisition still needs verification','one-fifth milestone credit']:
   self.assertIn(x,t)
 def test_new_summary_has_no_player_identity(self):
  t=(ROOT/'index.html').read_text().split('id="cl-oct29-maintenance-fixes"',1)[1].split('</li>',1)[0]
  self.assertNotIn('diagnostic JAR',t);self.assertNotIn('proximity chat',t)
