"""
Loads the source dataset once, at import time.

Everything downstream reads from here rather than opening files itself, so
there is a single place to look when you want to know what data exists.
"""

import json
from functools import cache
from pathlib import Path

import config


def load_json(path: Path):
    """Reads a UTF-8 JSON file, with a message that names the file when it fails."""
    try:
        with open(path, encoding="utf-8") as handle:
            return json.load(handle)
    except FileNotFoundError:
        raise FileNotFoundError(f"missing data file: {path}") from None
    except json.JSONDecodeError as error:
        raise ValueError(f"{path} is not valid JSON: {error}") from None


quran = load_json(config.QURAN_JSON)
english = load_json(config.ENGLISH_JSON)
urdu = load_json(config.URDU_JSON)
chapters_en = load_json(config.CHAPTERS_EN_JSON)
chapters_ur = load_json(config.CHAPTERS_UR_JSON)
asma_ul_husna = load_json(config.ASMA_JSON)
personalities = load_json(config.PERSONALITIES_JSON)

SURAH_COUNT = len(chapters_en)


class Surah:
    """The names and metadata of one surah, gathered from both chapter files."""

    __slots__ = ("number", "english", "arabic", "urdu", "transliteration", "type",
                 "total_ayaat")

    def __init__(self, number: int):
        index = number - 1
        self.number = number
        self.english = chapters_en[index]["translation"]
        self.arabic = chapters_ur[index]["name"]
        self.urdu = chapters_ur[index]["translation"]
        self.transliteration = chapters_en[index]["transliteration"]
        self.type = chapters_ur[index]["type"]
        self.total_ayaat = chapters_ur[index]["total_verses"]

    @property
    def folder_name(self) -> str:
        """
        Vault folder for this surah, e.g. '2 - The Cow'.

        No Arabic: this becomes a URL path segment on the published site, and
        Arabic slugifies to an unreadable percent-encoded block. The Arabic
        name still appears in the surah's own index note and every ayah note.
        """
        return f"{self.number} - {self.english}"

    @property
    def folder(self) -> str:
        """Vault path of this surah's folder, e.g. 'The Quran/2 - The Cow'."""
        return f"{config.QURAN_DIR}/{self.folder_name}"

    @property
    def index_path(self) -> str:
        """
        Wikilink target of this surah's page. 114 notes are called 'index',
        so a bare [[index]] is ambiguous; the path is what makes it land.
        """
        return f"{self.folder}/index"

    def note_name(self, ayah: int) -> str:
        """
        Note name for one ayah, e.g. '2_255'.

        This doubles as the wikilink target and the URL path segment, so the
        format is load-bearing: the published site's links break if it
        changes. Kept to bare numbers so the URL doesn't repeat the surah
        name already in the folder segment, or carry an unreadable
        percent-encoded Arabic block. `display_name` below carries the full
        human-readable form instead, for the page's `title` frontmatter.
        """
        return f"{self.number}_{ayah}"

    def display_name(self, ayah: int) -> str:
        """
        An ayah's page title, e.g. 'Al-Baqarah 2:255': the surah by the name
        readers cite it by, and the reference as it is written everywhere
        else. Search, backlinks and the browser tab all show it.
        """
        return f"{self.transliteration} {self.number}:{ayah}"


# Built once so any module can turn a surah number into its names.
SURAHS = {number: Surah(number) for number in range(1, SURAH_COUNT + 1)}


def wikilink(surah: int, ayah: int) -> str:
    """An Obsidian link to an ayah note: [[2_255: The Cow البقرة]]."""
    if surah in SURAHS:
        return f"[[{SURAHS[surah].note_name(ayah)}]]"
    return f"[[{surah}_{ayah}]]"


# Both tafsirs explain several ayaat in one passage. Every ayah the passage
# covers carries it whole, under a line that says how far it reaches: a reader
# who lands on 2:3 gets the commentary there, not a link to 2:1. Until
# 2026-10-16 only the first ayah carried it, because unfolded on a phone it was
# the same long text page after page; the site now folds both tafsirs.
TAFSIR_MISSING = "_Tafsir not available for this ayah._"


def _passage(surah: int, ayah: int, text: str, first: int, last: int) -> str:
    """A passage covering ayaat first..last, as one of those ayaat shows it."""
    if last == first:
        return text

    def link(number: int) -> str:
        reference = f"{surah}:{number}"
        if number == ayah:
            return reference
        return f"[[{SURAHS[surah].note_name(number)}|{reference}]]"

    joiner = "and" if last == first + 1 else "to"
    return f"_This commentary is for ayaat {link(first)} {joiner} {link(last)}._\n\n{text}"


def load_tafsir(surah: int, ayah: int) -> str:
    """
    Bayan ul Quran (Dr. Israr Ahmad) for one ayah. Missing or unreadable files
    degrade to a notice rather than aborting a 6,236-note run partway through.

    Each file's `covers` names the first and last ayah of its passage, or is
    null for an ayah with no commentary of its own (see docs/LICENSES.md §4).
    """
    path = config.BAYAN_DIR / str(surah) / f"{ayah}.json"
    try:
        with open(path, encoding="utf-8") as handle:
            entry = json.load(handle)
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return TAFSIR_MISSING

    covers = entry.get("covers")
    if not covers:
        return "_Bayan ul Quran has no separate commentary on this ayah._"
    first = covers[0]
    text = entry.get("text", "")
    if first != ayah:
        # The passage's text is kept once, on its first ayah.
        try:
            with open(config.BAYAN_DIR / str(surah) / f"{first}.json", encoding="utf-8") as handle:
                text = json.load(handle).get("text", "")
        except (FileNotFoundError, json.JSONDecodeError, OSError):
            return TAFSIR_MISSING
    return _passage(surah, ayah, text, *covers)


@cache
def _tazkirul_surah(surah: int) -> list:
    """Every ayah's Tazkirul Quran text for one surah, None where unreadable."""
    texts = []
    for ayah in range(1, SURAHS[surah].total_ayaat + 1):
        try:
            with open(config.TAZKIRUL_DIR / str(surah) / f"{ayah}.json",
                      encoding="utf-8") as handle:
                texts.append(json.load(handle).get("text", ""))
        except (FileNotFoundError, json.JSONDecodeError, OSError):
            texts.append(None)
    return texts


def load_tazkirul(surah: int, ayah: int) -> str:
    """
    Tazkirul Quran (Maulana Wahiduddin Khan) for one ayah.

    The source repeats a passage in full on every ayah it covers, so a
    passage is a run of consecutive ayaat with identical text. Paragraphs are
    split by single newlines, which Markdown would run together.
    """
    texts = _tazkirul_surah(surah)
    text = texts[ayah - 1]
    if not text:
        return TAFSIR_MISSING

    first = last = ayah
    while first > 1 and texts[first - 2] == text:
        first -= 1
    while last < len(texts) and texts[last] == text:
        last += 1

    paragraphs = "\n\n".join(line.strip() for line in text.split("\n") if line.strip())
    return _passage(surah, ayah, paragraphs, first, last)
