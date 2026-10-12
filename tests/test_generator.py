"""
Smoke tests for the generator.

Standard library only — run them with:

    python -m unittest discover tests

They cover the things that quietly break a published vault: the global ayah
numbering the CDN depends on, the note filename format the site's links are
built from, and the promise that hand-written sections survive a rebuild.
"""

import re
import tempfile
import unittest
from pathlib import Path

import config
import quranConnections as connections
from tadabbur import (asma_notes, assets, audio, ayah_notes, data, explore,
                      layout, notes, personalities, surah_index, themes)


class GlobalAyahNumbering(unittest.TestCase):
    """The CDN addresses ayaat 1–6236; a shift here silently mismatches audio."""

    def test_known_landmarks(self):
        self.assertEqual(audio.global_ayah(1, 1), 1)
        self.assertEqual(audio.global_ayah(1, 7), 7)
        self.assertEqual(audio.global_ayah(2, 1), 8)
        self.assertEqual(audio.global_ayah(2, 255), 262)
        self.assertEqual(audio.global_ayah(114, 6), 6236)

    def test_covers_every_ayah_exactly_once(self):
        seen = [
            audio.global_ayah(surah, ayah)
            for surah, count in enumerate(audio.AYAH_COUNTS, 1)
            for ayah in range(1, count + 1)
        ]
        self.assertEqual(seen, list(range(1, 6237)))

    def test_counts_agree_with_chapter_data(self):
        for surah in data.SURAHS.values():
            self.assertEqual(
                audio.AYAH_COUNTS[surah.number - 1],
                surah.total_ayaat,
                f"ayah count mismatch for surah {surah.number}",
            )


class AudioModes(unittest.TestCase):
    def test_api_url_uses_global_number(self):
        config.AUDIO_MODE = "api"
        self.assertIn("/262.mp3", audio.audio_url(2, 255))

    def test_local_layouts(self):
        config.AUDIO_LOCAL_LAYOUT = "flat"
        self.assertEqual(audio.local_filename(2, 255), "002255.mp3")
        config.AUDIO_LOCAL_LAYOUT = "nested"
        self.assertEqual(audio.local_filename(2, 255), "002/255.mp3")

    def tearDown(self):
        config.AUDIO_MODE = "api"
        config.AUDIO_LOCAL_LAYOUT = "flat"


class Configuration(unittest.TestCase):
    def test_rejects_unknown_audio_mode(self):
        config.AUDIO_MODE = "carrier-pigeon"
        with self.assertRaises(config.ConfigError):
            config.validate()

    def test_r2_requires_a_base_url(self):
        config.AUDIO_MODE, config.AUDIO_R2_BASE_URL = "r2", ""
        with self.assertRaises(config.ConfigError):
            config.validate()

    def tearDown(self):
        config.AUDIO_MODE = "api"


class NoteFilenames(unittest.TestCase):
    """The published site links to these names; the format is load-bearing."""

    def test_ayah_note_name(self):
        self.assertEqual(data.SURAHS[2].note_name(255), "2_255")

    def test_wikilink_round_trip(self):
        self.assertEqual(data.wikilink(2, 255), "[[2_255]]")

    def test_ayah_display_name(self):
        self.assertEqual(data.SURAHS[2].display_name(255), "2_255: The Cow البقرة")

    def test_folder_name_has_no_arabic(self):
        self.assertEqual(data.SURAHS[2].folder_name, "2 - The Cow")

    def test_surah_folder_sits_under_the_quran(self):
        self.assertEqual(data.SURAHS[2].folder, "The Quran/2 - The Cow")
        self.assertEqual(data.SURAHS[2].index_path, "The Quran/2 - The Cow/index")


class PersonalSectionSurvival(unittest.TestCase):
    """Every note type must carry the reader's own writing across a rebuild."""

    def setUp(self):
        self.folder = Path(tempfile.mkdtemp())

    def _rebuild_keeps(self, filename, generated, default):
        notes.write_note(self.folder, filename, generated, default)

        note = self.folder / filename
        note.write_text(note.read_text(encoding="utf-8") + "\nMY OWN WORDS\n",
                        encoding="utf-8")

        notes.write_note(self.folder, filename, generated, default)
        return note.read_text(encoding="utf-8")

    def test_ayah_note(self):
        surah = data.SURAHS[2]
        generated = ayah_notes.build(
            surah, 255,
            {"arabic": "a", "urdu": "u", "english": "e", "tafsir": "t", "tazkirul": "z"},
        )
        self.assertIn("MY OWN WORDS",
                      self._rebuild_keeps("ayah.md", generated, notes.AYAH_PERSONAL))

    def test_asma_note(self):
        generated = asma_notes.build(data.asma_ul_husna[0], data.asma_ul_husna)
        self.assertIn("MY OWN WORDS",
                      self._rebuild_keeps("asma.md", generated, notes.ASMA_PERSONAL))

    def test_personality_note(self):
        generated = personalities.build(data.personalities[0], data.personalities)
        self.assertIn("MY OWN WORDS",
                      self._rebuild_keeps("person.md", generated,
                                          notes.PERSONALITY_PERSONAL))


