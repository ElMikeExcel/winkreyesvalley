from pathlib import Path
import unittest,json
ROOT=Path(__file__).resolve().parents[1]
class MagicInstallReceipt(unittest.TestCase):
 def test_exact_labels_hashes_and_acceptance_limits(self):
  s=(ROOT/'index.html').read_text()
  for x in ['11.2.5-baa3d91','0.3.4-sp-display-candidate','0.1.3-gear-history-prototype','October 28, 2026, about 11:38 PM Central','7f105d60970cefe20a91c6f5b6e439855686e6377237ba1bcf3bdf0299e3e3f0','167ab4881ffce3809723786c0f7942423ed127062874c3501c9d7fbe74fadef9','00886af57383c3074fbd20628d272e6aee257d285438c98e3c24b8efbc13b1ec','Positive runtime practice-observer acquisition still needs verification','Real Java/Bedrock practice, item-history and menu acceptance remains pending']:
   self.assertIn(x,s)
 def test_changelog_order_preserves_rewards(self):
  s=(ROOT/'index.html').read_text();self.assertLess(s.index('id="cl-magic-practice-item-history"'),s.index('id="cl-personal-boss-rewards"'))
 def test_earlier_counts_not_mistaken_for_current_totals(self):
  s=(ROOT/'index.html').read_text();self.assertIn('Earlier spell bands (before October 28 bundle)',s);self.assertIn('loaded definitions are not the same as spells available on your current wand',s)
 def test_corpus_includes_new_and_reward_facts(self):
  s=json.dumps(json.loads((ROOT/'ai-knowledge.json').read_text()))
  for x in ['Useful spell practice and item history installed','My Boss Rewards','Positive runtime practice-observer acquisition still needs verification']:
   self.assertIn(x,s)
