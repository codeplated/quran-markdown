"""
The Themes section: one note per theme, and the page that lists them.

A theme is a tag, and the site serves a tag's page at /tags/<key>: every ayah
that carries it. A note at tags/<key>.md becomes the top of that page, so each
theme gets one, holding its name, Urdu name, category, count and description.
Those fields are also what the Themes page reads: tags/index.md holds one
table of every theme, with a tab that groups them by topic and a tab that
lists them A–Z.

The folder is called `tags` because that is the address the site serves
themes at; the title of its index note is what a reader sees, "Themes".
"""

import config
import quranConnections as connections
from tadabbur import data, notes

COUNTS_NOTE = ("*Notes* is the number of notes that carry a theme: the ayaat, "
               "plus any personality or Name of Allah notes that share it.")


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


def build(key: str, order: int, count: int) -> str:
    """
    One theme's note: the fields the Themes table shows, then its description,
    which the site puts above the theme's ayaat.

    `theme` is the name as a link to the theme's own page. A table can only
    link a row through a property, and written this way the column also sorts
    by name rather than by key. `order` is the theme's place in THEMES, which
    keeps the By Topic tab in the order the categories are declared.
    """
    category, title, urdu, description = connections.THEMES[key]

    head = notes.frontmatter({
        "title": notes.quote(title),
        "theme": notes.quote(f"[{title}]({config.THEMES_DIR}/{key})"),
        "urdu": notes.quote(urdu),
        "category": category,
        "notes": count,
        "order": order,
        "description": notes.quote(description),
    })
    return f"{head}{description}.\n"


def index_base() -> str:
    """
    The table on the Themes page, as a `base` block with two views.

    By Topic sorts by `order`, which runs through one category at a time, so
    the groups come out in the order THEMES declares them rather than A to Z.
    Only theme notes carry `theme`, which is what picks them out.
    """
    return (
        "filters:\n"
        "  and:\n"
        '    - file.hasProperty("theme")\n'
        "properties:\n"
        "  note.theme:\n"
        "    displayName: Theme\n"
        "  note.urdu:\n"
        "    displayName: Urdu\n"
        "views:\n"
        "  - type: table\n"
        "    name: By Topic\n"
        "    groupBy:\n"
        "      property: note.category\n"
        "      direction: ASC\n"
        "    order:\n"
        "      - note.theme\n"
        "      - note.urdu\n"
        "      - note.notes\n"
        "      - note.description\n"
        "    sort:\n"
        "      - property: note.order\n"
        "        direction: ASC\n"
        "  - type: table\n"
        "    name: A–Z\n"
        "    order:\n"
        "      - note.theme\n"
        "      - note.urdu\n"
        "      - note.category\n"
        "      - note.notes\n"
        "      - note.description\n"
        "    sort:\n"
        "      - property: note.title\n"
        "        direction: ASC\n"
    )


def write_index() -> None:
    """The Themes page: every theme in one table, by topic or A–Z."""
    categories = len({theme[0] for theme in connections.THEMES.values()})
    body = (
        notes.frontmatter({"title": "Themes"})
        + f"The {len(connections.THEMES)} themes of the Quran, in {categories} "
        "categories. See them by topic or A–Z, or click a column heading to sort "
        "by it. Open a theme for every ayah that carries it.\n\n"
        + f"```base\n{index_base()}```\n\n"
        + COUNTS_NOTE + "\n"
    )
    notes.write_plain(config.VAULT_PATH / config.THEMES_DIR, "index.md", body)


def generate() -> int:
    """Writes the Themes page and one note per theme. Returns how many themes."""
    counts = theme_counts()
    folder = config.VAULT_PATH / config.THEMES_DIR

    for order, key in enumerate(connections.THEMES, 1):
        notes.write_plain(folder, f"{key}.md", build(key, order, counts[key]))

    # A theme retired from THEMES would otherwise keep its row in the table.
    current = {f"{key}.md" for key in connections.THEMES} | {"index.md"}
    for note in folder.glob("*.md"):
        if note.name not in current:
            note.unlink()

    write_index()
    return len(connections.THEMES)