class FrontmatterIsParseableYaml(unittest.TestCase):
    """
    A frontmatter value that starts with a YAML indicator fails the whole site
    build, not just its own note — surah 80's transliteration is 'Abasa.
    """

    def _frontmatter(self, note: str) -> dict:
        import re
        block = note.split("---", 2)[1]
        fields = {}
        for line in block.strip().splitlines():
            key, _, value = line.partition(":")
            key, value = key.strip(), value.strip()
            # A JSON array and a list of class names: deliberately YAML flow lists.
            if key in ("tags", "cssclasses"):
                fields[key] = value
                continue
            if value.startswith('"'):
                self.assertTrue(value.endswith('"'), line)
                value = value[1:-1]
            else:
                self.assertNotIn(value[:1], "'\"-?,[{#&*!|>%@`", line)
            fields[key] = value
        return fields

    def test_every_surah_index(self):
        for number in range(1, data.SURAH_COUNT + 1):
            fields = self._frontmatter(surah_index.build(data.SURAHS[number]))
            self.assertEqual(fields["type"], data.SURAHS[number].type)

    def test_apostrophe_transliteration_is_quoted(self):
        note = surah_index.build(data.SURAHS[80])
        self.assertIn('transliteration: "\'Abasa"', note)

    def test_every_asma_note(self):
        for name in data.asma_ul_husna:
            self._frontmatter(asma_notes.build(name, data.asma_ul_husna))

    def test_quote_escapes_its_own_delimiters(self):
        self.assertEqual(notes.quote('a "b" c'), '"a \\"b\\" c"')


class AyahNavButtons(unittest.TestCase):
    """The site styles the buttons by position: Next, then Prev, both always there."""

    def _nav(self, surah, ayah):
        body = ayah_notes.build(data.SURAHS[surah], ayah, {
            "arabic": "a", "urdu": "u", "english": "e", "tafsir": "t", "tazkirul": "z"})
        return body.split("</audio>\n", 1)[1].split("\n", 1)[0]

    def test_middle_ayah_has_both(self):
        self.assertEqual(self._nav(11, 7), "[[11_8|Next 11:8]] [[11_6|Prev 11:6]]")

    def test_edges_keep_an_empty_slot(self):
        self.assertEqual(self._nav(1, 1), "[[1_2|Next 1:2]] <span></span>")
        self.assertEqual(self._nav(1, 7), "<span></span> [[1_6|Prev 1:6]]")


class TafsirPassages(unittest.TestCase):
    """Bayan ul Quran explains some ayaat together; each ayah note must say where."""

    def test_passage_start_carries_text_and_its_reach(self):
        tafsir = data.load_tafsir(1, 6)
        self.assertTrue(tafsir.startswith("_This commentary covers ayaat 6 and 7._"))
        self.assertIn("اِہْدِنَا", tafsir)

    def test_rest_of_passage_links_back_to_its_start(self):
        self.assertEqual(data.load_tafsir(1, 7),
                         "_The commentary on this ayah is given with [[1_6|ayah 1:6]]._")

    def test_no_link_across_surahs(self):
        # quran.com chains 13:1 onto 12:111's commentary, which is about 12:111.
        self.assertIn("no separate commentary", data.load_tafsir(13, 1))

    def test_single_ayah_is_just_text(self):
        self.assertFalse(data.load_tafsir(2, 255).startswith("_"))

    def test_tazkirul_repeats_become_one_passage(self):
        # The source repeats 2:1-5's passage on all five ayaat.
        self.assertTrue(data.load_tazkirul(2, 1).startswith(
            "_This commentary covers ayaat 1 to 5._"))
        for ayah in range(2, 6):
            self.assertEqual(data.load_tazkirul(2, ayah),
                             "_The commentary on this ayah is given with [[2_1|ayah 2:1]]._")
        self.assertFalse(data.load_tazkirul(2, 6).startswith("_The commentary"))

    def test_tazkirul_paragraphs_are_separate(self):
        self.assertNotRegex(data.load_tazkirul(2, 1), r"[^\n]\n[^\n]")


class SurahIndexNote(unittest.TestCase):
    """The folder page for a surah: identity, themes, and every ayah in order."""

    def setUp(self):
        self.note = surah_index.build(data.SURAHS[2])

    def test_names_the_surah_three_ways(self):
        for text in ("Al-Baqarah", "The Cow", "البقرة", "گائے"):
            self.assertIn(text, self.note)

    def test_links_every_ayah_in_order(self):
        import re
        numbers = [int(n) for n in re.findall(r"\[\[2_(\d+)\|\d+\]\]", self.note)]
        self.assertEqual(numbers, list(range(1, 287)))

    def test_neighbour_links_use_full_vault_paths(self):
        """A bare [[index]] is ambiguous — 114 notes carry that name."""
        self.assertIn("[[The Quran/1 - The Opener/index|", self.note)
        self.assertIn("[[The Quran/3 - Family of Imran/index|", self.note)

    def test_first_and_last_surah_have_one_neighbour(self):
        self.assertNotIn("← ", surah_index.build(data.SURAHS[1]))
        self.assertNotIn(" →", surah_index.build(data.SURAHS[114]))

    def test_themes_are_capped_and_counted(self):
        themes = surah_index.theme_counts(2)
        self.assertGreater(len(themes), surah_index.THEME_LIMIT)
        self.assertEqual(self.note.count("](tags/"), surah_index.THEME_LIMIT)
        self.assertEqual([c for _k, c in themes], sorted((c for _k, c in themes), reverse=True))


