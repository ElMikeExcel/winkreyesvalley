# Wink Reyes Valley

The existing family Minecraft website, hosted with GitHub Pages. This is a plain static site: no package install, framework, or build service is needed to serve it.

## Edit the mcMMO guide

- Edit player-facing facts in `data/mcmmo-guide.json`.
- Edit introduction, commands, party help, and current XP notices directly in `index.html`. Edit only card rendering in `scripts/build_guide.py`.
- Run `python3 scripts/build_guide.py` to update the marked section of `index.html`.
- Keep the generated `index.html` committed so all skills work without JavaScript.
- The generator updates only the `MCMO_SKILL_CARDS_START` / `MCMO_SKILL_CARDS_END` region. It must preserve all surrounding current instructions and asset URLs. Version CSS/JavaScript URLs separately when changing those assets.
- `guide.js` adds filtering, expandable controls, tab keyboard navigation, and skill permalinks. Native `<details>` elements still work without it.
- `style.css` preserves the site's existing green/brown design and adds responsive guide styles.

Use the checked server's Retro levels. Do not substitute levels from a newer wiki, infer live settings from bundled defaults, or publish private server configuration exports. Keep `unlockLabel` for abilities with additional gates; it may intentionally differ from the first configured rank. Recheck the settings and source version when mcMMO changes. The guide describes configured behavior; actual permissions and in-game behavior still need player testing.

## Update the site assistant

- After editing `index.html` or `questions.html`, run `python3 scripts/build_ai_knowledge.py` to rebuild `ai-knowledge.json` (the chunks the site assistant reads).
- Commit the regenerated `ai-knowledge.json` with the page change.

## Checks

```sh
python3 scripts/build_guide.py --check
python3 -m unittest discover -s tests -v
node --check guide.js
git diff --check
```

For a local browser preview:

```sh
python3 -m http.server 8767 --bind 127.0.0.1
```

Open `http://127.0.0.1:8767/`. The development-only fixture at `/tests/responsive.html` previews 320, 390, 768, and 1188-pixel iframe widths, and a no-JavaScript mode. It is a layout check, not an actual mobile-device or touch-input emulator.

Before publication, check search/no-results/reset, category filtering, repeated open/close actions, keyboard tab navigation, direct `#mcmmo-mining` links, browser Back/Forward, and the no-script fallback. Check the original server address, joining instructions, and other plugin tabs too.

Publishing, merging, and server configuration changes are separate actions. Editing this website does not update Minecraft plugins or server settings.

## Keep instructions and the change log current

Every plugin added or edited needs player instructions on this website and maintained instructions in its GitHub source repository. Link the relevant source instructions from the guide. For a prepared build, label the instructions as a preview until installation and runtime behavior are verified; never list it as an installed plugin early.

Record actual website and server changes in the existing change log, newest first, using the date in America/Chicago. Preserve earlier entries. When a feature is removed, update its current instructions and installed-plugin listing as well as the change log. Do not publish private backups, access details, or server configuration exports.
