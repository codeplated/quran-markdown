"""
The home page and the Quran's own page, with one card per surah.

The home page offers four ways in, The Quran, Personalities, Asma Ul Husna and
Themes. They are the same four the site's left panel shows as its parents. Each
is a card that says what its section holds and shows three entries from it.
"""

import config
import quranConnections as connections
from tadabbur import asma_notes, data, notes, personalities, themes

# Notes that lived under '0 - Explore' and were rebuilt wholesale on every
# run: the Explore page, which the home page's cards replace, and the old
# Themes A–Z note. layout.migrate removes them, and the Themes note that stood
# at the top level before the themes had a folder of their own.
RETIRED_EXPLORE_NOTES = ("index.md", "Themes.md")
RETIRED_THEMES_NOTE = "Themes.md"

# The view on the Quran's page: one card per surah, linking to the surah's
# index note. It is written into The Quran/index.md as a `base` block, which
# Obsidian and the site both draw in place. Every folder index
# is called "index", so the surah ones are told apart by their surah_name
# property; the number is parsed from "surah: 2 / 114" so the cards sort in
# Mushaf order. The site draws each card's heading from the note's title on
# its own, so `order` stays empty: listing note.title there printed it twice.
QURAN_BASE = """formulas:
  surah_number: number(note.surah.split(" ")[0])
views:
  - type: cards
    name: Surahs
    filters:
      and:
        - file.name == "index"
        - file.hasProperty("surah_name")
    sort:
      - property: formula.surah_number
        direction: ASC
    rowHeight: tall
    cardSize: 270
    image: note.image
    imageAspectRatio: 1
"""

# Quran.base, a file of its own under '0 - Explore', as earlier versions wrote
# it. layout.migrate removes one of these left unchanged; a copy edited inside
# Obsidian is left alone.
# The first matched ayah notes by "_1:", which the bare "2_1" names never
# contain, so it showed no cards at all.
_FIRST_AYAH_BASE = """formulas:
  surah_number: number(file.name.split("_")[0])
views:
  - type: cards
    name: Surahs
    filters:
      and:
        - file.name.endsWith("_1")
    order:
      - note.title
    sort:
      - property: formula.surah_number
        direction: ASC
    rowHeight: tall
    cardSize: 270
    image: note.image
    imageAspectRatio: 1
"""
# The second linked each card to the surah's first ayah rather than the
# surah, and printed the title twice on the site.
OLD_QURAN_BASES = (
    _FIRST_AYAH_BASE.replace('file.name.endsWith("_1")', 'file.name.contains("_1:")')
                    .replace("note.title", "file.name"),
    _FIRST_AYAH_BASE,
)


# Every text the generator has written to Quran.base, the current view included.
GENERATED_QURAN_BASES = (QURAN_BASE, *OLD_QURAN_BASES)


# What a card shows of its section: three entries a reader can open from the
# home page. They are picked, not computed: the three largest themes are
# Akhirah, Kufr and Revelation, which says less about the section than Tawheed
# and Sabr do. The numbers beside them are counted from the data on every run.
# A surah, or [surah, ayah] with the name the ayah is known by.
QURAN_EXAMPLES = (1, 36, ((2, 255), "Ayat al-Kursi"))
PERSON_EXAMPLES = ("musa", "ibrahim", "maryam")
NAME_EXAMPLES = ("Ar-Rahman", "Al-Alim", "Al-Ghafur")
THEME_EXAMPLES = ("tawheed", "sabr", "akhirah")

# The arrangements named on the cards are the ones the site offers on each
# listing page (the table at the top of its indexPage.inline.ts). The two are
# changed together.


def _lede() -> str:
    """One line, above the cards: what the site is."""
    return (
        "The whole Quran, ayah by ayah: recitation, translation and tafsir for "
        "each one, and themes that link every verse to the others on the same "
        "idea.\n\n"
    )


def _meaning() -> str:
    """What the word means and where the Quran asks for it: below the cards."""
    reference = data.SURAHS[47].note_name(24)
    return (
        "\n**Tadabbur** (تدبّر) means reflecting deeply on the Quran: reading it "
        "slowly, pondering its meaning and taking its lessons to heart. It is the "
        "kind of reading the Quran itself asks of us:\n\n"
        "> “Then do they not reflect upon (yatadabbaroon) the Quran, or are there "
        f"locks upon [their] hearts?” ([[{reference}|Quran 47:24]])\n\n"
        "This site is a structured companion for that reflection. It covers all "
        "114 surahs and gives every ayah its Arabic text, English and Urdu "
        "translations, Urdu tafsir by Dr. Israr Ahmad and Maulana Wahiduddin "
        "Khan, and recitation audio. "
        "Each ayah is also tagged by theme, so from any single verse you can "
        "follow its ideas to every other place they appear in the Quran.\n"
    )


