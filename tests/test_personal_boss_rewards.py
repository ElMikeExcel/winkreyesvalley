from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]

class PersonalBossRewardDocsTests(unittest.TestCase):
    def test_personal_and_shared_rewards_are_distinct(self):
        page = (ROOT / 'index.html').read_text()
        block = page.split('id="personal-boss-rewards">', 1)[1].split('</div>', 1)[0]
        for text in ('every qualified teammate', 'once-per-seal signature limit',
                     'not awarded retroactively', 'one pool, not one copy per player',
                     'Raid rewards and boss difficulty are unchanged',
                     'Gravewhisper', "Monument's Answer", 'Hushwalkers', 'First Breath'):
            self.assertIn(text, block)

    def test_eligibility_and_claim_safety_are_explicit(self):
        page = (ROOT / 'index.html').read_text()
        block = page.split('id="personal-boss-rewards">', 1)[1].split('</div>', 1)[0]
        for text in ('including as a healer', 'below 70%', 'Creative and spectator',
                     'dying, respawning, disconnecting or reconnecting', 'anti-cheese',
                     '/bossrewards', 'My Boss Rewards', 'owner-only', 'Overworld, Nether or End',
                     'guild world is excluded', 'Losing the marker', 'inventory is full',
                     'Close your wand hotbar', 'needs review', 'player acceptance'):
            self.assertIn(text, block)

    def test_faq_and_corpus_include_reward_instructions(self):
        faq = (ROOT / 'questions.html').read_text()
        self.assertIn('id="personal-boss-rewards-qa"', faq)
        corpus = json.loads((ROOT / 'ai-knowledge.json').read_text())
        text = json.dumps(corpus)
        self.assertIn('My Boss Rewards', text)
        self.assertIn('one pool, not one copy per player', text)

    def test_installed_status_retains_pending_acceptance(self):
        page = (ROOT / 'index.html').read_text()
        block = page.split('id="personal-boss-rewards">', 1)[1].split('</div>', 1)[0]
        self.assertIn('Installed October 28, 2026, about 8:44 PM Central', block)
        self.assertNotIn('Preview', block)
        self.assertIn('Real Java/Bedrock player checks are still pending', block)
        self.assertIn('draft and unmerged', block)
        self.assertIn('0.2.9-offline-team-r2', page)
        self.assertIn('1.5.24-offline-team-r2', page)