class HomeAndSectionPages(unittest.TestCase):
    """
    The home page offers four ways in, the same four the site's left panel
    shows; the Quran's page holds the surah cards.
    """

    def setUp(self):
        self.vault = Path(tempfile.mkdtemp())
        self.original_vault, config.VAULT_PATH = config.VAULT_PATH, self.vault

        explore.write_index()
        explore.write_quran_index()

        self.home = (self.vault / "index.md").read_text(encoding="utf-8")
        self.quran = (self.vault / "The Quran" / "index.md").read_text(encoding="utf-8")

    def tearDown(self):
        config.VAULT_PATH = self.original_vault

    def test_home_offers_the_four_ways_in_order(self):
        cards = re.findall(r"^- \[\[([^|]+)\|([^\]]+)\]\]", self.home, re.MULTILINE)
        self.assertEqual(cards, [("The Quran/index", "The Quran"),
                                 ("Personalities/index", "Personalities"),
                                 ("Asma Ul Husna/index", "Asma Ul Husna"),
                                 ("tags/index", "Themes")])

    def test_cards_come_before_the_meaning_of_the_word(self):
        self.assertLess(self.home.index("[[tags/index|Themes]]"),
                        self.home.index("**Tadabbur**"))

    def test_each_card_shows_three_entries_of_its_section(self):
        cards = re.split(r"^(?=- \[\[)", self.home, flags=re.MULTILINE)[1:]
        self.assertEqual(len(cards), 4)
        for card in cards:
            entries = re.findall(r"^    - \[\[[^|\]]+\|[^\]]+\]\] <span class=\"count\">",
                                 card, re.MULTILINE)
            self.assertEqual(len(entries), 3, card)

    def test_an_entry_says_the_number_its_own_page_says(self):
        ayaat = themes.ayah_counts()
        for key in explore.THEME_EXAMPLES:
            title = connections.THEMES[key][1]
            self.assertIn(f"[[tags/{key}|{title}]] "
                          f'<span class="count">{ayaat[key]:,} <span class="unit">ayaat</span>',
                          self.home)
        people = {person["id"]: person for person in data.personalities}
        for key in explore.PERSON_EXAMPLES:
            person = people[key]
            self.assertIn(f"[[{personalities.note_name(person)}|{person['name_english']}]] "
                          f'<span class="count">{personalities.ayah_count(person):,} ',
                          self.home)
        names = {name["transliteration"]: name for name in data.asma_ul_husna}
        for key in explore.NAME_EXAMPLES:
            self.assertIn(f"[[{asma_notes.note_name(names[key])}|{key}]] "
                          f'<span class="count">{names[key]["quran_occurrences"]:,} ',
                          self.home)

    def test_home_prose_has_no_em_dash(self):
        # A person's note is named "Musa (Moses) — مُوسَى"; that is a link's
        # target, not prose.
        prose = re.sub(r"\[\[[^|\]]+\|", "[[", self.home)
        self.assertNotIn("—", prose)

    def test_home_no_longer_carries_the_theme_tables(self):
        self.assertNotIn("](tags/", self.home)
        self.assertNotIn("| Topic |", self.home)

    def test_quran_page_holds_the_surah_cards_as_a_base_block(self):
        self.assertIn("```base\n" + explore.QURAN_BASE + "```", self.quran)
        self.assertIn('title: "The Quran"', self.quran)

    def test_no_emoji(self):
        for page, where in ((self.home, "home page"), (self.quran, "Quran page")):
            found = NoEmojiInGeneratedNotes.EMOJI.findall(page)
            self.assertEqual(found, [], f"{where} contains {found}")


class ThemesSection(unittest.TestCase):
    """One note per theme under tags/, and one page listing them all."""

    def setUp(self):
        self.vault = Path(tempfile.mkdtemp())
        self.original_vault, config.VAULT_PATH = config.VAULT_PATH, self.vault
        (self.vault / "tags").mkdir()
        (self.vault / "tags" / "retired_theme.md").write_text("old", encoding="utf-8")
        themes.generate()
        self.page = (self.vault / "tags" / "index.md").read_text(encoding="utf-8")

    def tearDown(self):
        config.VAULT_PATH = self.original_vault

    def _fields(self, key):
        note = (self.vault / "tags" / f"{key}.md").read_text(encoding="utf-8")
        return note.split("---")[1], note.split("---", 2)[2]

    def test_every_theme_has_a_note_named_by_its_key(self):
        """The site serves a theme at /tags/<key>, so the file name is the key."""
        written = {note.stem for note in (self.vault / "tags").glob("*.md")}
        self.assertEqual(written, set(connections.THEMES) | {"index"})

    def test_a_note_carries_the_theme_and_its_description(self):
        fields, body = self._fields("tawheed")
        self.assertIn('\ntitle: "Tawheed"\n', fields)
        self.assertIn("\ncategory: Belief\n", fields)
        self.assertIn(f"\nnotes: {themes.theme_counts()['tawheed']}\n", fields)
        self.assertIn(connections.THEMES["tawheed"][3], body)

    def test_a_note_has_no_fields_left_from_the_old_table(self):
        """`theme` and `order` only fed the table the Themes page used to be."""
        fields, _ = self._fields("tawheed")
        self.assertNotRegex(fields, r"(?m)^(theme|order):")

    def _sections(self):
        """The page's categories in order, each with its lines."""
        sections, current = {}, None
        for line in self.page.splitlines():
            if line.startswith("## "):
                current = sections.setdefault(line[3:], [])
            elif line.startswith("- ") and current is not None:
                current.append(line)
        return sections

    def test_page_lists_every_theme_once_under_its_category_in_order(self):
        """The order THEMES declares is the curated one, for categories and themes."""
        expected = {}
        for key, theme in connections.THEMES.items():
            expected.setdefault(theme[0], []).append(key)
        listed = {
            category: [re.match(r"- \[\[tags/([^|]+)\|", line).group(1) for line in lines]
            for category, lines in self._sections().items()
        }
        self.assertEqual(list(listed), list(expected))
        self.assertEqual(listed, expected)

    def test_a_line_carries_name_urdu_count_and_description(self):
        category, title, urdu, description = connections.THEMES["tawheed"]
        ayaat = themes.ayah_counts()["tawheed"]
        self.assertIn(
            f"- [[tags/tawheed|{title}]] "
            f'<span lang="ur">{urdu}</span> '
            f'<span class="count">{ayaat} <span class="unit">ayaat</span></span> '
            f"<small>{description}</small>",
            self._sections()[category],
        )

    def test_the_count_is_ayaat_only(self):
        """Personality and Name notes carry themes too, and are not ayaat."""
        ayaat, everything = themes.ayah_counts(), themes.theme_counts()
        self.assertTrue(all(ayaat[key] <= everything[key] for key in ayaat))
        self.assertEqual(
            ayaat["tawheed"],
            sum("tawheed" in tags for tags in connections.AYAH_TAGS.values()),
        )

    def test_one_ayah_is_not_called_ayaat(self):
        self.assertIn('1 <span class="unit">ayah</span>', themes.index_line("tawheed", 1))

    def test_every_line_leads_with_latin_text(self):
        """A line that opens with Urdu would be laid out right to left."""
        for lines in self._sections().values():
            for line in lines:
                self.assertRegex(line, r"^- \[\[tags/[a-z_0-9]+\|")

    def test_page_is_plain_lists_marked_for_the_site(self):
        self.assertIn("title: Themes", self.page)
        self.assertIn("cssclasses: [index-page, themes-index]", self.page)
        self.assertNotIn("```base", self.page)
        self.assertIn(themes.COUNTS_NOTE, self.page)

    def test_titles_with_an_ampersand_are_quoted(self):
        fields, _ = self._fields("rahmah")
        self.assertIn('\ntitle: "Mercy & Forgiveness"\n', fields)

    def test_a_retired_theme_loses_its_note(self):
        self.assertFalse((self.vault / "tags" / "retired_theme.md").exists())

    def test_no_emoji(self):
        found = NoEmojiInGeneratedNotes.EMOJI.findall(self.page)
        self.assertEqual(found, [], f"themes page contains {found}")


