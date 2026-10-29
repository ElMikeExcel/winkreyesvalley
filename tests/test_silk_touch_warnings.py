# Excel signature: MikeExcel / WinkReyesValley. Existing contributor and upstream credits preserved.
from pathlib import Path
import unittest,json
ROOT=Path(__file__).resolve().parents[1]
class SilkTouchWarnings(unittest.TestCase):
 def block(self):return (ROOT/'index.html').read_text().split('id="silk-touch-warnings">',1)[1].split('</div>',1)[0]
 def test_warning_only_and_scope(self):
  b=self.block()
  for x in ['own native ender chest','Silk Touch enchanted book','Warning only','no confirmation, cancellation, item movement or inventory edit','four levels, 256 visited stacks','Custom vaults, pouches, backpacks, bundles','withdrawals, cancelled moves and no-net-change swaps','three-second cooldown']:
   self.assertIn(x,b)
 def test_saved_personal_setting(self):
  b=self.block()
  for x in ['warnings start <b>ON</b>','Settings → Silk Touch Warnings','/silkwarnings on','/silkwarnings off','/silkwarnings status','saved across rejoin and restart','If saving fails, the old setting stays in effect','reopen it after changing']:
   self.assertIn(x,b)
 def test_install_does_not_claim_real_acceptance(self):
  b=self.block();self.assertIn('October 29, 2026, about 12:55 AM Central',b);self.assertIn('real-player deposits, saved-toggle checks, Java/Bedrock screens and hotbar-message coexistence remain pending',b)
 def test_faq_and_corpus(self):
  q=(ROOT/'questions.html').read_text();self.assertIn('id="silk-touch-warnings-qa"',q);self.assertIn('Custom vaults, pouches, backpacks, bundles',q)
  c=json.dumps(json.loads((ROOT/'ai-knowledge.json').read_text()));self.assertIn('Silk Touch Warnings',c);self.assertIn('My Boss Rewards',c);self.assertIn('Positive runtime practice-observer acquisition still needs verification',c)
 def test_versions_and_changelog(self):
  t=(ROOT/'index.html').read_text();self.assertIn('0.1.3-offline',t);self.assertIn('1.5.25-silk-offline',t);self.assertLess(t.index('id="cl-silk-touch-warnings"'),t.index('id="cl-magic-practice-item-history"'))
