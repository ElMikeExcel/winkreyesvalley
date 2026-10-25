"""Join ports: Java stays on 20795, Bedrock has its own port (NetherNet).
Accepts the NEW_PORT placeholder until the real port is filled in."""
import json, re, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
JAVA = 'wrv.duckdns.org:20795'


class PortChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = (ROOT / 'index.html').read_text(encoding='utf-8')
        m = re.search(r'addExternalServer=Wink%20Reyes%20Valley\|wrv\.duckdns\.org:(\w+)"', cls.text)
        cls.bedrock = m.group(1) if m else None

    def test_bedrock_port_is_placeholder_or_real_and_not_java(self):
        self.assertIsNotNone(self.bedrock)
        self.assertTrue(self.bedrock == 'NEW_PORT' or (self.bedrock.isdigit() and 1 <= int(self.bedrock) <= 65535), self.bedrock)
        self.assertNotEqual(self.bedrock, '20795')

    def test_java_address_unchanged(self):
        java = self.text.split('<h3>Java on PC or Mac</h3>', 1)[1].split('</article>', 1)[0]
        self.assertIn(JAVA, java)
        self.assertIn(JAVA, self.text.split('id="ports"', 1)[1].split('</p>', 1)[0])
        self.assertIn("makeBox('Java Port', '20795')", self.text)

    def test_every_bedrock_join_spot_uses_bedrock_port(self):
        b = self.bedrock
        for card in ['<h3>Phone, iPad or tablet</h3>', '<h3>Windows (Bedrock)</h3>']:
            body = self.text.split(card, 1)[1].split('</article>', 1)[0]
            self.assertIn('Port: <b>%s</b>' % b, body)
            self.assertNotIn('20795', body)
            self.assertIn('Trust', body)
        console = self.text.split('<h3>Xbox, PlayStation, Switch</h3>', 1)[1].split('</article>', 1)[0]
        self.assertIn('port <b>%s</b>' % b, console)
        self.assertIn('BedrockConnect', console)
        self.assertIn("makeBox('Bedrock Port', '%s')" % b, self.text)
        self.assertNotIn("makeBox('Port', '20795')", self.text)

    def test_change_port_steps_and_change_log(self):
        steps = self.text.split('id="bedrock-new-port"', 1)[1].split('</div>', 1)[0]
        for phrase in ['Edit', 'Change only the <b>Port</b>', self.bedrock, 'Tap <b>Trust</b>', 'once on each device', JAVA]:
            self.assertIn(phrase, steps)
        self.assertIn('id="cl-bedrock-port"', self.text)

    def test_no_em_dash_in_port_text(self):
        for anchor in ['id="ports"', 'id="bedrock-new-port"', 'id="cl-bedrock-port"']:
            self.assertNotIn('\u2014', self.text.split(anchor, 1)[1].split('</', 1)[0])

    def test_site_assistant_knows_both_ports(self):
        blob = (ROOT / 'ai-knowledge.json').read_text(encoding='utf-8')
        self.assertIn(JAVA, blob)
        self.assertIn('Bedrock has its own port now: %s' % self.bedrock, blob)


if __name__ == '__main__':
    unittest.main()