class NoEmojiInGeneratedNotes(unittest.TestCase):
    """
    Notes are read as text, and a colour emoji font paints its own colours over
    the page. Anything pictorial stays out of what the generator writes.
    """

    EMOJI = re.compile(
        "[\U0001F000-\U0001FAFF\U0001F1E6-\U0001F1FF\u2600-\u27BF\u2B00-\u2BFF\uFE0F]"
    )

    def _assert_clean(self, note: str, where: str):
        found = self.EMOJI.findall(note)
        self.assertEqual(found, [], f"{where} contains {found}")

    def test_ayah_note(self):
        self._assert_clean(ayah_notes.build(
            data.SURAHS[2], 255,
            {"arabic": "a", "urdu": "u", "english": "e", "tafsir": "t", "tazkirul": "z"},
        ), "ayah note")

    def test_every_asma_note(self):
        for name in data.asma_ul_husna:
            self._assert_clean(asma_notes.build(name, data.asma_ul_husna),
                               asma_notes.note_name(name))

    def test_every_personality_note(self):
        for person in data.personalities:
            self._assert_clean(personalities.build(person, data.personalities),
                               personalities.note_name(person))

    def test_every_surah_index(self):
        for number in range(1, data.SURAH_COUNT + 1):
            self._assert_clean(surah_index.build(data.SURAHS[number]), f"surah {number}")

    def test_scaffolding_defaults(self):
        for default in (notes.AYAH_PERSONAL, notes.PERSONALITY_PERSONAL,
                        notes.ASMA_PERSONAL, notes.SURAH_PERSONAL):
            self._assert_clean(default, "scaffolding")


class ScaffoldingRefresh(unittest.TestCase):
    """
    The 6,400 notes already in the vault carry the old emoji headings in their
    personal section, which is preserved verbatim on every run. Untouched
    scaffolding is the one part safe to replace.
    """

    def setUp(self):
        self.folder = Path(tempfile.mkdtemp())

    def _rebuild(self, personal: str) -> str:
        note = self.folder / "note.md"
        note.write_text(f"generated\n{config.SENTINEL_END}{personal}", encoding="utf-8")
        notes.write_note(self.folder, "note.md",
                         f"generated\n{config.SENTINEL_END}", notes.AYAH_PERSONAL)
        return note.read_text(encoding="utf-8")

    def test_old_emoji_scaffolding_is_replaced(self):
        rebuilt = self._rebuild("\n## 📝 Tafsir Notes\n\n")
        self.assertNotIn("📝", rebuilt)
        self.assertIn("## Tafsir Notes", rebuilt)

    def test_retired_multi_heading_scaffolding_is_replaced(self):
        rebuilt = self._rebuild(
            "\n## 📝 Tafsir Notes\n\n\n## 💡 Personal Reflection\n\n\n## 🔗 Thematic Links\n\n")
        self.assertNotIn("Personal Reflection", rebuilt)
        self.assertIn("## Tafsir Notes", rebuilt)

    def test_a_reader_s_words_are_never_touched(self):
        rebuilt = self._rebuild("\n## 📝 Tafsir Notes\n\nMY OWN WORDS\n")
        self.assertIn("MY OWN WORDS", rebuilt)
        self.assertIn("## 📝 Tafsir Notes", rebuilt)

    def test_a_reader_s_own_heading_is_never_touched(self):
        rebuilt = self._rebuild("\n## My questions\n\n")
        self.assertIn("## My questions", rebuilt)


