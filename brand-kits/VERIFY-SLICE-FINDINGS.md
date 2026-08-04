# Verify slice findings — P3 accom, both kits

Source: `phase3-search-accom-lofi.html` styled as `phase3-search-accom-fam-hifi-slice.html` and `phase3-search-accom-bbw-hifi-slice.html` using only the kits plus the recipe. Every manual intervention is logged here with a verdict: **kit** (folded into the kit), **recipe** (added to the procedure), or **screen** (stays local, expected polish).

## What the kits got for free

Steps 1 to 3 of the recipe (link kit, delete `:root`, sweep hex) rethemed the majority of both slices with no component work: all text, fills, lines and surfaces; the footer, save/continue, chrome-mid and search summary via shared shell classes; BBW's entire dark inversion including cards, since the lofi's `--paper` surfaces map to #181818; and the whole `--dark` economy (24 uses) via the black/yellow defaults. The token contract holds.

## Findings

**1. Shell class collision: the review rail.** The lofi rail's `.seg`/`.seg-group` are also kit toolbar classes, and the kit loads later, so the dark rail controls get restyled. Fixed by scoping the rail rules under `.rail`. Verdict: **recipe** — new lofis should scope all rail rules under `.rail` from the start.

**2. Component class collision: `.promo-banner` and `.sec-head` (BBW).** The BBW kit already owns both names for different components (the eat-3-pay-2 banner, the League Gothic section label), and flattens the lofi's promo strip and category disclosure rows. Re-asserted the lofi layout in the slice override block. Verdict: **screen** for the slice, but at the full styling pass these lofi components should be renamed (`.p3-promo`, `.cat-head`) or adopted into the kit under new names. Same risk class: `.price`, `.stepper`, `.btn`, `.desc`, `.body` — these collided benignly here (the kit's version was the desired one) but check them on every new screen.

**3. `--on-dark` was missing from 14 rules.** The lofi hardcoded `color:#fff` on every `--dark` surface. Harmless on Family (black) but breaks BBW (yellow). One systematic sweep fixed both slices. Verdict: **contract** already mandates it; the sweep is now the concrete recipe step 3b.

**4. `--font-display` gap.** BBW headings need League Gothic; the lofi had no display-face token. Added `--font-display` alias to the Family kit (maps to `--font`); BBW kit already had it. Verdict: **kit** (done). New lofis should put display headings on `var(--font-display)`.

**5. Family selection polish is real but bounded.** As predicted by the contract, selected states needed re-pointing from black to Sunshine gold: 5 rules (tiles, arrangement tiles, room cards, ledger active, current party). Progress/confirmation markers re-pointed to Bright Rose: 2 rules. Primary CTAs to rose: 3 rules. Roughly 10 rules per screen is the expected Family polish budget. Verdict: **screen** — correct per-screen work, not kit changes, because which state means "selected" vs "confirmed" vs "primary" is a per-component judgement.

**6. BBW polish budget was smaller** (~8 rules), mostly display type and the two collisions. The yellow `--dark` default did the selection work automatically. Verdict: **screen**.

**7. BBW appbar needs a markup swap, not CSS.** The kit's `.appbar` rules expect the real brand header (logo image, nav, top bar). Swapped in the markup from the BBW hifi. Family's placeholder header restyles cleanly without changes. Verdict: **recipe** — BBW re-skins swap the appbar markup as step 1b.

**8. Not yet done, deliberately.** The slices retheme the lofi's own components rather than adopting kit component markup (recipe step 4's full form). That adoption pass is the real P3 styling work; the slice proves the foundations under it are sound.

## Verdict on the kits

Both kits pass. No kit CSS needed changing beyond the `--font-display` addition. The per-screen override budget is roughly 10 rules for Family, 8 for BBW, plus one markup swap for the BBW header — small enough to confirm the brand-kit approach is the right economics for the full P3 pass.
