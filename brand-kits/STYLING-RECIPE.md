# Styling recipe: lofi to branded hifi

The repeatable procedure for re-skinning a signed-off lofi with a brand kit. Follow it in order. Steps 1 to 3 take minutes and get you most of the way; steps 4 to 6 are the real work.

Prerequisites: the lofi is signed off, and it follows `LOFI-TOKEN-CONTRACT.md`.

## 0. Set up

Work inside `BTL P1 Cursor/`, alongside the existing prototypes. The kits reference shared fonts and assets at `../../`, so a kit only resolves correctly from a page in that folder. Copy the lofi in and rename it to the hifi convention:

```
phase3-search-accom-fam-hifi.html
phase3-search-accom-bbw-hifi.html
```

Never edit the lofi in place. It is the signed-off record of what the client agreed.

## 1. Link the kit

**1b (BBW only):** swap the lofi's placeholder `.appbar` markup for the real BBW header block (copy it from `phase2-dining-extras-bbw-hifi.html` or the verify slice). The kit's appbar rules expect the logo image, nav and top bar. Family's placeholder header restyles cleanly as-is.

**1c:** if the lofi has a review rail, check its rules are scoped under `.rail` — unscoped `.seg`/`.seg-group`/`.stepper` get restyled by the kit. Also check the lofi doesn't reuse kit component names for different components (`.promo-banner` and `.sec-head` bit the P3 slice); rename or re-assert. Full collision list and fixes: `VERIFY-SLICE-FINDINGS.md`.

Add the stylesheet **after** the lofi's own `<style>` block:

```html
<style> /* the lofi's existing CSS, untouched for now */ </style>
<link rel="stylesheet" href="brand-kits/family/kit.css">
```

Order matters. The kit needs to win on the shell and chrome classes it shares with the lofi.

## 2. Delete the lofi `:root`

Remove the lofi's entire `:root` block. The kit now supplies all 14 role tokens. Do not merge the two, and do not keep "just the radius" — partial token blocks are how drift starts.

Open the page. Expect roughly 60% of the re-skin to be done: type, colour, the prototype shell, the header, the footer, buttons and any class the lofi shares with the kit. The BBW kit shares 35 class names with the P3 accom lofi, the Family kit 21.

## 3. Sweep the hardcoded values

Search the file for `#` and fix every literal colour that is not genuinely absolute. The P3 accom lofi has around 30 (`#3a3a3a`, `#ededed`, `#128100`, `#1f1f1f` and friends). Each becomes a `var()` reference. This step is quick and it removes the majority of the "looks nearly right but grubby" problem.

Leave alone: pure `#fff` / `#000` where the value is absolute, and anything inside a data-URI SVG.

Then check `--dark`. Wherever the lofi uses it as a background, make sure the text on top reads `var(--on-dark)` rather than an assumed white or black. This single fix prevents most contrast failures.

## 4. Polish against the gallery

Open the relevant `gallery.html` beside the page. Work component by component, top of the page down. For each one, either it matches a gallery component (adopt the gallery's markup and classes wholesale) or it does not (see step 5).

Do not eyeball-match. If a lofi card is doing roughly what a `dcard` does, use `dcard`. Adopting the class is faster than approximating it, and it means the component stays correct when the kit changes.

Give particular attention to:

- **Selected and added states.** These are the least transferable part of any re-skin. The Family kit maps `--dark` to black, so after linking, everything that used `--dark` reads as quiet monochrome. That is deliberate. Re-point true primary CTAs to `--accent` (rose) and selection borders and rings to `--selected` (gold), component by component. Check every one.
- **Price blocks.** Both brands treat price as a hero with a qualifier beneath. Match the gallery's hierarchy rather than the lofi's.
- **Scope tags (BBW).** Every priced extra needs one. Lofis routinely omit them.
- **Expanders open via a class, not a display override.** Family's `plan-more`, `drinks-more` and `xmas-more` animate with `grid-template-rows:0fr` and open with `.open`; BBW's `dc-more` toggles `display` with `.open`. Forcing `display:block` on the Family ones leaves the content invisible but still occupying space — a giant phantom gap.
- **Desktop components assume the full 1100px frame.** The horizontal bars (drinks, Christmas, BBW promo banner) crush below roughly 900px: fixed photo fractions and action widths squeeze the text column and fixed-height rows overflow. Keep desktop examples inside the standard device frame; never preview them in narrow columns and conclude the kit is broken.

## 5. New components

If the screen needs something the kit does not have, build it in the page first, get it right, then **move it into `kit.css` and add it to `gallery.html` before you move on.** Not at the end of the phase, not "when there's time".

This is the rule that decides whether the kits are still useful at Phase 5 or have quietly rotted. Every component that stays inline in a page is a component the next phase will rebuild slightly differently.

Where a new component is fiddly enough that CSS iteration is slower than drawing it, design it in Figma first and point Claude at the frame via the Figma MCP. Name and structure that frame properly, because it should survive to the developer hand-off rather than being thrown away.

## 6. Check before you share

- Both breakpoints: desktop and the 390px mobile frame. Toggle with the shell's segmented control.
- Contrast on anything you hand-tuned. Both kits carry a measured contrast table in a comment at the foot of `kit.css` — check against those numbers rather than guessing. The two known traps: Family's `--muted` drops to 3.74:1 on `--fill3`, and BBW's `--red` is 3.65:1 on `--bg`. Both are large-text-only.
- Keyboard: tab through the whole flow. Selected states need `aria-pressed` or `aria-checked`, disabled options need `aria-disabled` plus `tabindex="-1"`.
- Fonts actually loaded, not falling back. Neutraface and League Gothic both fail silently to a system face, which is easy to miss on a quick look.
- Console clean.

## 7. Portable build for hand-off

`_embed.py` inlines every font, icon and photo into one self-contained file for sharing with the client or the strategist. Point it at the new page and its kit:

```
SRC = phase3-search-accom-bbw-hifi.html
CSS = brand-kits/bbw/kit.css
```

Send the embed build, not the linked working file. Keep iterating on the linked version.

For user testing, send the embed plus a short note on what is real and what is faked. It saves a round of questions from the strategist.

## What not to do

- **Do not edit `app.css` or `app-bbw.css`.** They belong to the two shipped hifis. The kits are copies for exactly this reason.
- **Do not edit a kit to fix one screen.** Screen-specific overrides live in the screen. Only genuinely reusable changes go in the kit.
- **Do not merge the two kits.** The brands share 8 of 35 tokens and 22 of 90-plus classes. They are different design systems, and the contract plus the galleries are what keep them consistent in spirit.