class Sentinels(unittest.TestCase):
    """Both markers must be present, in order, or preservation cannot work."""

    def _assert_well_formed(self, note: str):
        start = note.find(config.SENTINEL_START)
        end = note.find(config.SENTINEL_END)
        self.assertNotEqual(start, -1, "missing GENERATED:START")
        self.assertNotEqual(end, -1, "missing GENERATED:END")
        self.assertLess(start, end, "sentinels are out of order")

    def test_ayah(self):
        self._assert_well_formed(ayah_notes.build(
            data.SURAHS[1], 1,
            {"arabic": "a", "urdu": "u", "english": "e", "tafsir": "t", "tazkirul": "z"},
        ))

    def test_every_asma_note(self):
        for name in data.asma_ul_husna:
            self._assert_well_formed(asma_notes.build(name, data.asma_ul_husna))

    def test_every_personality_note(self):
        for person in data.personalities:
            self._assert_well_formed(personalities.build(person, data.personalities))


class AsmaNoteNaming(unittest.TestCase):
    """The note name is the wikilink target, the page title and the sidebar label."""

    def test_number_transliteration_arabic(self):
        name = next(n for n in data.asma_ul_husna if n["number"] == 10)
        self.assertEqual(asma_notes.note_name(name), "10 - Al-Jabbar ٱلْجَبَّار")

    def test_every_related_link_resolves(self):
        """A Related Names link pointing at a note that is never written is a dead end."""
        written = {asma_notes.note_name(n) for n in data.asma_ul_husna}
        for name in data.asma_ul_husna:
            for other in asma_notes.related(name, data.asma_ul_husna):
                self.assertIn(asma_notes.note_name(other), written)


class RelatedNames(unittest.TestCase):
    """Same category, never itself, capped so a big category stays navigable."""

    def _category(self, title):
        return [n for n in data.asma_ul_husna if n["category"] == title]

    def test_small_category_links_all_siblings(self):
        group = self._category("Names of Peace & Security")
        self.assertEqual(len(asma_notes.related(group[0], data.asma_ul_husna)),
                         len(group) - 1)

    def test_lone_name_has_no_siblings(self):
        lone = self._category("Names of Holiness")[0]
        self.assertEqual(asma_notes.related(lone, data.asma_ul_husna), [])

    def test_large_category_is_capped(self):
        biggest = self._category("Names of Power & Sovereignty")[0]
        self.assertEqual(len(asma_notes.related(biggest, data.asma_ul_husna)),
                         asma_notes.RELATED_LIMIT)

    def test_never_links_itself(self):
        for name in data.asma_ul_husna:
            numbers = [o["number"] for o in asma_notes.related(name, data.asma_ul_husna)]
            self.assertNotIn(name["number"], numbers)
            self.assertEqual(len(numbers), len(set(numbers)))

    def test_every_name_is_reachable(self):
        """Wrapping large categories means no Name is left without inbound links."""
        linked = {o["number"]
                  for n in data.asma_ul_husna
                  for o in asma_notes.related(n, data.asma_ul_husna)}
        orphans = [n["number"] for n in data.asma_ul_husna
                   if n["number"] not in linked
                   and len(self._category(n["category"])) > 1]
        self.assertEqual(orphans, [])


class AsmaMasterIndex(unittest.TestCase):
    """The folder's own page. Without it the site lists the folder as raw files."""

    def setUp(self):
        self.folder = Path(tempfile.mkdtemp())
        asma_notes._write_master_index(data.asma_ul_husna, self.folder)
        self.index = (self.folder / "index.md").read_text(encoding="utf-8")

    def _sections(self, page=None):
        sections, current = {}, None
        for line in (page or self.index).splitlines():
            if line.startswith("## "):
                current = sections.setdefault(line[3:], [])
            elif line.startswith("- ") and current is not None:
                current.append(line)
        return sections

    def test_is_a_listing_page_with_one_title(self):
        """The site draws the title from the frontmatter; a heading here was a second one."""
        self.assertIn("\ntitle: Asma Ul Husna\n", self.index)
        self.assertIn("\ncssclasses: [index-page, names-index]\n", self.index)
        self.assertNotRegex(self.index, r"(?m)^# ")
        self.assertNotRegex(self.index, r"(?m)^\|")

    def test_lists_every_name_once_under_its_category(self):
        sections = self._sections()
        self.assertEqual(sum(len(lines) for lines in sections.values()),
                         len(data.asma_ul_husna))
        for name in data.asma_ul_husna:
            heading = asma_notes.category_heading(name["category"])
            link = f"[[{asma_notes.note_name(name)}|{name['transliteration']}]]"
            self.assertEqual(sum(link in line for line in sections[heading]), 1, link)

    def test_headings_drop_what_the_page_already_says(self):
        self.assertIn("Forgiveness & Mercy", self._sections())
        self.assertIn("The Hereafter", self._sections())
        self.assertFalse([h for h in self._sections() if h.startswith("Names of")])

    def test_names_run_in_traditional_order_within_a_category(self):
        for lines in self._sections().values():
            numbers = [int(re.search(r'class="num">(\d+)<', line).group(1)) for line in lines]
            self.assertEqual(numbers, sorted(numbers))

    def test_a_line_carries_what_the_site_lays_out(self):
        """Number, link, Arabic marked as Arabic, count with its unit, then the details."""
        line = asma_notes.index_line(next(n for n in data.asma_ul_husna if n["number"] == 2))
        self.assertRegex(line, r'^- <span class="num">2</span> \[\[2 - Ar-Rahman [^|]+\|Ar-Rahman\]\] '
                               r'<span lang="ar">[^<]+</span> '
                               r'<span class="count">57 <span class="unit">times</span></span> '
                               r'<small>The Most Gracious · <span lang="ur">[^<]+</span> · '
                               r'<span class="root">root <span lang="ar">ر-ح-م</span></span></small>$')

    def test_a_name_that_does_not_appear_has_no_count(self):
        absent = next(n for n in data.asma_ul_husna if not n["quran_occurrences"])
        self.assertNotIn('class="count"', asma_notes.index_line(absent))

    def test_two_roots_are_each_marked_arabic(self):
        """The "and" between them is English and must not be read as Arabic."""
        two = next(n for n in data.asma_ul_husna if " and " in n["root"])
        self.assertRegex(asma_notes.index_line(two),
                         r'root <span lang="ar">[^<]+</span> and <span lang="ar">[^<]+</span>')

    def test_unknown_category_still_listed(self):
        """A category added to the data but not to CATEGORY_ORDER must not vanish."""
        extra = dict(data.asma_ul_husna[0], number=100, category="Names of Something New")
        asma_notes._write_master_index([extra], self.folder)
        refreshed = (self.folder / "index.md").read_text(encoding="utf-8")
        self.assertEqual(list(self._sections(refreshed)), ["Something New"])


