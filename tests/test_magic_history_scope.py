import json
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
class MagicHistoryScope(unittest.TestCase):
 def test_practice_limits_and_floors(self):
  s=(ROOT/'index.html').read_text().split('id="magic-progression"',1)[1].split('<h4>Combat Attunement',1)[0]
  for text in ['40 → 120 → 300 → 600 → 1,000','actual maximum','Single-level spells stay unlock-only','other utility spells keep their existing progression','No past cast counts are invented','unknown injury and overhealing','One practice credit is not a promise of an SP award','800 SP','1,600 SP','1,800 SP','25% rate','x1.2','x1.25','x1.5']:
   self.assertIn(text,s)
 def test_history_scope(self):
  s=(ROOT/'index.html').read_text().split('id="makers-mark"',1)[1].split('</div>',1)[0]
  for text in ['ordinary gear, shields and tested Magic wands','EliteMobs gear','one-fifth milestone credit','actual kill totals stay visible','/mark history page [number]','no drops or XP','without inventing a finishing kill']:
   self.assertIn(text,s)
  self.assertNotIn('Color milestones are not included',s)
 def test_seal_two_additions(self):
  s=(ROOT/'index.html').read_text()
  self.assertIn('Spark and Frostbite become available automatically through the normal Seal 2 unlock',s)
  self.assertIn('not the stronger Chain Lightning',s)
 def test_faq_policy_is_same(self):
  a=(ROOT/'index.html').read_text().split('<h4 id="magic-progression">How magic leveling works</h4>',1)[1].split('<h4>Combat Attunement',1)[0].strip()
  self.assertIn(a,(ROOT/'questions.html').read_text())
 def test_corpus_has_no_replaced_claims_in_current_faq(self):
  chunks=json.loads((ROOT/'ai-knowledge.json').read_text())
  for c in chunks:
   if c['id'] in ['magic-progression-qa','makers-mark-qa']:
    self.assertNotIn('abilities do not have independent grindable XP',c['text'])
    self.assertNotIn('Magic wands and EliteMobs gear are excluded',c['text'])
