"""Build the HTML decks from their markdown sources in decks/.

    python3 build.py            # rebuild every deck
    python3 build.py decks/build.md

The markdown syntax is described in decks/README.md.
"""
import base64
import html
import re
import shlex
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TEMPLATE = ROOT / "template"
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}


# --- inline -----------------------------------------------------------------

def inline(text):
    """Markdown inline -> HTML: `code`, **bold**, ==highlight==, bare & escaped; other HTML passes through."""
    out = []
    for i, part in enumerate(re.split(r"(`[^`]*`)", text)):
        if i % 2:
            out.append(f"<code>{html.escape(part[1:-1], quote=False)}</code>")
        else:
            part = re.sub(r"&(?!#?\w+;)", "&amp;", part)
            part = re.sub(r"==(.+?)==", r'<span class="g">\1</span>', part)
            out.append(re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", part))
    return "".join(out)


# --- attributes ---------------------------------------------------------------

ATTRS = re.compile(r"\s*\{([^{}]*)\}\s*$")


def parse_attrs(spec):
    """'.a -b #id style="x"' -> (add, remove, id, other attrs)."""
    add, remove, ident, other = [], [], None, []
    for token in shlex.split(spec):
        if token.startswith("."):
            add.append(token[1:])
        elif token.startswith("-"):
            remove.append(token[1:])
        elif token.startswith("#"):
            ident = token[1:]
        elif "=" in token:
            other.append(tuple(token.split("=", 1)))
        else:
            add.append(token)
    return add, remove, ident, other


def attr_html(classes, ident=None, other=()):
    parts = []
    if classes:
        parts.append(f'class="{" ".join(classes)}"')
    if ident:
        parts.append(f'id="{ident}"')
    parts += [f'{k}="{v}"' for k, v in other]
    return (" " + " ".join(parts)) if parts else ""


def element(tag, base, top, content, attrs=None, reveal=True):
    add, remove, ident, other = attrs or ([], [], None, [])
    classes = base + add + (["reveal"] if top and reveal else [])
    classes = [c for c in dict.fromkeys(classes) if c not in remove]
    return f"<{tag}{attr_html(classes, ident, other)}>{content}</{tag}>"


# --- raw HTML blocks ------------------------------------------------------------

class _Depth(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.depth = 0

    def handle_starttag(self, tag, attrs):
        if tag not in VOID:
            self.depth += 1

    def handle_endtag(self, tag):
        if tag not in VOID:
            self.depth -= 1


def take_raw(lines, i):
    """Collect lines from i until every tag opened is closed. Returns (block, next index)."""
    parser, start = _Depth(), i
    while i < len(lines):
        parser.feed(lines[i] + "\n")
        i += 1
        if parser.depth <= 0:
            break
    return "\n".join(lines[start:i]), i


# --- blocks ---------------------------------------------------------------------

CODE_MARKS = ((re.compile(r"\*\*(.+?)\*\*"), "k"), (re.compile(r"~~(.+?)~~"), "w"),
              (re.compile(r"(?<![*\w])\*([^*\s][^*]*?)\*(?![*\w])"), "s"))


def code_line(line):
    """One line inside a ``` fence: #/ // lines are headings; **key**, *highlight*, ~~warning~~ are coloured."""
    line = html.escape(line, quote=False)
    if line.startswith(("#", "//")):
        return f'<span class="p">{line}</span>'
    for pattern, cls in CODE_MARKS:
        line = pattern.sub(rf'<span class="{cls}">\1</span>', line)
    return line


TAG = re.compile(r"\[\[(?:([a-z]): )?(.+?)\]\]")
TAGS_ONLY = re.compile(r"^(\s*\[\[.+?\]\])+\s*$")
BLOCK_START = re.compile(r"^(\^ |#{1,3} |> |~ |- |:::|```|!! |!\[|@|<|\{.*\}$|\[\[)")
PHOTO = re.compile(r"!\[(.+?)\]\((.+?)\)")
IMAGE_TYPES = {".webp": "webp", ".jpg": "jpeg", ".jpeg": "jpeg", ".png": "png"}


def photo(caption, src):
    """A photo from template/assets/, inlined at build time like the fonts, with its caption below."""
    data = f"data:image/{IMAGE_TYPES[Path(src).suffix.lower()]};base64,{{{{base64:assets/{src}}}}}"
    return f'<img src="{data}" alt="{html.escape(caption)}"><figcaption>{inline(caption)}</figcaption>'


def tags(line):
    return "".join(f'<span class="tag{" " + c if c else ""}">{inline(t)}</span>' for c, t in TAG.findall(line))


DASHED = "repeating-linear-gradient(90deg,var(--text-3) 0 8px,transparent 8px 14px)"


def colour(item):
    """'[teal] rest' -> ('teal', 'rest'); no [..] -> (None, item)."""
    m = re.match(r"\[([\w-]+)\]\s+(.*)", item)
    return (m.group(1), m.group(2)) if m else (None, item)


def agenda_row(item):
    c, item = colour(item)
    t, n, d = item.split(" | ")
    return (f'<span class="t"><span class="dot" style="--c:var(--{c})"></span>{inline(t)}</span>'
            f'<span class="n">{inline(n)}</span><span class="d">{inline(d)}</span>')


def cp_step(item):
    c, item = colour(item)
    when, name, what = item.split(" | ")
    style = "" if not c else f' style="background:{DASHED if c == "dashed" else f"var(--{c})"}"'
    return (f'<div class="cp-step"><div class="bar"{style}></div><span class="when">{inline(when)}</span>'
            f'<span class="name">{inline(name)}</span><span class="what">{inline(what)}</span></div>')


def labelled(tag, cls):
    """Row of 'label | text [| [[tag]]]': label as written, text in a <span>, optional tag."""
    def row(item):
        label, text, *tag_line = item.split(" | ")
        end = tags(tag_line[0]) if tag_line else ""
        return f"<{tag}{cls}>{inline(label)}<span>{inline(text)}</span>{end}</{tag}>"
    return row


# ::: <component> containers whose content is a list, one row per item: (element, row renderer)
ROWS = {
    "agenda": ("div", agenda_row),
    "cp-track": ("div", cp_step),
    "layers": ("div", labelled("div", ' class="layer"')),
    "hazards": ("div", labelled("div", ' class="hz"')),
    "filelist": ("ul", labelled("li", "")),
}


def render_rows(classes, ident, other, items, pad):
    tag, row = ROWS[classes[0]]
    out = []
    if classes[0] == "agenda":
        bar = "".join(f'<span style="--c:var(--{colour(i)[0]})"></span>' for i in items)
        bar_classes = ["agenda-bar"] + classes[1:]
        out.append(f'{pad}<div{attr_html(bar_classes)} aria-hidden="true">{bar}</div>')
    out.append(f"{pad}<{tag}{attr_html(classes, ident, other)}>")
    out += [pad + "    " + row(i) for i in items]
    out.append(f"{pad}</{tag}>")
    return out


def split_attrs(text):
    m = ATTRS.search(text)
    if m and not text.lstrip().startswith("<"):
        return text[:m.start()], parse_attrs(m.group(1))
    return text, None


def render_blocks(lines, top, indent):
    """Render a list of markdown lines (one container's content) to indented HTML lines."""
    out, i, pending = [], 0, None
    pad = " " * indent

    def emit(s):
        out.append(pad + s)

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if not stripped:
            i += 1
            continue
        if stripped.startswith("```"):
            j = i + 1
            while j < len(lines) and lines[j].strip() != "```":
                j += 1
            spec = stripped[3:].strip()
            attrs = parse_attrs(spec[1:-1]) if spec.startswith("{") else pending
            code = "\n".join(code_line(l) for l in lines[i + 1:j])
            emit(element("pre", [], top, code, attrs))
            i, pending = j + 1, None
            continue
        if stripped.startswith("<"):
            block, i = take_raw(lines, i)
            out.append(block)
            continue
        if re.fullmatch(r"\{[^{}]*\}", stripped):
            pending = parse_attrs(stripped[1:-1])
            i += 1
            continue
        if stripped.startswith(":::"):
            spec = stripped[3:].strip()
            m = ATTRS.search(spec)
            if m:
                spec = spec[:m.start()] + " " + m.group(1)
            add, remove, ident, other = parse_attrs(spec)
            depth, j = 1, i + 1
            while j < len(lines):
                s = lines[j].strip()
                if s == ":::":
                    depth -= 1
                    if not depth:
                        break
                elif s.startswith(":::"):
                    depth += 1
                j += 1
            classes = [c for c in add if c not in remove]
            body = [l.strip() for l in lines[i + 1:j] if l.strip()]
            if classes and classes[0] in ROWS and all(l.startswith("- ") for l in body):
                out += render_rows(classes, ident, other, [l[2:] for l in body], pad)
                i, pending = j + 1, None
                continue
            emit(f"<div{attr_html(classes, ident, other)}>")
            out.extend(render_blocks(lines[i + 1:j], False, indent + 4))
            emit("</div>")
            i, pending = j + 1, None
            continue
        if stripped.startswith("- "):
            items = []
            while i < len(lines) and lines[i].strip().startswith("- "):
                items.append(lines[i].strip()[2:])
                i += 1
            checklist = all(item.startswith("[ ] ") for item in items)
            if checklist:
                lis = "".join(f'<li><span class="box"></span><p>{inline(t[4:])}</p></li>' for t in items)
            else:
                lis = "".join(f"<li>{inline(t)}</li>" for t in items)
            emit(element("ul", ["checklist" if checklist else "bullet-list"], top, lis, pending, reveal=False))
            pending = None
            continue
        text, attrs = split_attrs(stripped)
        if TAGS_ONLY.match(text):
            if attrs:   # attributes go on the line's single tag
                (c, t), = TAG.findall(text)
                emit(element("span", ["tag"] + ([c] if c else []), False, inline(t), attrs))
            else:
                emit(tags(text))
            i += 1
            continue
        if re.fullmatch(r"@[\w-]+", stripped):
            out.append((TEMPLATE / f"{stripped[1:]}.html").read_text().rstrip("\n"))
            i += 1
            continue

        # one-line text blocks; a paragraph runs until a blank line or another block
        text, attrs = split_attrs(stripped)
        attrs = attrs or pending
        pending = None
        i += 1
        if text.startswith("!! "):
            emit(element("span", ["cp-num"], False, inline(text[3:]), attrs))
            continue
        m = PHOTO.fullmatch(text)
        if m:
            emit(element("figure", ["photo"], top, photo(*m.groups()), attrs))
            continue
        for prefix, tag, base in (("^ ", "div", ["eyebrow"]), ("### ", "h3", []), ("## ", "h2", []),
                                  ("# ", "h1", []), ("> ", "p", ["lede"]), ("~ ", "p", ["small"])):
            if text.startswith(prefix):
                emit(element(tag, base, top, inline(text[len(prefix):]), attrs))
                break
        else:
            para = [text]
            while i < len(lines) and lines[i].strip() and not BLOCK_START.match(lines[i].strip()):
                para.append(lines[i].strip())
                i += 1
            emit(element("p", [], top, inline("\n".join(para)), attrs))
    return out


# --- slides ---------------------------------------------------------------------

def render_slide(header, body):
    add, remove, ident, other = parse_attrs(header[len("=== slide"):].strip())
    classes = ["slide"] + [c for c in add if c not in remove]
    notes = []
    for n, line in enumerate(body):
        if line.strip() == "Notes:":
            notes = [l.strip()[2:] for l in body[n + 1:] if l.strip().startswith("- ")]
            body = body[:n]
            break
    out = [f"<section{attr_html(classes, ident, other)}>"]
    if "bg-img" in classes:
        out.append('    <div class="bg-overlay"></div>')
    out.append('    <div class="slide-content">')
    out += render_blocks(body, True, 8)
    out.append("    </div>")
    if "title-slide" in classes:
        out.append("    " + (TEMPLATE / "brand-mark.html").read_text().strip())
    if notes:
        out.append('    <aside class="notes"><ul>' + "".join(f"<li>{inline(n)}</li>" for n in notes) + "</ul></aside>")
    out.append("</section>")
    return "\n".join(out)


def render_slides(markdown):
    lines = markdown.splitlines()
    out, prefix, i = [], [], 0
    while i < len(lines) and not lines[i].startswith("=== slide"):
        prefix.append(lines[i])
        i += 1
    while i < len(lines):
        header, i = lines[i], i + 1
        body = []
        while i < len(lines) and not lines[i].startswith("=== slide"):
            body.append(lines[i])
            i += 1
        # comments right before the next "=== slide" label that slide, not this one
        nxt = []
        while body and (not body[-1].strip() or body[-1].strip().startswith("<!--")):
            nxt.insert(0, body.pop())
        out += [l for l in prefix if l.strip()]
        out.append(render_slide(header, body))
        out.append("")
        prefix = nxt
    return "\n".join(out)


# --- whole deck -----------------------------------------------------------------

def front_matter(text):
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    meta = dict(line.split(":", 1) for line in m.group(1).splitlines() if ":" in line)
    return {k.strip(): v.strip() for k, v in meta.items()}, text[m.end():]


def build_deck(source):
    meta, body = front_matter(Path(source).read_text())
    extras = meta.get("extras", "")
    deck_css = (TEMPLATE / f"{extras}.css").read_text().rstrip("\n") if extras else ""
    deck_js = (TEMPLATE / f"{extras}.js").read_text().rstrip("\n") if extras else ""
    page = (TEMPLATE / "deck.html").read_text()
    for key, value in (("title", meta["title"]), ("deck_css", deck_css), ("deck_js", deck_js),
                       ("slides", render_slides(body).rstrip("\n"))):
        page = page.replace("{{%s}}" % key, value)
    # after the slides go in, so their photos are inlined too
    return re.sub(r"\{\{base64:([^}]+)\}\}",
                  lambda m: base64.b64encode((TEMPLATE / m.group(1)).read_bytes()).decode(), page)


def main(paths):
    for source in paths or sorted((ROOT / "decks").glob("*.md")):
        source = Path(source)
        if source.name == "README.md":
            continue
        meta, _ = front_matter(source.read_text())
        target = ROOT / meta["output"]
        target.write_text(build_deck(source))
        print(f"{source.relative_to(ROOT)} -> {target.relative_to(ROOT)}")


if __name__ == "__main__":
    main(sys.argv[1:])