class ProfileNotes(unittest.TestCase):
    """A person's or a Name's note says its fields in lines under its heading."""

    def test_a_person_links_its_type_its_ayaat_and_its_themes(self):
        adam = next(p for p in data.personalities if p["id"] == "adam")
        note = personalities.build(adam, data.personalities)
        self.assertIn("\ncssclasses: [profile]\n", note)
        self.assertIn("\n# Adam — آدَم\n\nآدم علیہ السلام\n\n> [[Personalities/index#Prophets and "
                      "Messengers|Prophet / Messenger]] · Straight Path · ", note)
        self.assertIn(f"[[#Mentioned in Quran|{len(adam['mentioned_in'])} ayaat]]", note)
        self.assertIn("> **Themes:** [[tags/story_adam|" + connections.THEMES["story_adam"][1] + "]]", note)
        self.assertEqual(len(re.findall(r"(?m)^# ", note)), 1)
        self.assertNotRegex(note, r"(?m)^#{3,} ")

    def test_a_person_with_no_other_names_or_ayaat_says_neither(self):
        for person in data.personalities:
            summary = personalities.summary(person)
            if not person.get("also_known_as"):
                self.assertNotIn("Also known as", summary)
            if not person.get("mentioned_in"):
                self.assertNotIn("Mentioned in Quran", summary)

    def test_a_type_link_lands_on_a_heading_the_page_has(self):
        folder = Path(tempfile.mkdtemp())
        personalities._write_master_index(data.personalities, folder)
        page = (folder / "index.md").read_text(encoding="utf-8")
        for person in data.personalities:
            target = re.search(r"\[\[Personalities/index#([^|]+)\|", personalities.summary(person))
            self.assertIn(f"\n## {target.group(1)}\n", page)

    def test_a_name_links_its_category_and_its_themes(self):
        rahman = next(n for n in data.asma_ul_husna if n["number"] == 2)
        note = asma_notes.build(rahman, data.asma_ul_husna)
        self.assertIn("\ncssclasses: [profile]\n", note)
        self.assertIn("\n**The Most Gracious**\n\n", note)
        self.assertIn("> Name 2 of 99 · [[Asma Ul Husna/index#Forgiveness & Mercy|Names of "
                      "Forgiveness & Mercy]] · In the Quran: 57 times\n", note)
        self.assertIn("> **Themes:** [[tags/", note)
        self.assertEqual(len(re.findall(r"(?m)^# ", note)), 1)
        self.assertNotRegex(note, r"(?m)^#{3,} ")

    def test_a_category_link_lands_on_a_heading_the_page_has(self):
        folder = Path(tempfile.mkdtemp())
        asma_notes._write_master_index(data.asma_ul_husna, folder)
        page = (folder / "index.md").read_text(encoding="utf-8")
        for name in data.asma_ul_husna:
            target = re.search(r"\[\[Asma Ul Husna/index#([^|]+)\|",
                               asma_notes.build(name, data.asma_ul_husna))
            self.assertIn(f"\n## {target.group(1)}\n", page)


class RenamedNoteKeepsPersonalSection(unittest.TestCase):
    """Renaming must move the file; a copy would strand the reader's writing."""

    def setUp(self):
        self.folder = Path(tempfile.mkdtemp())

    def test_personal_section_follows_the_rename(self):
        old = self.folder / "10 - old.md"
        old.write_text("generated\n<!-- GENERATED:END -->\nMY OWN WORDS\n",
                       encoding="utf-8")

        self.assertTrue(notes.rename_note(self.folder, "10 - old.md", "10 - new.md"))
        self.assertFalse(old.exists())
        self.assertIn("MY OWN WORDS",
                      (self.folder / "10 - new.md").read_text(encoding="utf-8"))

    def test_leaves_an_already_renamed_note_alone(self):
        (self.folder / "10 - new.md").write_text("current", encoding="utf-8")
        self.assertFalse(notes.rename_note(self.folder, "10 - old.md", "10 - new.md"))
        self.assertEqual((self.folder / "10 - new.md").read_text(encoding="utf-8"),
                         "current")

    def test_never_overwrites_an_existing_note(self):
        (self.folder / "10 - old.md").write_text("old", encoding="utf-8")
        (self.folder / "10 - new.md").write_text("new", encoding="utf-8")
        self.assertFalse(notes.rename_note(self.folder, "10 - old.md", "10 - new.md"))
        self.assertEqual((self.folder / "10 - new.md").read_text(encoding="utf-8"),
                         "new")


