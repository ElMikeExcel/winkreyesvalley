#!/usr/bin/env python3
"""Render the checked-in mcMMO data into the existing static page (no packages)."""
import argparse
import hashlib
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
START, END = '<!-- MCMO_SKILL_CARDS_START -->', '<!-- MCMO_SKILL_CARDS_END -->'

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

def render_page(existing, data):
    """Update only skill cards; preserve hand-maintained current instructions."""
    if existing.count(START) != 1 or existing.count(END) != 1:
        raise ValueError('Expected exactly one pair of skill-card markers')
    before, rest = existing.split(START, 1)
    _, after = rest.split(END, 1)
    generated = '\n'.join(render_skill(skill) for skill in data['skills'])
    return before + START + '\n' + generated + '\n' + END + after


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    data = json.loads((ROOT / 'data/mcmmo-guide.json').read_text())
    path = ROOT / 'index.html'
    existing = path.read_text()
    result = render_page(existing, data)
    if args.check:
        if existing != result:
            raise SystemExit('Skill cards are out of date. Review data then run python3 scripts/build_guide.py')
        print('Skill cards are reproducible; surrounding instructions preserved.')
    else:
        path.write_text(result)
        print(f'Rendered {len(data["skills"])} skill cards only')

if __name__ == '__main__':
    main()
