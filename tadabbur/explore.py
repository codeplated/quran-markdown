"""
The vault's front page: the thematic index, the same themes A–Z, and the
Obsidian base view that shows one card per surah.
"""

import config
import quranConnections as connections
from tadabbur import data, notes

# Both theme tables carry the same counts, so both explain them the same way.
COUNTS_NOTE = ("*Notes* is the number of notes that carry each tag: the ayaat, "
               "plus any personality or Name of Allah notes that share it.\n")

# The A–Z themes note. Its filename is the sidebar label, its wikilink target
# and its page title, and three pages link to it, so it is named once here.
THEMES_NOTE = "Themes"
THEMES_PATH = f"{config.EXPLORE_DIR}/{THEMES_NOTE}"

# One card per surah, linking to the surah's index note. Every folder index
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

# Quran.base as earlier versions wrote it. A vault still holding one of these
# unchanged gets the current file; one edited inside Obsidian is left alone.
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


def theme_counts() -> dict:
    """How many notes carry each theme — ayaat plus personalities plus Names."""
    counts = {key: 0 for key in connections.THEMES}

    tag_lists = (
        list(connections.AYAH_TAGS.values())
        + [person.get("tags", []) for person in data.personalities]
        + [name.get("tags", []) for name in data.asma_ul_husna]
    )

    for tags in tag_lists:
        for tag in tags:
            if tag in counts:
                counts[tag] += 1

    return counts


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


def write_index() -> None:
    """The master table of every theme, grouped by category."""
    counts = theme_counts()

    lines = [
        _intro(),
        "# The General Topics of the Quran\n",
        "\n" + COUNTS_NOTE,
    ]

    category = None
    row = 0

    for key, (theme_category, title, urdu_title, description) in connections.THEMES.items():
        if theme_category != category:
            category = theme_category
            lines.append(f"\n### {theme_category}\n")
            lines.append("| # | Topic | Tag | Notes | Description |\n")
            lines.append("|---|-------|-----|-------|-------------|\n")

        row += 1
        lines.append(
            f"| {row} | **{title}** {urdu_title} "
            f"| [#{key}](tags/{key}) "
            f"| {counts[key]} "
            f"| {description} |\n"
        )

    notes.write_plain(config.VAULT_PATH, "index.md", "".join(lines))


def write_themes_index() -> None:
    """
    Every theme A–Z.

    The front page groups the themes by subject, which is the order for a
    reader following an idea. A reader who already has the name of a topic
    needs the other order, and the site's own /tags page gives only that: bare
    tag names, no Urdu, no counts, and nothing saying what a tag covers.

    A note rather than a section of the front page, because the sidebar is a
    file tree — only a real file puts Themes under Explore — and because the
    two orders of 139 rows on one page would bury whichever came second.
    """
    counts = theme_counts()

    lines = [
        "# Themes A–Z\n",
        f"\nAll {len(connections.THEMES)} themes in alphabetical order.\n",
        "\n" + COUNTS_NOTE,
        "\n| Topic | Tag | Category | Notes | Description |\n",
        "|-------|-----|----------|-------|-------------|\n",
    ]

    alphabetical = sorted(connections.THEMES.items(), key=lambda item: item[1][1].lower())

    for key, (category, title, urdu_title, description) in alphabetical:
        lines.append(
            f"| **{title}** {urdu_title} "
            f"| [#{key}](tags/{key}) "
            f"| {category} "
            f"| {counts[key]} "
            f"| {description} |\n"
        )

    notes.write_plain(config.VAULT_PATH / config.EXPLORE_DIR,
                      f"{THEMES_NOTE}.md", "".join(lines))


def write_explore_index() -> None:
    """
    The Explore folder's own page.

    Left to itself the site lists the folder — two links, no counts, and no
    Quran.base at all, because a folder listing leaves .base files out. That
    hides the surah grid from the one page meant to lead to it.
    """
    lines = [
        "# Explore\n\n",
        "Ways into the Quran beyond reading it surah by surah.\n\n",
        "| Section | What it holds |\n",
        "|---------|---------------|\n",
        f"| [[{config.EXPLORE_DIR}/Quran.base\\|The Quran]] "
        f"| all {data.SURAH_COUNT} surahs as cards, in order |\n",
        f"| [[{config.ASMA_DIR}/index\\|Asma ul Husna]] "
        f"| the {len(data.asma_ul_husna)} Names, grouped by what they tell us |\n",
        f"| [[{config.PERSONALITIES_DIR}/index\\|Personalities]] "
        f"| {len(data.personalities)} prophets, companions, groups and figures |\n",
        f"| [[{THEMES_PATH}\\|Themes]] "
        f"| every one of the {len(connections.THEMES)} themes, A–Z |\n",
    ]

    notes.write_plain(config.VAULT_PATH / config.EXPLORE_DIR, "index.md", "".join(lines))


def write_quran_base() -> None:
    """
    Writes Quran.base once; later edits made inside Obsidian are kept. A file
    still exactly as an earlier version wrote it is replaced, since it no
    longer matches the ayah note names.
    """
    folder = config.VAULT_PATH / config.EXPLORE_DIR
    existing = folder / "Quran.base"
    if existing.exists() and existing.read_text(encoding="utf-8") not in OLD_QURAN_BASES:
        return
    notes.write_plain(folder, "Quran.base", QURAN_BASE)