class RenamedFolderKeepsPersonalSections(unittest.TestCase):
    """The folder equivalent of RenamedNoteKeepsPersonalSection."""

    def setUp(self):
        self.parent = Path(tempfile.mkdtemp())

    def test_personal_section_follows_the_rename(self):
        old = self.parent / "1 - old"
        old.mkdir()
        (old / "note.md").write_text("generated\n<!-- GENERATED:END -->\nMY OWN WORDS\n",
                                     encoding="utf-8")

        self.assertTrue(notes.rename_folder(self.parent, "1 - old", "1 new"))
        self.assertFalse(old.exists())
        self.assertIn("MY OWN WORDS",
                      (self.parent / "1 new" / "note.md").read_text(encoding="utf-8"))

    def test_leaves_an_already_renamed_folder_alone(self):
        (self.parent / "1 new").mkdir()
        self.assertFalse(notes.rename_folder(self.parent, "1 - old", "1 new"))

    def test_never_overwrites_an_existing_folder(self):
        (self.parent / "1 - old").mkdir()
        (self.parent / "1 new").mkdir()
        self.assertFalse(notes.rename_folder(self.parent, "1 - old", "1 new"))


class QuranCardsMatchSurahNotes(unittest.TestCase):
    """The surah grid shows one card per surah, linking to its index note."""

    def test_filters_on_what_only_surah_indexes_have(self):
        self.assertIn('file.name == "index"', explore.QURAN_BASE)
        self.assertIn('file.hasProperty("surah_name")', explore.QURAN_BASE)
        for number in data.SURAHS:
            fields = surah_index.build(data.SURAHS[number]).split("---")[1]
            self.assertIn("\nsurah_name: ", fields)
            self.assertIn(f"\nsurah: {number} / ", fields)
            self.assertIn("\ntitle: ", fields)

    def test_card_title_is_not_repeated_as_a_row(self):
        self.assertNotIn("note.title", explore.QURAN_BASE)


class PersonalitiesPage(unittest.TestCase):
    """Every figure as a line in a plain list, under a heading for its type."""

    def setUp(self):
        self.folder = Path(tempfile.mkdtemp())
        personalities._write_master_index(data.personalities, self.folder)
        self.page = (self.folder / "index.md").read_text(encoding="utf-8")

    def _sections(self):
        sections, current = {}, None
        for line in self.page.splitlines():
            if line.startswith("## "):
                current = sections.setdefault(line[3:], [])
            elif line.startswith("- ") and current is not None:
                current.append(line)
        return sections

    def test_is_a_listing_page_and_no_longer_a_table(self):
        self.assertIn("\ntitle: Personalities\n", self.page)
        self.assertIn("\ncssclasses: [index-page, people-index]\n", self.page)
        self.assertNotIn("```base", self.page)

    def test_lists_every_figure_once_under_its_type_in_order(self):
        """Types in TYPE_META's order; within one, the order of the data."""
        sections = self._sections()
        present = [key for key in personalities.TYPE_META
                   if any(p["type"] == key for p in data.personalities)]
        self.assertEqual(list(sections), [personalities.TYPE_HEADINGS[key] for key in present])
        self.assertEqual(sum(len(lines) for lines in sections.values()), len(data.personalities))
        prophets = sections["Prophets and Messengers"]
        self.assertIn("|Adam]]", prophets[0])
        self.assertIn("|Nuh (Noah)]]", prophets[1])

    def test_a_line_carries_what_the_site_lays_out(self):
        """Link, Arabic marked as Arabic, count with its unit, then path, era and Urdu."""
        adam = next(p for p in data.personalities if p["id"] == "adam")
        self.assertRegex(personalities.index_line(adam),
                         r'^- \[\[Adam — [^|]+\|Adam\]\] <span lang="ar">[^<]+</span> '
                         r'<span class="count">\d+ <span class="unit">ayaat</span></span> '
                         r'<small><span class="path" data-rank="1">Straight Path</span> · '
                         r'Beginning of humanity · <span lang="ur">[^<]+</span></small>$')

    def test_paths_carry_their_place_among_the_paths(self):
        """The site shows the paths in this order: straight, mixed, deviated."""
        ranks = dict(re.findall(r'data-rank="(\d)">([^<]+)<', self.page))
        self.assertEqual(ranks, {"1": "Straight Path", "2": "Mixed Path", "3": "Deviated Path"})

    def test_a_figure_with_no_ayaat_listed_has_no_count(self):
        silent = next(p for p in data.personalities if not p.get("mentioned_in"))
        self.assertNotIn('class="count"', personalities.index_line(silent))

    def test_the_two_notes_on_paths_follow_the_lists(self):
        self.assertIn("**Mixed Path.** ", self.page)
        self.assertIn("**Deviated Path.** ", self.page)

    def test_order_runs_through_one_type_at_a_time(self):
        order = personalities.listing_order(data.personalities)
        self.assertEqual(sorted(order.values()), list(range(1, len(data.personalities) + 1)))

    def test_a_note_no_longer_carries_the_tables_sort_key(self):
        """`order` only fed the table the Personalities page used to be."""
        note = personalities.build(data.personalities[0], data.personalities)
        self.assertNotRegex(note.split("---")[1], r"(?m)^order:")


