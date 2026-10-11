"""
The Themes section: one note per theme, and the page that lists them.

A theme is a tag, and the site serves a tag's page at /tags/<key>: every ayah
that carries it. A note at tags/<key>.md becomes the top of that page, so each
theme gets one, holding its name, Urdu name, category, count and description.

tags/index.md is the Themes page: every theme under its category, as plain
headings and lists. It reads as it is, in Obsidian and with scripts off; the
site lays the lists out in columns and adds a filter and other arrangements
(A to Z, most ayaat) on top, from what each line already carries.

The folder is called `tags` because that is the address the site serves
themes at; the title of its index note is what a reader sees, "Themes".
"""

import config
import quranConnections as connections
from tadabbur import data, notes

# The class the site's styling and script look for on the Themes page.
INDEX_CLASS = "themes-index"

COUNTS_NOTE = "The number beside a theme is how many ayaat carry it."


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


def ayah_counts() -> dict:
    """How many ayaat carry each theme. This is the count the Themes page shows."""
    counts = {key: 0 for key in connections.THEMES}

    for tags in connections.AYAH_TAGS.values():
        for tag in tags:
            if tag in counts:
                counts[tag] += 1

    return counts


def build(key: str, count: int) -> str:
    """
    One theme's note: its fields, then its description, which the site puts
    above the theme's ayaat.
    """
    category, title, urdu, description = connections.THEMES[key]

    head = notes.frontmatter({
        "title": notes.quote(title),
        "urdu": notes.quote(urdu),
        "category": category,
        "notes": count,
        "description": notes.quote(description),
    })
    return f"{head}{description}.\n"


def index_line(key: str, ayaat: int) -> str:
    """
    One theme on the Themes page: its name as a link, then its Urdu name, its
    ayah count and its description.

    The line leads with the Latin name so it reads left to right. The Urdu is
    marked as Urdu here, at the source: the site would otherwise have to guess
    the language from the letters, and a word like نفاق has none that only
    Urdu uses. Each part is in its own element so the site can lay them out,
    filter on them and sort by the count.
    """
    _, title, urdu, description = connections.THEMES[key]
    unit = "ayah" if ayaat == 1 else "ayaat"

    return (
        f"- [[{config.THEMES_DIR}/{key}|{title}]] "
        f'<span lang="ur">{urdu}</span> '
        f'<span class="count">{ayaat} <span class="unit">{unit}</span></span> '
        f"<small>{description}</small>"
    )


def index_body() -> str:
    """Every theme under a heading for its category, in the order THEMES declares."""
    ayaat = ayah_counts()
    sections = {}
    for key, theme in connections.THEMES.items():
        sections.setdefault(theme[0], []).append(index_line(key, ayaat[key]))

    return "\n\n".join(
        f"## {category}\n\n" + "\n".join(lines)
        for category, lines in sections.items()
    )


def write_index() -> None:
    """The Themes page: every theme, by category."""
    categories = len({theme[0] for theme in connections.THEMES.values()})
    body = (
        notes.frontmatter({"title": "Themes", "cssclasses": f"[{INDEX_CLASS}]"})
        + f"The {len(connections.THEMES)} themes of the Quran, in {categories} "
        "categories. Open a theme for every ayah that carries it.\n\n"
        + index_body() + "\n\n"
        + COUNTS_NOTE + "\n"
    )
    notes.write_plain(config.VAULT_PATH / config.THEMES_DIR, "index.md", body)


def generate() -> int:
    """Writes the Themes page and one note per theme. Returns how many themes."""
    counts = theme_counts()
    folder = config.VAULT_PATH / config.THEMES_DIR

    for key in connections.THEMES:
        notes.write_plain(folder, f"{key}.md", build(key, counts[key]))

    # A theme retired from THEMES would otherwise keep its note and its page.
    current = {f"{key}.md" for key in connections.THEMES} | {"index.md"}
    for note in folder.glob("*.md"):
        if note.name not in current:
            note.unlink()

    write_index()
    return len(connections.THEMES)
