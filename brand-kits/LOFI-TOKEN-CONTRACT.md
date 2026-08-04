# Lofi token contract

The interface between a lofi prototype and a brand kit. Any lofi that styles itself **only** through the 14 role tokens below can be re-skinned as Family or BBW by linking one stylesheet.

Verified against the four current lofis (`phase3-search-accom-lofi.html`, `phase3-search-accom-lofi-sketch.html`, `phase3-group-status-explorations.html`, `phase4-extras-family-lofi.html`). All four already use exactly this vocabulary, so the contract describes existing practice rather than imposing something new.

## The 14 role tokens

| Token | Role | Lofi value | Notes |
|---|---|---|---|
| `--ink` | Primary text | `#2b2b2b` | Headings, body copy |
| `--ink2` | Secondary text | `#555` | Supporting copy, labels |
| `--muted` | Tertiary text | `#7a7a7a` | Metadata, hints. Fails AA small on white in lofi; kits fix this |
| `--line` | Light divider | `#cfcfcf` | Inner card rules, subtle separators |
| `--line2` | Medium border | `#a9a9a9` | Card outlines, input borders |
| `--line3` | Strong border | `#8a8a8a` | Emphasis outlines, active inputs |
| `--fill` | Subtle fill | `#f2f2f2` | Zebra rows, inset panels |
| `--fill2` | Deeper fill | `#e7e7e7` | Hover surfaces, image placeholders |
| `--fill3` | Deepest fill | `#dcdcdc` | Pressed states, halo rings |
| `--paper` | Component surface | `#fff` | Card and panel backgrounds |
| `--bg` | Page backdrop | `#9a9a9a` | Behind the device frame |
| `--dark` | Selected / primary action | `#2b2b2b` | Filled buttons **and** selection borders. See warning below |
| `--radius` | Corner radius | `10px` | Single radius step |
| `--font` | Body typeface | system stack | Kits swap to the brand face |

## The `--dark` problem

`--dark` carries two jobs at once: filled backgrounds (buttons, active pills) and selection colour (borders, inset rings). In the P3 accom lofi it appears 24 times split across both.

That is fine while everything is grey, but a brand kit cannot always satisfy both, and the two kits resolve it differently because the brands differ:

- **BBW maps `--dark` to yellow** `#ffd614` with `--on-dark` black. Yellow is BBW's dominant identity, so yellow-everywhere is the correct unpolished default.
- **Family maps `--dark` to black** `#000` with `--on-dark` white. Not rose. An audit of the P3 lofi found most `--dark` uses are pressed controls, badges and tooltips, and Family's own idiom for those is black (gold for selection borders, rose only for CTAs and radio dots). Rose works because it is scarce; mapping it onto `--dark` would splash it across everything. During polish, re-point true CTAs to `--accent` and selection borders to `--selected`.

Consequences:

1. **Every kit must expose `--on-dark`** — the text colour that is legible on `--dark`. Lofis should use `color:var(--on-dark)` on any `--dark` background rather than assuming `#fff`.
2. **Selection styling is a component-level refinement, not a token swap.** Expect to hand-tune selected states after the kit is linked. This is the single biggest source of manual work in a re-skin, so budget for it.
3. **On Family, primary CTAs need re-pointing to `--accent` during polish.** They are few and easy to find (`.btn.primary`, `.continue` equivalents), and the kit's own CTA classes already carry the correct rose.

New lofis should split the roles where practical: `--dark` for filled actions, and a separate `--selected` for selection colour. Kits already carry the values for both.

## Rules for authoring a new lofi

1. Declare the 14 tokens in one `:root` block at the top of the file, nothing else in it.
2. Reference colour, radius and type **only** through `var()`. No literal hex in component rules.
3. Two exceptions are allowed, because the kits override them anyway: pure `#fff` / `#000` where the value is genuinely absolute (a focus ring on a photo, an icon fill), and the prototype shell (`.stage`, `.toolbar`, `.frame`, `.seg`) which every kit already styles.
4. Reuse the established shell and chrome class names — `.stage`, `.toolbar`, `.frame`, `.frame-outer`, `.scroll`, `.appbar`, `.chrome-mid`, `.searchsum`, `.footer`, `.continue`, `.seg`, `.seg-group`, `.sr-only`. Both kits already style all of these, so you inherit the full prototype shell for free. The P3 accom lofi shares 35 class names with the BBW kit on this basis.
5. Add `--on-dark` alongside `--dark` and use it for text on filled surfaces.

## Known drift to fix when re-skinning

The current P3 accom lofi contains roughly 30 hardcoded hex values outside the token block (`#3a3a3a`, `#ededed`, `#128100`, `#1f1f1f` and similar). These survive the kit link and will look wrong against a brand palette. The styling recipe includes a sweep step for exactly this.
