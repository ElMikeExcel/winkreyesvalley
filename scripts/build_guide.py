#!/usr/bin/env python3
"""Render the checked-in mcMMO data into the existing static page (no packages)."""
import argparse
import hashlib
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
START, END = '<!-- MCMO_GUIDE_START -->', '<!-- MCMO_GUIDE_END -->'

def esc(value):
    return html.escape(str(value), quote=True)

def paragraph(text, label='', css=''):
    if not text:
        return ''
    prefix = f'<b>{esc(label)}</b> ' if label else ''
    attr = f' class="{esc(css)}"' if css else ''
    return f'<p{attr}>{prefix}{esc(text)}</p>'

def render_skill(skill):
    name, sid = esc(skill['name']), esc(skill['id'])
    category = esc(skill['category'])
    abilities = skill['abilities']
    out = [f'<details class="skill-card" id="mcmmo-{sid}" data-category="{category}">',
           f'<summary><span class="skill-title">{name}</span>',
           f'<span class="skill-summary">{esc(skill["summary"])}</span>',
           f'<span class="skill-meta">{len(abilities)} abilities · Tap to see unlocks</span></summary>',
           '<div class="skill-body">',
           f'<p class="skill-command"><code>{esc(skill["command"])}</code> shows your progress. <a href="#mcmmo-{sid}" aria-label="Link to {name}">Link to this skill</a></p>',
           paragraph(skill['training'], 'How to level up:'),
           paragraph(skill.get('activation'), 'How to use it:'),
           paragraph(skill.get('warning'), 'Be careful:', 'guide-warning')]
    notes = skill.get('caveats', [])
    for note in notes:
        out.append(paragraph(note))
    out.append('<ul class="ability-list">')
    for ability in abilities:
        kind = ability.get('type', 'passive')
        label = {'active':'Active boost', 'manual':'Use it yourself', 'passive':'Automatic'}[kind]
        unlock = ability.get('unlockLabel') or f'Level {ability["unlockRetro"]}'
        out += ['<li class="ability">', f'<h5>{esc(ability["name"])}</h5>',
                f'<div class="ability-tags"><span class="ability-type {kind}">{label}</span><span class="unlock">{esc(unlock)}</span></div>',
                paragraph(ability['description'])]
        if ability.get('activation') and not ability['activation'].startswith('Passive: works automatically'):
            out.append(paragraph(ability['activation'], 'Use:'))
        cooldown = ability.get('cooldown')
        if isinstance(cooldown, (float, int)) and cooldown:
            cooldown = f'{int(cooldown // 60)} minute' + ('s' if cooldown != 60 else '') + ' after it ends.'
        if cooldown and ability.get('cooldownSeconds'):
            out.append(paragraph(cooldown, 'Wait:'))
        ranks = ability.get('rankLevelsRetro', [])
        if len(ranks) > 1:
            out.append(paragraph(' → '.join(map(str, ranks)), 'Rank levels:', 'rank-list'))
        out.append(paragraph(ability.get('warning'), 'Be careful:', 'guide-warning'))
        for caveat in ability.get('caveats', []):
            out.append(paragraph(caveat, css='ability-note'))
        details = [ability['detail']] if ability.get('detail') else []
        if details:
            out.append('<details class="skill-notes"><summary>More about this ability</summary>')
            for detail in details:
                out.append(paragraph(detail))
            out.append('</details>')
        recipes = ability.get('recipes', [])
        if recipes:
            out.append('<details class="skill-notes"><summary>Ingredients you unlock</summary><ul>')
            for recipe in recipes:
                out.append(f'<li><b>Level {esc(recipe["level"])}:</b> {esc(recipe["ingredients"])}</li>')
            out.append('</ul></details>')
        out.append('</li>')
    out.append('</ul>')
    sources = list(dict.fromkeys(skill.get('sources', []) + [source for a in abilities for source in a.get('sources', [])]))
    if sources:
        out += ['<details class="guide-sources"><summary>Sources for this skill</summary>',
                '<p>Implementation checked against the version-pinned mcMMO source and server settings. These links are for anyone who wants the technical details.</p><ul>']
        # A few useful, stable sources per skill keep the public guide readable.
        chosen = list(dict.fromkeys([u for u in sources if 'skillranks.yml' in u][:1] + [u for u in sources if '.java' in u][:3] + [u for u in sources if 'advanced.yml' in u][:1]))
        for source in chosen:
            title = source.split('/')[-1].split('#')[0].replace('.java', '').replace('.yml', ' settings')
            out.append(f'<li><a href="{esc(source)}">{esc(title)}</a></li>')
        out.append('</ul></details>')
    out.append('</div></details>')
    return '\n'.join(out)