def _example(target: str, label: str, count: str) -> str:
    return f"    - [[{target}|{label}]] {count}\n"


def _card(target: str, label: str, description: str, examples: list) -> str:
    """
    One way in: a link, a line saying what is behind it, and under it a short
    list of entries from the section, each a link with its count.
    """
    return f"- [[{target}|{label}]] <small>{description}</small>\n" + "".join(examples)


def _quran_examples() -> list:
    lines = []
    for example in QURAN_EXAMPLES:
        if isinstance(example, int):
            surah = data.SURAHS[example]
            name = data.chapters_en[example - 1]["transliteration"]
            lines.append(_example(surah.index_path, name,
                                  notes.index_count(surah.total_ayaat, "ayah", "ayaat")))
        else:
            (surah, ayah), name = example
            lines.append(_example(data.SURAHS[surah].note_name(ayah), name,
                                  f'<span class="count">{surah}:{ayah}</span>'))
    return lines


def _person_examples() -> list:
    by_id = {person["id"]: person for person in data.personalities}
    return [
        _example(personalities.note_name(by_id[key]), by_id[key]["name_english"],
                 notes.index_count(personalities.ayah_count(by_id[key]), "ayah", "ayaat"))
        for key in PERSON_EXAMPLES
    ]


def _name_examples() -> list:
    by_name = {name["transliteration"]: name for name in data.asma_ul_husna}
    return [
        _example(asma_notes.note_name(by_name[key]), key,
                 notes.index_count(by_name[key]["quran_occurrences"], "time", "times"))
        for key in NAME_EXAMPLES
    ]


def _theme_examples() -> list:
    ayaat = themes.ayah_counts()
    return [
        _example(f"{config.THEMES_DIR}/{key}", connections.THEMES[key][1],
                 notes.index_count(ayaat[key], "ayah", "ayaat"))
        for key in THEME_EXAMPLES
    ]


def write_index() -> None:
    """
    The home page: one line on what the site is, the four ways in, then what
    Tadabbur means.

    The cards come before the prose. With the meaning and the ayah on top, the
    first card began 851px down a phone's 844px screen, and none of the four
    was on the first screen of a 1280px laptop either.
    """
    head = notes.frontmatter({"title": "Tadabbur", "cssclasses": "[home]"})
    ayaat = sum(surah.total_ayaat for surah in data.SURAHS.values())
    categories = len({theme[0] for theme in connections.THEMES.values()})

    cards = "".join([
        _card(f"{config.QURAN_DIR}/index", "The Quran",
              f"All {data.SURAH_COUNT} surahs and {ayaat:,} ayaat. Each ayah has "
              "its recitation, Arabic text, Urdu and English translations and two "
              "Urdu tafsirs.",
              _quran_examples()),
        _card(f"{config.PERSONALITIES_DIR}/index", "Personalities",
              f"The {len(data.personalities)} prophets, angels, jinn, companions, "
              "people and nations the Quran speaks about. Filter by name, or "
              "arrange by type, path, A–Z or most ayaat.",
              _person_examples()),
        _card(f"{config.ASMA_DIR}/index", "Asma Ul Husna",
              f"The {len(data.asma_ul_husna)} Names of Allah, each with its "
              "meaning in English and Urdu, its root and its ayaat. Filter by "
              "name, meaning or root, or arrange by meaning, 1–99, A–Z or most in "
              "the Quran.",
              _name_examples()),
        _card(f"{config.THEMES_DIR}/index", "Themes",
              f"{len(connections.THEMES)} themes in {categories} categories, each "
              "listing every ayah that carries it, in Quran order. Filter by "
              "name, or arrange by topic, A–Z or most ayaat.",
              _theme_examples()),
    ])

    notes.write_plain(config.VAULT_PATH, "index.md", head + _lede() + cards + _meaning())


def write_quran_index() -> None:
    """
    The Quran folder's own page: the surah cards.

    Left to itself the site would list the folder, 114 names sorted as text
    (1, 10, 100, 101 …). The cards are a `base` block in the page, so there
    is no separate Quran.base page beside it.
    """
    body = (
        notes.frontmatter({"title": notes.quote("The Quran")})
        + f"All {data.SURAH_COUNT} surahs, in order. Open one for its ayaat.\n\n"
        + f"```base\n{QURAN_BASE}```\n"
    )
    notes.write_plain(config.VAULT_PATH / config.QURAN_DIR, "index.md", body)
