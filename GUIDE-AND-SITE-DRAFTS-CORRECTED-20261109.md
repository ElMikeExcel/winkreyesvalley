# ExcelDetails 0.1.0 — Guide + website surface drafts (CORRECTED Nov 9, 2026, wrv-work-advance canon sweep)

Supersedes GUIDE-AND-SITE-DRAFTS.md for the publication pass. Corrections
verified against the installed plugin's source + rig proof — see
~/workspace/goals/family-minecraft-server-build/hidden_files/canon-details-guide-draft-20261109-0629.md.

Changes vs the original draft:
1. REMOVED the false sentence "Numbers are shown in the same x1000 scale
   as boss-fight numbers." The installed meter renders raw final damage
   (rig: 4.425 damage renders "4.4"); the x1000 display scale is a
   BossTrial 0.5.2 feature that is NOT installed yet (live is 0.4.1).
2. Bare /details is the STATUS view, not the toggle. Toggling is
   /details on, /details off, or /details toggle.
3. The segment is SHARED: it opens on the first tracked combat event
   from anyone, closes after ~8 s with no tracked combat from anyone,
   and /details clear discards the shared current segment for everyone
   (overall totals survive; /details reset wipes those too).
4. Healing-window caveat stated: v1 credits healing to the player it
   lands on, not to the healer (the game event names no healer).
5. Added the /dmeter alias and /details next (both real, plugin.yml +
   DetailsCommands).

## Guide knowledge chunk (corrected draft)

ExcelDetails is the server's live combat meter, modeled on Details!
Damage Meter. During a fight, a meter appears in your sidebar showing
damage done, damage taken, and healing, updating live. In an EliteMobs
party it tucks in directly under the party box; everywhere else it
stands alone. The fight segment is shared: it opens on the first hit
anyone lands and closes after about 8 seconds without combat. The
numbers are the real damage values, compacted as they grow (for
example 12.5k). Commands: /details (your current numbers and window),
/details on, /details off and /details toggle (turn the meter on or
off — your choice is remembered when you log out), /details window
taken (watch damage taken instead of damage done; damage and healing
are the other windows, and /details next cycles them), /details clear
(start a fresh segment — this clears the shared segment for everyone;
overall totals stay), and /dmeter works as a short alias. One v1
limit: the healing window credits healing to the player it lands on,
not to the healer, because the game does not name a healer for those
events. End-of-fight boss numbers still come from /bosstrial stats;
the meter is the live, in-the-moment view.

## Guide intent (draft, unchanged)

- Intent: details_meter — triggers: "damage meter", "details",
  "how much damage did I do", "dps meter", "combat meter",
  "/details", "damage taken meter", "healing meter".
- Answer: the knowledge chunk above.

## Website plugin-list line (corrected draft)

ExcelDetails 0.1.0 — a Details!-style live combat meter in the
sidebar: damage done, damage taken, and healing, updating live during
a fight, tucked under the EliteMobs party box in a party and standing
alone everywhere else. /details on and /details off control it; your
choice is remembered.

## Also flagged (parent pipeline lane, NOT edited here)

whatsnew-pipeline/registry/whatsnew.yml, entry
2026-11-09-exceldetails-meter (already LIVE in-game, staged for the
website): the command glosses repeat the loose phrasing — "/details —
Turns your combat meter on or off" (bare /details is status) and
"/details clear — Zeroes the meter" (clear discards the current
segment only; overall totals survive). Suggested registry glosses:
"/details — Show your meter numbers; /details on/off turns it on or
off" and "/details clear — Discards the current segment and starts a
fresh one". Registry is the generator source; the generated
changelog.yml / website files must be regenerated, never hand-edited.
