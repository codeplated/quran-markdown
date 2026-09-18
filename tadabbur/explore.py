"""
The vault's front page: the thematic index, and the Obsidian base view that
shows one card per surah.
"""

import config
import quranConnections as connections
from tadabbur import data, notes

# One card per surah — matched by its first ayah note, "2_1: ...", from which
# the surah number is parsed so the cards sort in Mushaf order.
QURAN_BASE = """formulas:
  surah_number: number(file.name.split("_")[0])
views:
  - type: cards
    name: Surahs
    filters:
      and:
        - file.name.contains("_1:")
    order:
      - file.name
    sort:
      - property: formula.surah_number
        direction: ASC
    rowHeight: tall
    cardSize: 270
    image: note.image
    imageAspectRatio: 1
"""


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
        "**Tadabbur** (تدبّر) means to reflect deeply, to ponder — the kind of "
        "unhurried reading the Quran itself calls its readers to:\n\n"
        "> “Then do they not reflect upon (yatadabbaroon) the Quran, or are there "
        f"locks upon [their] hearts?” — [[{reference}|Quran 47:24]]\n\n"
        "This site is a structured companion for that reflection: every ayah of all "
        "114 surahs, laid out with recitation audio, Arabic text, Urdu and English "
        "translation, and cross-linked by theme — so you can move from a single verse "
        "to everywhere else in the Quran that verse’s ideas appear.\n\n"
    )


def write_index() -> None:
    """The master table of every theme, grouped by category."""
    counts = theme_counts()

    lines = [
        _intro(),
        "# 🗂 The General Topics of the Quran\n",
        "\n*Notes* counts how many notes carry each tag — ayaat plus the "
        "personality and Name of Allah notes that share it.\n",
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


def write_quran_base() -> None:
    """Writes Quran.base once; later edits made inside Obsidian are kept."""
    folder = config.VAULT_PATH / config.EXPLORE_DIR
    if (folder / "Quran.base").exists():
        return
    notes.write_plain(folder, "Quran.base", QURAN_BASE)
