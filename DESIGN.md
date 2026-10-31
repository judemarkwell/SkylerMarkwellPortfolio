# Design

Visual system for skylermarkwell's portfolio. Product truth lives in `PRODUCT.md`; this file records how it looks and moves.

## Direction

Dealt by taste-skill (`.taste-skill/direction.json`): **Type and nothing else**, seed 1492563424, palette **Orange, sky, lime**, type **Hanken Grotesk**, motion **Colour by chapter**.

**Idea:** Skyler's sentence frames ("I can ___.") become the page's headline device. Her materials are built so a learner can finish that sentence; the site lets the visitor finish it too.

**Live thing:** the "I can ___" frame on the home page. Choosing an ending (ask for a break, cite evidence, talk to my child's teacher…) names who that learner is and lifts the sheet on the desk that was made for it.

**Signature surface:** the desk. Her work is paper, so the Work section is a calm tabletop of tilted sheets that lift on hover/focus and travel into their own page with a cross-document View Transition (prototype: `prototypes/desk/`).

## Deliberate departures from the dealt sheet

- **Shadows on the desk sheets.** House rule bans shadows at rest. The sheets are physical paper on a surface, and the lift is the interaction the client approved, so they keep a layered paper shadow. Nothing else on the site has a shadow.
- **Desk ground.** The desk is a pale tint of the sky field (`--desk`), quieter than the chapter colours, so her already-colourful materials stay the loudest thing in that section (client: "whimsical and vibrant around the work, calm desk under it").
- **Contact section dropped;** the footer (email as headline) does that job.
- **Ledger without hover preview.** Below the desk, every piece is listed in a plain ledger; the desk already shows the pictures.
- **Imagery.** Her own materials and photos are the only pictures (17 pieces, 30+ previews, 7 photos, one 4-second classroom loop). No stock photographs.

## Client decisions (Oct 30 notes)

- Names inside her own documents (e.g. "Mrs. Garr" in the ACCESS FAQ) and on the Grateful board leaves are shown as they are.
- "Why I made it" notes appear only when Skyler has written one (`why:` in the piece file; prompts listed in WHY-I-MADE-IT.md).
- Every piece has a real PDF download (`npm run downloads`). The transcript is published with the student ID and date of birth removed and flattened to images.
- "By definition" section on the home page: her definition sentence, each highlighted term linked to its evidence, in the four chapter colours.

## Spanish version

- Every page exists in English and Spanish (`/es/...`). Pages are shared views in `src/views/` that take `lang`; strings use `t(en, es)` from `src/lib/i18n.ts`.
- Work pieces: Spanish text lives in `src/content/work-es/` and is laid over the English entry (layout, order, previews and downloads stay shared). Her documents themselves stay in the language she used them in.
- The EN / ES switch sits in the header and goes to the same page in the other language. On phones under 520px, "Email me" moves into the menu so the switch always fits.

## Definition terms

Each highlighted term is underlined with a down arrow that nudges twice on load; clicking glides to its card and flashes it. Evidence links are black pill buttons with an arrow.

## Snapshots carousel

On the home page between "Finish the sentence" and the desk: a scroll-snap carousel of photos of Skyler and her proudest moments. Swipe on phones; arrows, dots and Pause always present; it auto-advances only while visible and not being used, never under reduced motion.

## Photo rules

- Student faces are always blurred (YuNet face detection plus manual boxes, checked by eye on every photo). Skyler and adult staff stay clear.
- Student names are removed before resizing: certificates, the We're Multilingual banner and signed posters get `blurRects`; the classroom loop is cut to its first 4.3 seconds and cropped on the left, before chairs with name cards and a wall of photos come into view.
- The loop plays muted, pauses off-screen, does not autoplay under reduced motion, and always has a visible Pause control.

## Tokens

| Role | Value | Use |
| --- | --- | --- |
| `--paper` | `#f1f2f0` | Hero upper field, detail pages |
| `--orange` | `#ff8126` | Chapter 1: hero lower field, intro |
| `--sky` | `#4db3ff` | Chapter 2 field (desk header band) |
| `--desk` | `#cfe8fb` | The desk surface |
| `--lime` | `#c5f53d` | Chapter 4: about, footer |
| `--night` | `#161615` / ink `#f2f2f2` | The one dark band: "What I design" poster list |
| `--ink` | `#111111` | Text on every light field |
| `--muted` | `#3d3a36` | Secondary text on light fields |
| `--accent` | `#de194b` | Crimson: primary action per field, hover ink in the poster list |

Type: Hanken Grotesk variable, self-hosted (Fontsource). Display weight 500, tracking -0.05em, leading 0.9, sentence case. Body 400, leading 1.45. Steps: small 13–14px, body 17–19px, lead 20–26px, head 32–64px, display 9.5vw/15vw.

Shape: one radius (`2px` on paper, `999px` on the button), one button style (solid crimson rectangle with white text), equal outer margins `clamp(20px, 4vw, 56px)`.

## Rules

- No eyebrows, no uppercase micro-labels, no monospace, no 01/02/03 numbering, no hairline rules, no gradients.
- Every heading two lines or fewer at every width.
- Header: one solid paper-coloured bar with ink text on every page, gaining a soft shadow once the page scrolls (client: the menu blended into content when it took each chapter's colour). Sections enter once with a 60–90ms stagger (rise 24px + opacity), never hidden if script fails. Every control has hover, press and focus feedback. All travel drops under `prefers-reduced-motion`.
- Accessibility: WCAG 2.2 AA; every sheet is an ordinary link; previews always come with real text.
