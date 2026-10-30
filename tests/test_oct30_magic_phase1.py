# Excel signature: MikeExcel / WinkReyesValley. Existing contributor and upstream credits preserved.
from pathlib import Path
import json,unittest
ROOT=Path(__file__).resolve().parents[1]
class MagicPhase1October30(unittest.TestCase):
 def test_changelog_entry_present(self):
  t=(ROOT/'index.html').read_text()
  block=t.split('<summary>Oct 30, 2026</summary>',1)[1].split('</details>',1)[0]
  for x in ['Storm Shackle is a channel now, not a single aimed shot','holds a light slow on everything it touches while it runs','Cast again, or swap away from your wand, to stop','Boon costs less at higher ranks','The new rule (the martial lock)','Boon ends if you swap to a sword or any other non-wand item','about 3:41 AM Central']:
   self.assertIn(x,block)
 def test_spell_entries_match_new_behavior(self):
  t=(ROOT/'index.html').read_text()
  shackle=t.split('<b>Storm Shackle</b>',1)[1].split('</li>',1)[0]
  self.assertIn('toggle lightning channel',shackle);self.assertIn('light slow',shackle)
  boon=t.split('<b>Boon</b>',1)[1].split('</li>',1)[0]
  self.assertIn('while it is active',boon);self.assertIn('ends if you swap to a sword',boon)
 def test_knowledge_carries_the_changes(self):
  t=json.dumps(json.loads((ROOT/'ai-knowledge.json').read_text()))
  for x in ['Storm Shackle is a channel now','martial lock','toggle lightning channel','Your mana still does not refill while Boon is on']:
   self.assertIn(x,t)
 def test_prior_publication_retained(self):
  t=json.dumps(json.loads((ROOT/'ai-knowledge.json').read_text()))
  for x in ['Wand repair: a wand saved before today','Menus now turn away outdated screens','My Boss Rewards']:
   self.assertIn(x,t)
if __name__=='__main__': unittest.main()