INTRO = '''
<div class="panel guide-panel" role="tabpanel" id="panel-mcmmo" aria-labelledby="tab-mcmmo" tabindex="0">
  <div class="guide-intro">
    <p class="guide-kicker">The family field guide</p>
    <h3 class="guide-title">mcMMO: what will you unlock next?</h3>
    <p>Mine, fish, farm, fight, and get better as you play. Every skill has its own level, and you can work on all of them. You don't have to choose a class.</p>
    <p>Some rewards happen automatically. Others are short boosts you switch on. Pick a skill below to see what it does, when it unlocks, and how to use it.</p>
  </div>
  <nav class="guide-nav" aria-label="mcMMO guide sections">
    <a href="#mcmmo-skills">Explore skills</a><a href="#mcmmo-activate">Use an ability</a><a href="#mcmmo-commands">Useful commands</a><a href="#mcmmo-party">Play together</a>
  </nav>
  <div class="guide-facts">
    <div class="guide-fact"><b>19 skills to explore</b><p>Gathering, fighting, and useful everyday skills.</p></div>
    <div class="guide-fact"><b>Your levels matter</b><p>Unlocks use this server's Retro scale. Level 1000 is a milestone, not a hard limit.</p></div>
    <div class="guide-fact"><b>Start with /mcstats</b><p>See your levels, then try a skill command such as <code>/mining</code>.</p></div>
  </div>
  <div class="howto">
    <h4>New here? Try Mining first.</h4>
    <p>Mine natural stone and ores. Double Drops starts at level 1; your first Super Breaker boost unlocks at Mining level 50. <a href="#mcmmo-mining">See the Mining card</a>.</p>
    <p class="note">mcMMO skill XP is different from green Minecraft XP orbs and Jobs money. Placing and re-breaking the same blocks usually won't earn skill rewards.</p>
  </div>
  <section class="guide-section" id="mcmmo-skills" aria-labelledby="mcmmo-skills-title">
    <h4 id="mcmmo-skills-title">Find your next skill</h4>
    <p class="guide-legend"><span class="ability-type passive">Automatic</span> happens while you play. <span class="ability-type active">Active boost</span> needs activating. <span class="ability-type manual">Use it yourself</span> needs a special action.</p>
    <p class="note">In combat, 2 damage points equal 1 heart. Let melee attacks fully charge for the strongest hits; armor can reduce the final damage.</p>
    <p class="note">Unlock levels below were checked against server files on October 12, 2026 (UTC). Your in-game skill command shows your current bonuses and any permission-based differences.</p>
    <div class="skill-controls" id="skill-controls" hidden>
      <div class="skill-fields">
        <div><label for="skill-search">Search skills or abilities</label><input id="skill-search" type="search" placeholder="Try mining or wolves" autocomplete="off" aria-describedby="skill-results"></div>
        <div><label for="skill-category">Type of skill</label><select id="skill-category"><option value="all">All skills</option><option value="gathering">Gathering</option><option value="combat">Combat</option><option value="utility">Useful skills</option></select></div>
      </div>
      <div class="skill-actions"><button class="plain-btn" id="skill-reset" type="button">Clear filters</button><button class="plain-btn" id="skill-expand" type="button">Open shown skills</button><button class="plain-btn" id="skill-collapse" type="button">Close all skills</button></div>
      <p class="skill-results" id="skill-results" role="status" aria-live="polite" aria-atomic="true"></p>
    </div>
    <p class="skill-empty" id="skill-empty" hidden>No skills match that search. Try an ability name, a shorter word, or choose All skills.</p>
    <div class="skill-grid">
'''
OUTRO = '''
    </div>
  </section>
  <section class="guide-section" id="mcmmo-activate" aria-labelledby="mcmmo-activate-title">
    <h4 id="mcmmo-activate-title">How to use an active ability</h4>
    <ol class="guide-steps">
      <li>Reach the required level and hold the right tool.</li>
      <li>Use/right-click the tool to ready it. On a phone or controller, use your control scheme's <b>Use / Interact</b> action.</li>
      <li>Within <b>4 seconds</b>, do the matching action: mine, chop, dig, harvest, or hit a target.</li>
      <li>Watch for the ability message. After the boost ends, most active abilities have a <b>4-minute base cooldown</b>. Blast Mining has its own activation and a <b>1-minute cooldown</b>.</li>
    </ol>
    <p>The usual level-50 boosts start at about 3 seconds, grow to 12 seconds at level 500, and reach 22 seconds at level 1000. Player perks can change the timing.</p>
    <div class="howto"><h4>Nothing happened?</h4><p>Check your level with the skill command and your timer with <code>/mccooldown</code>. Make sure you're using the right tool and target. With something in your off-hand, try sneaking while you ready the tool. <code>/mcability</code> toggles ability activation, so check its message instead of repeatedly switching it.</p><p class="note">Touch controls differ by Minecraft control scheme. A long press is not the same action on every phone.</p></div>
    <p class="guide-warning"><b>Keep family builds safe.</b> Tree Feller can take down connected logs, and Blast Mining explodes immediately. Practice far from homes, animals, and other players. Repair may remove enchantments; Salvage destroys the item.</p>
  </section>
  <section class="guide-section" id="mcmmo-commands" aria-labelledby="mcmmo-commands-title">
    <h4 id="mcmmo-commands-title">Useful commands</h4>
    <ul class="cmds">
      <li><code>/mcstats</code> see all your skill levels</li>
      <li><code>/mining</code> see one skill; swap in <code>/fishing</code>, <code>/repair</code>, or another skill name</li>
      <li><code>/mccooldown</code> check when your active abilities are ready</li>
      <li><code>/mcability</code> turn ability activation on or off</li>
      <li><code>/mctop</code> see the skill leaderboard</li>
      <li><code>/party info</code> check your party and unlocked features</li>
    </ul>
    <p class="note">On Java, the compass menu's mcMMO Stats button also runs <code>/mcstats</code>. You can always use chat if a menu doesn't have that button.</p>
  </section>
  <section class="guide-section" id="mcmmo-party" aria-labelledby="mcmmo-party-title">
    <h4 id="mcmmo-party-title">Play together in a party</h4>
    <p>A party is a little team. Use Minecraft account names in commands, which can be different from display nicknames.</p>
    <ol class="guide-steps">
      <li>One person types <code>/party create Family</code> (or chooses another team name).</li>
      <li>Invite someone with <code>/party invite PlayerName</code>.</li>
      <li>The invited player types <code>/party accept</code>.</li>
      <li>Check <code>/party info</code> together. Use <code>/party quit</code> to leave.</li>
    </ol>
    <p>Party features unlock as the <b>party's level</b> rises: chat at 1, party teleport at 2, alliances at 5, item sharing at 8, and XP sharing at 10. These are party levels, separate from your skill levels. Features also depend on permissions; the compass teleport-request menu is still the easiest way to visit family.</p>
    <details class="skill-notes"><summary>How XP sharing works at party level 10</summary>
      <p>The party leader can use <code>/party xpshare equal</code> to share, or <code>/party xpshare none</code> to stop. Eligible teammates within <b>75 blocks</b> share the earned skill XP pool.</p>
      <p>With the checked settings, 100 earned XP shared by two nearby teammates becomes a 150-XP pool: <b>75 each</b>, before individual modifiers. Sharing helps everyone progress together, but does not mean each player gets 150 XP.</p>
    </details>
    <div class="howto"><h4>What about the Together bonus?</h4><p>The <b>Together and Weekend XP update is built and tested, awaiting installation</b>. The existing Together setting is saved on, but runtime activation is still pending. The new green-bar bonus and live indicator are not installed yet. Party XP sharing is a separate feature.</p></div>
    <details class="skill-notes"><summary>What is in the prepared XP update?</summary>
      <p><b>Not live yet:</b> the prepared build adds 25% more eligible mcMMO skill XP and green-bar XP when one online teammate in your party is less than 32 blocks away in the same world. The weekend boost is 20%; together on a weekend gives 50% more XP points.</p>
      <p>The update also includes a live bonus bar and <code>/xpbonus</code> status, show, hide, and toggle commands. It boosts the skill you are using; it does not award unrelated skills. Green-bar bonuses apply to eligible orb pickups after Mending, where enabled and permitted.</p>
    </details>
    <p class="note">WeekendXP is a separate plugin. The site's weekend schedule is Saturday and Sunday (Central time), with a scheduled 1.2× mcMMO XP boost. Check the in-game announcement for the current event; runtime timing has not been verified for this guide.</p>
  </section>
  <details class="guide-sources">
    <summary>About this guide and its sources</summary>
    <p>Reviewed October 12, 2026 (UTC). Skill ranks, advanced settings, recipes, and treasure tables were compared with the server's files. Implementation was checked against mcMMO 2.3.003-SNAPSHOT source at commit 058279c.</p>
    <p>The server uses Retro levels. A level number is an unlock, not a promise that a chance-based effect will happen every time. Player permissions, actual in-game behavior, and every touch/controller layout have not been play-tested. Use your skill command for your current stats.</p>
    <p>Crossbows, Tridents, Maces, and Spears have working passive skills in the checked source. Their unfinished super abilities are not listed as unlocks. Older videos and wiki pages may describe different abilities.</p>
    <ul>
      <li><a href="https://github.com/mcMMO-Dev/mcMMO/tree/058279c148a65bd708dc85067d3858f6adde1173">Version-pinned mcMMO source</a></li>
      <li><a href="https://github.com/mcMMO-Dev/mcMMO/blob/058279c148a65bd708dc85067d3858f6adde1173/src/main/resources/skillranks.yml">Skill unlock levels</a></li>
      <li><a href="https://github.com/mcMMO-Dev/mcMMO/blob/058279c148a65bd708dc85067d3858f6adde1173/src/main/java/com/gmail/nossr50/datatypes/player/McMMOPlayer.java#L1015">Active-ability timing</a></li>
      <li><a href="https://github.com/mcMMO-Dev/mcMMO/blob/058279c148a65bd708dc85067d3858f6adde1173/src/main/java/com/gmail/nossr50/party/ShareHandler.java#L32">Party XP sharing</a></li>
    </ul>
  </details>
  <details class="skill-notes"><summary>Watch the original mcMMO overview video</summary>
    <figure class="video"><div class="vwrap"><iframe src="https://www.youtube-nocookie.com/embed/AkNs7GlAZ-8" title="Tutorial - mcMMO Skills Walkthrough" loading="lazy" allow="encrypted-media; picture-in-picture; fullscreen" allowfullscreen></iframe></div><figcaption>A general overview of mcMMO<span class="vnote">This older video is not a reference for our current unlock levels. Use the skill cards above for this server's checked settings.</span></figcaption></figure>
  </details>
  <p class="guide-footer-link"><a href="#mcmmo-skills">Back to the skills</a></p>
</div>
'''

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    data = json.loads((ROOT / 'data/mcmmo-guide.json').read_text())
    generated = INTRO + '\n'.join(render_skill(s) for s in data['skills']) + OUTRO
    path = ROOT / 'index.html'
    existing = path.read_text()
    before, rest = existing.split(START, 1)
    _, after = rest.split(END, 1)
    result = before + START + '\n' + generated + '    ' + END + after
    for filename in ('style.css', 'guide.js'):
        digest = hashlib.sha256((ROOT / filename).read_bytes()).hexdigest()[:10]
        result = re.sub(re.escape(filename) + r'(?:\?v=[a-f0-9]+)?(?=")', filename + '?v=' + digest, result)
    if args.check:
        if existing != result:
            raise SystemExit('Guide is out of date. Run python3 scripts/build_guide.py')
        print('Guide is reproducible and up to date.')
    else:
        path.write_text(result)
        print(f'Rendered {len(data["skills"])} skills into index.html')

if __name__ == '__main__':
    main()
