# AI workshop decks

Browser slide decks for an AI workshop, served by GitHub Pages from `main` (repo root). There is no build step: each deck is one self-contained HTML file, and a push to `main` republishes the site in about a minute.

Read this before changing anything. The goal is that every edit, by a person or an agent, matches what is already here.

## Files

| File | What it is |
|---|---|
| `index.html` | Landing page linking the decks. Small, no embedded assets. |
| `build.html` | The parking-app build brief: agenda, checkpoints, status board, demos. |
| `playbook.html` | "A way of working with AI": CLAUDE.md, spec, journal, commands, guards, habits. |
| `tools/fit-check.sh` | Checks every slide fits its viewport (4 sizes x 2 themes). Run it before every push. |
| `tools/fit-check.html` | The in-browser checker the script drives. |

## How the decks were made

They were generated with Claude Code using the `dt-slides` skill (Dynatrace Corporate 2026 style, from the internal AI knowledgebase repo, `plugins/dt-slides`), then edited by hand. The skill is not needed to edit them: everything it produced is already in the files. Use it only if you build a new deck from scratch, and then copy the head and controller of `build.html` so the decks stay identical in behaviour.

## Do not read the decks whole

`build.html` and `playbook.html` are about 800 KB each, almost all of it base64 fonts and images on a handful of lines. Find what you need with `grep -n` and read line ranges. Never paste the base64 lines into a prompt or a diff review.

- Slides start at `<!-- NN NAME -->` comments: `grep -n '<!-- ' build.html`.
- CSS sections start at `/* === NAME === */`: `grep -n '/\* === ' build.html`.

## Anatomy of a deck

In order inside each file:

1. `FONTS`: DTFlow `@font-face` rules as base64 data URIs (weights 100, 300, 500, 600, 700). Do not touch.
2. `THEME TOKENS`: every colour, as CSS variables on `:root` (dark) and `[data-theme="light"]`. The only place colours are defined.
3. `VIEWPORT BASE`: from the skill's `viewport-base.css`. Slides are exactly one screen tall; sizes use `clamp()`.
4. Component CSS (`BASE`, `TITLE`, `CHECKPOINT`, `STATUS BOARD`, `BRAND CHROME`, ...).
5. Slides: `<section class="slide">` > `<div class="slide-content">` plus `<aside class="notes">` for speaker notes.
6. `PRESENTATION CONTROLLER`: keyboard, nav dots, pager, theme toggle, notes panel, `?slide=N`.
7. `build.html` only: `STATUS BOARD` (5 teams x 5 checkpoints, saved in the presenting browser's localStorage).

## Style rules

- **Colours only through tokens**: `var(--teal)`, `--blue`, `--purple`, `--pink`, their `-text` variants, `--text`, `--text-2`, `--text-3`, `--card`, `--card-border`. Never a hex value in a slide or new CSS. Palette: teal `#49C2B3`, sky `#3BACF0`, blue `#1966FF`, purple `#5E28E5`, magenta `#8D1CDC`, pink `#C93FDB`, navy `#1A2440`. Nothing outside it.
- **Meaning of colours**: teal = done / build time / primary highlight; blue = in progress / info; purple = checkpoints; pink = need help / warnings. Keep it consistent with the status board.
- **Both themes must work.** Check every change in dark and light (press T).
- **Type**: DTFlow. Headings 500, body 300, emphasis (`<strong>`) 600. Code and labels use JetBrains Mono.
- **Logo and backgrounds**: the logo sits top-left (white) in dark and bottom-left (colour) in light; background images appear only on the first and last slide, only in dark. Handled by `BRAND CHROME`; do not add more.
- **One screen per slide, no scrolling.** At most: a heading plus 4-6 bullets, or up to 6 cards, or 8-10 lines of code. More content means a new slide.
- **Text**: plain English, short sentences. No emoji anywhere (use inline SVG for icons). No em or en dashes. Fake data only, no real names.

## Building blocks to reuse

Reuse these classes instead of writing new CSS:

- Layout: `cols-2`, `cols-3`, `cols-4`, `grid`, `cp-layout` (`cp-left` / `cp-right`), `meta-row`.
- Text: `eyebrow` (small mono label above a heading), `lede` (intro paragraph), `small`, highlights `.g` `.b` `.o`.
- Cards: `card` plus an accent border `accent-g` (teal), `accent-b` (blue), `accent-v` (purple), `accent-o` (pink).
- Tags: `tag`, `tag b`, `tag v`, `tag o` (same colour order as the accents).
- Lists: `checklist` (with `<span class="box"></span>`), `bullet-list`.
- Timeline: `agenda` + `agenda-bar` (the evening), `cp-track` + `cp-step` (checkpoint overview).
- Motion: `reveal` on a single element, `stagger` on a container whose children appear one by one.

The class names `g` / `v` / `o` predate the current palette (they meant green, violet, orange). They now map to teal, purple and pink. Keep using them; do not rename.

## Keeping the schedule consistent

Clock times appear in several places in `build.html`. When one changes, change all of them in the same commit:

- the agenda slide (`02 THE EVENING`) rows and the `agenda-bar` column widths (one `fr` per minute),
- the checkpoint overview (`cp-track`),
- each checkpoint slide's time tag,
- the pit stop, demos and closing slides,
- the speaker notes on those slides.

Find them with `grep -n -E '1[78]:[0-9]{2}' build.html`.

## Adding or moving a slide

- Copy the nearest similar slide and keep its structure.
- Inserting a slide shifts every later slide number, so `?slide=N` links shared earlier will point one slide off. Say so in the commit message.
- New teams or checkpoints on the board: change `StatusBoard.TEAMS` / `CHECKPOINTS` and the table header together. A size change resets saved board state, which is intended.

## Before you push

1. `tools/fit-check.sh` must print only `ok` lines and end with `sanity: planted overflow detected`. It needs Google Chrome and python3 (set `CHROME` if Chrome is not in `/Applications`).
2. Open the deck locally, step through the slides you touched in both themes, and open the notes panel (N).
3. No em or en dashes in added lines: `git diff | perl -CS -ne 'print if /^\+.*[\x{2013}\x{2014}]/'` must print nothing.
4. Commit messages say what changed and why. No AI co-author trailers or "generated with" footers.
