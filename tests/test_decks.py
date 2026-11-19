"""Acceptance test: every published deck is reproduced by building its markdown source.

Compares what a viewer gets, not bytes:
- slides: same elements, attributes and text, with whitespace normalised (exact inside <pre>)
- page chrome outside <main>: identical, except the contents of <style> and <script>
- <style> and <script>: the same lines, in any order
"""
import re
import unittest
from html.parser import HTMLParser
from pathlib import Path

import build

ROOT = Path(__file__).resolve().parent.parent
DECKS = {"build.html": "decks/build.md", "playbook.html": "decks/playbook.md"}
VOID = {"meta", "link", "br", "img", "input", "hr"}


class _Tree(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = ("#root", (), [])
        self.stack = [self.root]
        self.pre = 0

    def handle_starttag(self, tag, attrs):
        node = (tag, tuple(sorted((k, v or "") for k, v in attrs)), [])
        self.stack[-1][2].append(node)
        if tag in VOID:
            return
        self.stack.append(node)
        self.pre += tag == "pre"

    def handle_startendtag(self, tag, attrs):
        self.stack[-1][2].append((tag, tuple(sorted((k, v or "") for k, v in attrs)), []))

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        while len(self.stack) > 1:
            node = self.stack.pop()
            if node[0] == "pre":
                self.pre -= 1
            if node[0] == tag:
                break

    def handle_data(self, data):
        if not self.pre:
            data = re.sub(r"\s+", " ", data)
            if not data.strip():
                return
        self.stack[-1][2].append(("#text", data))


def slides(html):
    main = re.search(r"<main>(.*)</main>", html, re.S).group(1)
    tree = _Tree()
    tree.feed(main)
    return [n for n in tree.root[2] if n[0] == "section"]


def chrome(html):
    outside = re.sub(r"<main>.*</main>", "<main></main>", html, flags=re.S)
    return re.sub(r"<(style|script)>.*?</\1>", r"<\1></\1>", outside, flags=re.S)


def block_lines(html, tag):
    body = "\n".join(re.findall(rf"<{tag}>(.*?)</{tag}>", html, re.S))
    return sorted(line.rstrip() for line in body.splitlines() if line.strip())


class DecksMatchTheirMarkdown(unittest.TestCase):
    def test_each_deck_is_built_from_its_markdown(self):
        for page, source in DECKS.items():
            with self.subTest(page=page):
                expected = (ROOT / page).read_text()
                built = build.build_deck(ROOT / source)

                want, got = slides(expected), slides(built)
                self.assertEqual(len(got), len(want), "slide count")
                for i, (w, g) in enumerate(zip(want, got), 1):
                    self.assertEqual(g, w, f"slide {i}")
                self.assertEqual(chrome(built), chrome(expected), "page chrome")
                self.assertEqual(block_lines(built, "style"), block_lines(expected, "style"), "CSS lines")
                self.assertEqual(block_lines(built, "script"), block_lines(expected, "script"), "JS lines")

    def test_every_placeholder_is_filled(self):
        for source in DECKS.values():
            with self.subTest(source=source):
                self.assertEqual(re.findall(r"\{\{[^}]*\}\}", build.build_deck(ROOT / source)), [])


if __name__ == "__main__":
    unittest.main()
