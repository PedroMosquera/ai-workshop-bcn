"""Unit tests: each piece of the deck markdown syntax renders to the HTML the decks use."""
import unittest

from build import render_slides


def slide(body, header="=== slide"):
    return render_slides(f"{header}\n\n{body}\n")


def flat(html):
    return "".join(line.strip() for line in html.splitlines())


class SlideMarkdown(unittest.TestCase):
    def assertRenders(self, body, inner, header="=== slide", section='<section class="slide">'):
        expected = f'{section}<div class="slide-content">{inner}</div></section>'
        self.assertEqual(flat(slide(body, header)), expected)

    def test_top_level_text_blocks_reveal(self):
        self.assertRenders(
            "^ The mission\n\n# Big\n\n## \"Title\"\n\n> Lede text\n\n~ Small print",
            '<div class="eyebrow reveal">The mission</div><h1 class="reveal">Big</h1>'
            '<h2 class="reveal">"Title"</h2><p class="lede reveal">Lede text</p>'
            '<p class="small reveal">Small print</p>',
        )

    def test_blocks_inside_a_container_do_not_reveal(self):
        self.assertRenders(
            "::: card accent-g\n### See\nWhich spots are free.\n> Lede\n:::",
            '<div class="card accent-g"><h3>See</h3><p>Which spots are free.</p><p class="lede">Lede</p></div>',
        )

    def test_containers_nest(self):
        self.assertRenders(
            "::: cols-2 stagger\n::: card\n### A\n:::\n::: card\n### B\n:::\n:::",
            '<div class="cols-2 stagger"><div class="card"><h3>A</h3></div><div class="card"><h3>B</h3></div></div>',
        )

    def test_attributes_add_and_remove_classes(self):
        self.assertRenders(
            '::: cols-2\n### In scope {.g}\n> Lede {.reveal}\n:::\n\n## Plain {-reveal style="font-size:2rem"}',
            '<div class="cols-2"><h3 class="g">In scope</h3><p class="lede reveal">Lede</p></div>'
            '<h2 style="font-size:2rem">Plain</h2>',
        )

    def test_container_attributes(self):
        self.assertRenders(
            '::: stagger {style="display:flex; gap:1rem"}\n### A\n:::',
            '<div class="stagger" style="display:flex; gap:1rem"><h3>A</h3></div>',
        )

    def test_attribute_line_applies_to_the_next_block(self):
        self.assertRenders(
            "{.o}\n- Login\n- Email",
            '<ul class="bullet-list o"><li>Login</li><li>Email</li></ul>',
        )

    def test_lists_and_checklists(self):
        self.assertRenders(
            "- One\n- Two\n\n- [ ] Check `spec.md`",
            '<ul class="bullet-list"><li>One</li><li>Two</li></ul>'
            '<ul class="checklist"><li><span class="box"></span><p>Check <code>spec.md</code></p></li></ul>',
        )

    def test_tag_lines(self):
        self.assertRenders(
            "::: card\n[[Any stack]]\n:::\n\n::: meta-row reveal\n[[5 checkpoints]] [[b: 17:00]]\n:::",
            '<div class="card"><span class="tag">Any stack</span></div>'
            '<div class="meta-row reveal"><span class="tag">5 checkpoints</span><span class="tag b">17:00</span></div>',
        )

    def test_inline_markup(self):
        self.assertRenders(
            "::: card\nRun **this** & `<name>` with <span class=\"g\">care</span> &amp; more.\n:::",
            '<div class="card"><p>Run <strong>this</strong> &amp; <code>&lt;name&gt;</code> '
            'with <span class="g">care</span> &amp; more.</p></div>',
        )

    def test_raw_html_block_is_kept_verbatim_including_blank_lines(self):
        raw = '<pre class="reveal"><span class="p"># spec</span>\n\nline two</pre>'
        html = slide(raw)
        self.assertIn("\n" + raw + "\n", html)

    def test_code_fence_colours_headings_and_marked_words(self):
        fence = ("``` {.reveal}\n# spec.md\n**Run:**  npm run dev   **Test:** npm test\n\n"
                 "*Given* a & <b>\n~~Out of scope:~~ login\n// settings.json\n  plain *(line)\n```")
        self.assertIn(
            '<pre class="reveal"><span class="p"># spec.md</span>\n'
            '<span class="k">Run:</span>  npm run dev   <span class="k">Test:</span> npm test\n\n'
            '<span class="s">Given</span> a &amp; &lt;b&gt;\n<span class="w">Out of scope:</span> login\n'
            '<span class="p">// settings.json</span>\n  plain *(line)</pre>',
            slide(fence))

    def test_code_fence_without_attributes_reveals_at_top_level(self):
        self.assertIn('<pre class="reveal">x</pre>', slide("```\nx\n```"))
        self.assertIn('<pre>x</pre>', slide("::: cols-2\n```\nx\n```\n:::"))

    def test_checkpoint_number(self):
        self.assertRenders(
            "::: cp-left reveal\n!! CP1\n## Title\n:::",
            '<div class="cp-left reveal"><span class="cp-num">CP1</span><h2>Title</h2></div>',
        )

    def test_agenda_rows_also_build_the_coloured_bar(self):
        self.assertRenders(
            "::: agenda reveal\n- [teal] 17:25 | Sprint 1 | Spec & plan\n- [blue] 18:45 | Demos | 2 minutes\n:::",
            '<div class="agenda-bar reveal" aria-hidden="true"><span style="--c:var(--teal)"></span>'
            '<span style="--c:var(--blue)"></span></div>'
            '<div class="agenda reveal"><span class="t"><span class="dot" style="--c:var(--teal)"></span>17:25</span>'
            '<span class="n">Sprint 1</span><span class="d">Spec &amp; plan</span>'
            '<span class="t"><span class="dot" style="--c:var(--blue)"></span>18:45</span>'
            '<span class="n">Demos</span><span class="d">2 minutes</span></div>',
        )

    def test_checkpoint_track_rows(self):
        self.assertRenders(
            "::: cp-track stagger\n- CP1 · 17:40 | Spec | written\n- [pink] CP4 | Rules | hold\n"
            "- [dashed] Pit stop | Learn | refill\n:::",
            '<div class="cp-track stagger">'
            '<div class="cp-step"><div class="bar"></div><span class="when">CP1 · 17:40</span>'
            '<span class="name">Spec</span><span class="what">written</span></div>'
            '<div class="cp-step"><div class="bar" style="background:var(--pink)"></div><span class="when">CP4</span>'
            '<span class="name">Rules</span><span class="what">hold</span></div>'
            '<div class="cp-step"><div class="bar" style="background:repeating-linear-gradient(90deg,var(--text-3) '
            '0 8px,transparent 8px 14px)"></div><span class="when">Pit stop</span>'
            '<span class="name">Learn</span><span class="what">refill</span></div></div>',
        )

    def test_layers_hazards_and_file_list_rows(self):
        self.assertRenders(
            "::: layers stagger\n- `spec.md` | This task, like `/bug`. | [[v: this task]]\n:::\n\n"
            "::: hazards stagger\n- **Money** | anything that pays\n:::\n\n"
            "::: filelist stagger\n- `evidence.md` | No \"done\" without proof.\n:::",
            '<div class="layers stagger"><div class="layer"><code>spec.md</code>'
            '<span>This task, like <code>/bug</code>.</span><span class="tag v">this task</span></div></div>'
            '<div class="hazards stagger"><div class="hz"><strong>Money</strong><span>anything that pays</span></div></div>'
            '<ul class="filelist stagger"><li><code>evidence.md</code><span>No "done" without proof.</span></li></ul>',
        )

    def test_tag_line_attributes(self):
        self.assertRenders(
            '::: card\n[[o: tips (next)]] {style="margin-top:auto"}\n:::',
            '<div class="card"><span class="tag o" style="margin-top:auto">tips (next)</span></div>',
        )

    def test_highlight(self):
        self.assertRenders("# The ==parking== app.", '<h1 class="reveal">The <span class="g">parking</span> app.</h1>')

    def test_partial_from_the_template(self):
        html = slide("@board")
        self.assertIn('<table class="board"', html)
        self.assertIn('<button id="boardReset"', html)

    def test_slide_header_attributes(self):
        self.assertRenders("## Hi", '<h2 class="reveal">Hi</h2>',
                           header='=== slide #board-slide style="--cp-color: var(--teal)"',
                           section='<section class="slide" id="board-slide" style="--cp-color: var(--teal)">')

    def test_title_slide_gets_overlay_and_brand_mark(self):
        html = flat(slide("# Go", header="=== slide .title-slide .bg-img .bg-title"))
        self.assertTrue(html.startswith(
            '<section class="slide title-slide bg-img bg-title"><div class="bg-overlay"></div>'
            '<div class="slide-content"><h1 class="reveal">Go</h1></div><div class="brand-mark">'))

    def test_notes(self):
        html = flat(slide("## Hi\n\nNotes:\n- First **note**\n- Second"))
        self.assertTrue(html.endswith(
            '</div><aside class="notes"><ul><li>First <strong>note</strong></li><li>Second</li></ul></aside></section>'))

    def test_photo_is_embedded_with_its_caption(self):
        self.assertRenders(
            "::: photos\n![Motorbikes take car bays](photos/bikes.webp)\n:::",
            '<div class="photos"><figure class="photo">'
            '<img src="data:image/webp;base64,{{base64:assets/photos/bikes.webp}}" alt="Motorbikes take car bays">'
            '<figcaption>Motorbikes take car bays</figcaption></figure></div>',
        )

    def test_photo_at_top_level_reveals(self):
        self.assertRenders(
            "![Level -3](photos/level.jpg)",
            '<figure class="photo reveal"><img src="data:image/jpeg;base64,{{base64:assets/photos/level.jpg}}" '
            'alt="Level -3"><figcaption>Level -3</figcaption></figure>',
        )

    def test_svg_logo_is_embedded(self):
        self.assertRenders(
            "![Bluebox](photos/bluebox.svg) {.logo}",
            '<figure class="photo logo reveal"><img src="data:image/svg+xml;base64,{{base64:assets/photos/bluebox.svg}}" '
            'alt="Bluebox"><figcaption>Bluebox</figcaption></figure>',
        )

    def test_comments_between_slides_are_kept(self):
        html = render_slides("<!-- 01 TITLE -->\n=== slide\n\n## A\n\n<!-- 02 NEXT -->\n=== slide\n\n## B\n")
        self.assertEqual(html.count("<section"), 2)
        self.assertLess(html.index("<!-- 02 NEXT -->"), html.index("<h2 class=\"reveal\">B"))
        self.assertGreater(html.index("<!-- 02 NEXT -->"), html.index("</section>"))


if __name__ == "__main__":
    unittest.main()
