import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class DualPortDocs(unittest.TestCase):
 def test_keep_working_bedrock_entries(self):
  s=(ROOT/'index.html').read_text()
  self.assertNotIn('If you saved us there before with port 20795, remove that entry',s)
  self.assertIn('Keep a saved entry that already works',s)
  self.assertIn('If you cannot join on 25622, try 20795',s)
  self.assertIn('Java keeps port <b>20795</b>',s)
  self.assertIn('id="cl-bedrock-both-ports"',s)
 def test_faq_allows_both_directions(self):
  s=(ROOT/'questions.html').read_text()
  self.assertIn('try the other (20795 or 25622)',s)
  self.assertNotIn('If Bedrock shows the server as offline or will not connect, edit the saved server and change the port to 25622.',s)
