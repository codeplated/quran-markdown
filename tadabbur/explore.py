"""
The home page and the Quran's own page, with one card per surah.

The home page offers four ways in, The Quran, Personalities, Asma Ul Husna and
Themes. They are the same four the site's left panel shows as its parents.
"""

import config
import quranConnections as connections
from tadabbur import data, notes

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


def _intro() -> str:
    reference = data.SURAHS[47].note_name(24)
    return (
        "**Tadabbur** (تدبّر) means reflecting deeply on the Quran: reading it "
        "slowly, pondering its meaning and taking its lessons to heart. It is the "
        "kind of reading the Quran itself asks of us:\n\n"
        "> “Then do they not reflect upon (yatadabbaroon) the Quran, or are there "
        f"locks upon [their] hearts?” ([[{reference}|Quran 47:24]])\n\n"
        "This site is a structured companion for that reflection. It covers all "
        "114 surahs and gives every ayah its Arabic text, English and Urdu "
        "translations, Urdu tafsir by Dr. Israr Ahmad and Maulana Wahiduddin "
        "Khan, and recitation audio. "
        "Each ayah is also tagged by theme, so from any single verse you can "
        "follow its ideas to every other place they appear in the Quran.\n\n"
    )


def _card(target: str, label: str, description: str) -> str:
    """One way in: a link, and a line saying what is behind it."""
    return f"- [[{target}|{label}]] <small>{description}</small>\n"


def write_index() -> None:
    """The home page: what Tadabbur is, then the four ways in."""
    head = notes.frontmatter({"title": "Tadabbur", "cssclasses": "[home]"})

    cards = "".join([
        _card(f"{config.QURAN_DIR}/index", "The Quran",
              f"All {data.SURAH_COUNT} surahs. Open a surah for its ayaat, each "
              "with recitation, translations and tafsir."),
        _card(f"{config.PERSONALITIES_DIR}/index", "Personalities",
              f"The {len(data.personalities)} prophets, companions, groups and "
              "figures the Quran speaks about."),
        _card(f"{config.ASMA_DIR}/index", "Asma Ul Husna",
              f"The {len(data.asma_ul_husna)} Names of Allah, with their "
              "meanings, roots and the ayaat they appear in."),
        _card(f"{config.THEMES_DIR}/index", "Themes",
              f"The {len(connections.THEMES)} themes of the Quran, by topic or "
              "A–Z, each listing every ayah that carries it."),
    ])

    notes.write_plain(config.VAULT_PATH, "index.md", head + _intro() + cards)


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