class LayoutMigration(unittest.TestCase):
    """An older vault moves into the section folders with the reader's notes."""

    def _old_vault(self, tmp):
        vault = Path(tmp)
        (vault / "2 - The Cow").mkdir()
        (vault / "2 - The Cow" / "2_255.md").write_text("mine", encoding="utf-8")
        explore_dir = vault / config.LEGACY_EXPLORE_DIR
        (explore_dir / "Personalities").mkdir(parents=True)
        (explore_dir / "Personalities" / "Adam.md").write_text("adam", encoding="utf-8")
        (explore_dir / "Asma Ul Husna").mkdir()
        (explore_dir / "index.md").write_text("generated", encoding="utf-8")
        (explore_dir / "Themes.md").write_text("generated", encoding="utf-8")
        return vault, explore_dir

    def test_moves_everything_into_the_sections(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault, explore_dir = self._old_vault(tmp)
            (explore_dir / "Quran.base").write_text(explore.OLD_QURAN_BASES[0],
                                                    encoding="utf-8")
            self.assertEqual(layout.migrate(vault), 3)
            self.assertEqual((vault / "The Quran/2 - The Cow/2_255.md").read_text(), "mine")
            self.assertEqual((vault / "Personalities" / "Adam.md").read_text(), "adam")
            self.assertTrue((vault / "Asma Ul Husna").is_dir())
            self.assertFalse(explore_dir.exists())
            self.assertEqual(layout.migrate(vault), 0)

    def test_removes_the_themes_note_that_stood_at_the_top_level(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp)
            (vault / "Themes.md").write_text("generated", encoding="utf-8")
            layout.migrate(vault)
            self.assertFalse((vault / "Themes.md").exists())

    def test_moves_the_oldest_folder_names_too(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp)
            (vault / "2 The Cow").mkdir()
            (vault / "2 The Cow" / "2_255.md").write_text("mine", encoding="utf-8")
            layout.migrate(vault)
            self.assertEqual((vault / "The Quran/2 - The Cow/2_255.md").read_text(), "mine")

    def test_removes_the_retired_path_pages(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault, explore_dir = self._old_vault(tmp)
            filtered = explore_dir / "Personalities" / "Filtered"
            filtered.mkdir()
            for name in personalities.RETIRED_PATH_PAGES:
                (filtered / name).write_text("generated", encoding="utf-8")
            layout.migrate(vault)
            self.assertFalse((vault / "Personalities" / "Filtered").exists())
            self.assertTrue((vault / "Personalities" / "Adam.md").exists())

    def test_keeps_a_base_edited_in_obsidian(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault, explore_dir = self._old_vault(tmp)
            (explore_dir / "Quran.base").write_text("my own view\n", encoding="utf-8")
            layout.migrate(vault)
            self.assertEqual((explore_dir / "Quran.base").read_text(), "my own view\n")


class CanvasRelinking(unittest.TestCase):
    """Canvas cards follow the ayah notes to their renamed paths."""

    CANVAS = ('{\n\t"nodes":[\n'
              '\t\t{"id":"a","type":"file","file":"2 - The Cow البقرة/2_255: The Cow البقرة.md","x":0},\n'
              '\t\t{"id":"b","type":"file","file":"0 - Explore/Personalities/Filtered/Straight Path.md","x":1},\n'
              '\t\t{"id":"c","type":"text","text":"mine","x":2}\n'
              '\t]\n}')

    def test_rewrites_old_paths_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "x.canvas"
            path.write_text(self.CANVAS, encoding="utf-8")
            self.assertTrue(assets.relink_canvas(path))
            expected = (self.CANVAS
                        .replace("2 - The Cow البقرة/2_255: The Cow البقرة.md",
                                 "The Quran/2 - The Cow/2_255.md")
                        .replace("0 - Explore/Personalities/Filtered/Straight Path.md",
                                 "Personalities/index.md"))
            self.assertEqual(path.read_text(encoding="utf-8"), expected)
            self.assertFalse(assets.relink_canvas(path))

    def test_cards_on_people_follow_the_folder(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "x.canvas"
            path.write_text('{"file":"0 - Explore/Personalities/Adam — آدَم.md"}',
                            encoding="utf-8")
            self.assertTrue(assets.relink_canvas(path))
            self.assertEqual(path.read_text(encoding="utf-8"),
                             '{"file":"Personalities/Adam — آدَم.md"}')

    def test_rewrites_the_top_level_folder_layouts(self):
        for old in ("2 The Cow/2_255.md", "2 - The Cow/2_255.md"):
            with tempfile.TemporaryDirectory() as tmp:
                path = Path(tmp) / "x.canvas"
                path.write_text(f'{{"file":"{old}"}}', encoding="utf-8")
                self.assertTrue(assets.relink_canvas(path))
                self.assertEqual(path.read_text(encoding="utf-8"),
                                 '{"file":"The Quran/2 - The Cow/2_255.md"}')

    def test_shipped_canvases_point_at_current_notes(self):
        for canvas in config.VAULT_FILES_SRC.rglob("*.canvas"):
            with tempfile.TemporaryDirectory() as tmp:
                copy = Path(tmp) / canvas.name
                copy.write_bytes(canvas.read_bytes())
                self.assertFalse(assets.relink_canvas(copy), canvas.name)


class BismillahPlacement(unittest.TestCase):
    def test_prepended_to_opening_ayah(self):
        self.assertTrue(ayah_notes.arabic_text(2, 1, "x").startswith(config.BISMILLAH))

    def test_skipped_for_fatihah_and_tawbah(self):
        self.assertEqual(ayah_notes.arabic_text(1, 1, "x"), "x")
        self.assertEqual(ayah_notes.arabic_text(9, 1, "x"), "x")

    def test_not_added_mid_surah(self):
        self.assertEqual(ayah_notes.arabic_text(2, 2, "x"), "x")


if __name__ == "__main__":
    unittest.main()
