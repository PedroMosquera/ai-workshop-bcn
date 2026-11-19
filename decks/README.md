# Deck sources

Each deck is one markdown file here. `build.py` turns it into the HTML page that GitHub Pages serves:

| Source | Builds |
|---|---|
| `decks/build.md` | `build.html` |
| `decks/playbook.md` | `playbook.html` |

Edit the `.md` and push. The `Build decks` workflow (`.github/workflows/build-decks.yml`) rebuilds the HTML, runs the tests and commits the result: on `main` GitHub Pages then publishes it, and on a pull request it comments links to preview the branch in a browser.

To see a change before pushing, build locally and open the `.html`:

```sh
python3 build.py                      # every deck
python3 build.py decks/build.md       # one deck
python3 -m unittest discover -t . -s tests   # checks each .html matches its .md
```

Python 3.9 or newer, no packages to install. Don't edit the `.html` by hand: the next build overwrites it.

## What lives where

- `decks/*.md`: slide content and speaker notes.
- `template/deck.html`: the shared page (CSS, navigation, theme, notes panel). `{{…}}` marks where each deck's parts go.
- `template/<extras>.css` / `.js`: CSS and JS only one deck needs (the status board, copy buttons). Picked with `extras:` in the front matter.
- `template/assets/`: fonts and background images, inlined at build time so each page works offline.
- `template/brand-mark.html`: the Dynatrace logo added to title slides.

## Syntax

The `# …` notes on the right explain each line; they are not part of the syntax.

```markdown
---
title: Parking App Build      # browser tab title
output: build.html            # page to write
extras: build                 # template/build.css + template/build.js
---

<!-- 02 THE MISSION -->       # optional label, kept as an HTML comment
=== slide                     # starts a slide

^ The mission                 # eyebrow label
## "Is there a spot for me tomorrow?"
> Today nobody knows…         # lede paragraph
~ Out of scope is not "never". # small print

::: cols-3 stagger            # a <div> with these classes, closed by :::
::: card accent-g
[[See]]                       # tag; [[b: text]] for a coloured one (g, b, o, v)
### See
Which spots are free for a given day.
:::
:::

Notes:                        # speaker notes (N key), one bullet each
- Three verbs. Every checkpoint maps to them.
```

| Markdown | HTML |
|---|---|
| `=== slide .title-slide .bg-img .bg-title` | title slide with background, overlay and logo (`.bg-closing` for the closing image) |
| `=== slide #board-slide style="--cp-color: var(--pink)"` | slide with an id or inline style |
| `^ text` | `<div class="eyebrow">` |
| `#`, `##`, `###` | `h1`, `h2`, `h3` |
| `> text` / `~ text` | `<p class="lede">` / `<p class="small">` |
| plain line | `<p>` |
| `- item` | `<ul class="bullet-list">` |
| `- [ ] item` | `<ul class="checklist">` with check boxes |
| `[[text]] [[o: text]]` on a line of their own | `<span class="tag">`, `<span class="tag o">` |
| `::: a b` … `:::` | `<div class="a b">`, can nest |
| `**bold**`, `` `code` ``, `==word==` | `<strong>`, `<code>`, teal highlight |
| `[[o: text]] {style="…"}` | a single tag with attributes |
| `@board` | the interactive status board (`template/board.html`) |
| `!! CP1` | the big checkpoint number (`<span class="cp-num">`) |
| ```` ``` ```` … ```` ``` ```` | a coloured code block, see below |

**Code blocks.** Write the content as-is between ```` ``` ```` lines. Lines starting with `#` or `//` are coloured as headings. Mark other words to colour them:

````markdown
``` {.reveal}
# spec.md
**Problem:** drivers don't know if a spot is free     # key, teal
*Given* spot 7 is booked for Thu                      # highlight, blue
~~Out of scope:~~ login, notifications                # warning, pink
```
````

**Animation.** Blocks directly on the slide (not inside a `:::`) get the `reveal` entry animation. Blocks inside a `:::` don't; add `stagger` to the container to animate its children one by one.

**Attributes.** Add `{…}` at the end of a line, or on the line before a list, to change classes or add attributes:

```markdown
### In scope {.g}                  # add a class
## Smaller title {-reveal}         # remove the default animation
> Lede inside a column {.reveal}
{.o}
- Login, SSO, user accounts        # <ul class="bullet-list o">
::: stagger {style="display:flex; flex-direction:column"}
```

**Row layouts.** These containers take a list, one row per item, with ` | ` between the fields:

```markdown
::: agenda reveal                        # also draws the coloured bar above it
- [teal] 17:25 | Sprint 1 | Spec and plan, no code yet
:::
::: cp-track stagger                     # [colour] or [dashed] only where the bar differs
- CP1 · 17:35 | Spec & plan | spec.md written, stack chosen
- [dashed] Pit stop · 18:20 | What we learned | …
:::
::: layers stagger
- `spec.md` | This task: what to build. | [[v: this task]]
:::
::: hazards stagger
- **Money** | anything that charges or pays
:::
::: filelist stagger
- `evidence.md` | No "done" without proof.
:::
```

Colours are the theme names: `teal`, `blue`, `purple`, `pink`, `text-3` (grey). The agenda bar's segment widths are set in `template/build.css` (`.agenda-bar`, one column per row, sized by duration): update that line when you add, remove or retime agenda rows.

**Plain HTML.** Any block that starts with `<` is copied as-is until its tags close, blank lines included. Inline HTML such as `<span class="hl-pink">word</span>` works inside any line.
