"""
Smoke tests for the generator.

Standard library only — run them with:

    python -m unittest discover tests

They cover the things that quietly break a published vault: the global ayah
numbering the CDN depends on, the note filename format the site's links are
built from, and the promise that hand-written sections survive a rebuild.
"""

import tempfile
import unittest
from pathlib import Path

import config
from tadabbur import asma_notes, audio, ayah_notes, data, notes, personalities


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
        self.assertEqual(data.SURAHS[2].note_name(255), "2_255: The Cow البقرة")

    def test_wikilink_round_trip(self):
        self.assertEqual(data.wikilink(2, 255), "[[2_255: The Cow البقرة]]")


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
            {"arabic": "a", "urdu": "u", "english": "e", "tafsir": "t"},
        )
        self.assertIn("MY OWN WORDS",
                      self._rebuild_keeps("ayah.md", generated, notes.AYAH_PERSONAL))

    def test_asma_note(self):
        generated = asma_notes.build(data.asma_ul_husna[0])
        self.assertIn("MY OWN WORDS",
                      self._rebuild_keeps("asma.md", generated, notes.ASMA_PERSONAL))

    def test_personality_note(self):
        generated = personalities.build(data.personalities[0], data.personalities)
        self.assertIn("MY OWN WORDS",
                      self._rebuild_keeps("person.md", generated,
                                          notes.PERSONALITY_PERSONAL))


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
            {"arabic": "a", "urdu": "u", "english": "e", "tafsir": "t"},
        ))

    def test_every_asma_note(self):
        for name in data.asma_ul_husna:
            self._assert_well_formed(asma_notes.build(name))

    def test_every_personality_note(self):
        for person in data.personalities:
            self._assert_well_formed(personalities.build(person, data.personalities))


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
