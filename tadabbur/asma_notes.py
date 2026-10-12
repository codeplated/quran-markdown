"""
The 99 Names of Allah.

These notes used to be written straight to disk with no GENERATED:START
sentinel and no read-back, so anything written under them was lost on the
next run. They now go through notes.write_note like every other note.

A note reads like a personality note: a header naming it in all three scripts,
its root and category, then the explanations. The data file keeps english,
arabic, urdu, transliteration and root apart, so the note keeps them apart
too — they used to be joined into a single `name` frontmatter string, which
the site could only print back as one long bidirectional line.

The Asma Ul Husna page is written the way the Themes page is: every Name as a
line in a plain list under its category's heading. It reads as it is, in
Obsidian and with scripts off; the site lays the lists out in columns and adds
a filter and other arrangements (1 to 99, A to Z, most in the Quran) from what
each line already carries.
"""

import json

import config
import quranConnections as connections
from tadabbur import data, notes

# The class that says which listing this is; notes.INDEX_PAGE_CLASS says it is
# one. The site's styling and script look for both.
INDEX_CLASS = "names-index"

COUNTS_NOTE = ("The number at the end of a line is how many times the Name "
               "appears in the Quran in this form. A Name with no number does "
               "not appear in this form.")

# Every category in the data begins with this. On a page of Names it is said
# once, by the page; a heading there keeps only what follows.
CATEGORY_PREFIX = "Names of "

# Reading order for the folder index: what Allah is in Himself, then how He
# governs, creates, knows, forgives, provides, judges, protects — ending with
# holiness and the Hereafter. Any category missing here still gets a section,
# appended at the end, so a new one in the data can never drop its Names.
CATEGORY_ORDER = (
    "Names of Essential Nature",
    "Names of Power & Sovereignty",
    "Names of Creation",
    "Names of Knowledge",
    "Names of Forgiveness & Mercy",
    "Names of Generosity & Provision",
    "Names of Justice",
    "Names of Peace & Security",
    "Names of Holiness",
    "Names of the Hereafter",
)

# A category holds up to 33 Names. Past a handful a related list stops being
# navigation and becomes a wall, so each note links only its nearest few.
RELATED_LIMIT = 8


def note_name(name: dict) -> str:
    """
    Note name, which is also the wikilink target and the page title on the
    site: '10 - Al-Jabbar ٱلْجَبَّار'. The number keeps the folder in the
    canonical order; the transliteration is what makes the note findable in
    English — in the title, the sidebar and search.
    """
    return f"{name['number']} - {name['transliteration']} {name['arabic']}"


def category_heading(category: str) -> str:
    """A category as a heading on the Asma Ul Husna page: 'Forgiveness & Mercy'."""
    if not category.startswith(CATEGORY_PREFIX):
        return category
    rest = category[len(CATEGORY_PREFIX):]
    return rest[:1].upper() + rest[1:]


def _meanings(value: str, separator: str = " · ") -> str:
    """The data joins multiple meanings with '/'; the note reads better without it."""
    return separator.join(part.strip() for part in value.split("/") if part.strip())


def _occurrences(count: int) -> str:
    """How often the Name appears in the Quran, in words."""
    if not count:
        return "not in this form"
    return "1 time" if count == 1 else f"{count} times"


def related(name: dict, everyone: list, limit: int = RELATED_LIMIT) -> list:
    """
    The other Names in the same category, nearest first by number.

    Nothing else in the vault links to a Name note, so without this the 99 sit
    unconnected in the site's graph. Large categories wrap around their own
    ends, so every Name is reachable from its neighbours instead of the first
    few collecting all the links.
    """
    group = sorted(
        (other for other in everyone if other["category"] == name["category"]),
        key=lambda other: other["number"],
    )
    others = [other for other in group if other["number"] != name["number"]]
    if len(others) <= limit:
        return others

    by_number = {other["number"]: other for other in group}
    ring = [other["number"] for other in group]
    start = ring.index(name["number"])

    picked = {}
    step = 1
    while len(picked) < limit:
        for offset in (step, -step):
            number = ring[(start + offset) % len(ring)]
            if number != name["number"] and len(picked) < limit:
                picked[number] = by_number[number]
        step += 1

    return sorted(picked.values(), key=lambda other: other["number"])


def build(name: dict, everyone: list) -> str:
    """Frontmatter plus the script-owned block for one Name."""
    ayah_links = "\n".join(
        f"- {data.wikilink(surah, ayah)}" for surah, ayah in name["key_ayaat"]
    ) or "_No ayaat recorded._"

    related_links = "\n".join(
        f"- [[{note_name(other)}]]" for other in related(name, everyone)
    )

    themes = notes.theme_links(name.get("tags", []), connections.THEMES,
                               config.THEMES_DIR)

    # What the Name is, in a few lines: its place among the Names, its category
    # as a link to it on the Asma Ul Husna page, how often it appears, its
    # root, and its themes by name. The site used to draw a properties box
    # here, with the fields under their raw names (`root_meaning`,
    # `quran_occurrences`) and the tags as keys.
    summary = [
        f"Name {name['number']} of {len(everyone)} · "
        f"[[{config.ASMA_DIR}/index#{category_heading(name['category'])}|{name['category']}]] · "
        f"In the Quran: {_occurrences(name['quran_occurrences'])}",
        f"**Root:** {name['root']} · {name['root_meaning']}",
    ]
    if themes:
        summary.append(f"**Themes:** {themes}")
    summary = "\n>\n".join(f"> {line}" for line in summary)

    head = notes.frontmatter({
        "number": name["number"],
        "english": notes.quote(_meanings(name["english"], ", ")),
        "arabic": notes.quote(name["arabic"]),
        "urdu": notes.quote(_meanings(name["urdu"], "، ")),
        "transliteration": notes.quote(name["transliteration"]),
        "root": notes.quote(name["root"]),
        "root_meaning": notes.quote(name["root_meaning"]),
        "category": notes.quote(name["category"]),
        "quran_occurrences": name["quran_occurrences"],
        "tags": json.dumps(name.get("tags", [])),
        "cssclasses": f"[{notes.PROFILE_CLASS}]",
    })

    body = f"""# {name['transliteration']} — {name['arabic']}

**{_meanings(name['english'])}**

{_meanings(name['urdu'], "، ")}

{summary}

---

## Meaning — English

{name['explanation']}

---

## معنی — اردو

{name['urdu_explanation']}

---

## In Daily Life

{name['daily_life']}

---

## Key Ayaat

{ayah_links}
"""

    # The single-Name category has no siblings to offer.
    if related_links:
        body += f"""
---

## Related Names

{related_links}
"""

    return head + notes.wrap(body)


def _categories(everyone: list) -> list:
    """Declared order first, then anything the data added since."""
    present = {name["category"] for name in everyone}
    known = [c for c in CATEGORY_ORDER if c in present]
    return known + sorted(present - set(known))


def index_line(name: dict) -> str:
    """
    One Name on the Asma Ul Husna page: its number, the Name as a link, the
    Name in Arabic, how many times it appears in the Quran, and in the details
    its meaning in English and Urdu and its root.

    Each part is in its own element so the site can lay them out, filter on
    them and sort by the number or the count. Arabic and Urdu are marked here,
    at the source: the two share most of their letters, so the site could only
    guess, and a meaning like صمد has no letter only Urdu uses.
    """
    count = name["quran_occurrences"]
    # A Name with two roots joins them with "and", which is not Arabic.
    roots = " and ".join(
        f'<span lang="ar">{root}</span>' for root in name["root"].split(" and ")
    )
    details = " · ".join((
        _meanings(name["english"], ", "),
        f'<span lang="ur">{_meanings(name["urdu"], "، ")}</span>',
        f'<span class="root">root {roots}</span>',
    ))

    return " ".join(part for part in (
        f'- <span class="num">{name["number"]}</span>',
        f"[[{note_name(name)}|{name['transliteration']}]]",
        f'<span lang="ar">{name["arabic"]}</span>',
        notes.index_count(count, "time", "times") if count else "",
        f"<small>{details}</small>",
    ) if part)


def index_body(everyone: list) -> str:
    """Every Name under a heading for its category, in traditional order."""
    sections = []
    for category in _categories(everyone):
        group = sorted(
            (name for name in everyone if name["category"] == category),
            key=lambda name: name["number"],
        )
        sections.append(
            f"## {category_heading(category)}\n\n"
            + "\n".join(index_line(name) for name in group)
        )
    return "\n\n".join(sections)


def _write_master_index(everyone: list, folder) -> None:
    """
    The folder's own page: every Name, by category.

    Without an index.md the site falls back to listing the folder, which sorts
    the notes as text — 1, 10, 11, … 2 — and says nothing about any of them.
    """
    body = (
        notes.frontmatter({"title": config.ASMA_DIR,
                           "cssclasses": notes.index_classes(INDEX_CLASS)})
        + f"The {len(everyone)} Names of Allah, grouped by what they tell us. "
        "Open a Name for its meaning in English and Urdu, the root it grows "
        "from and the ayaat it appears in.\n\n"
        + index_body(everyone) + "\n\n"
        + COUNTS_NOTE + "\n"
    )
    notes.write_plain(folder, "index.md", body)


def generate() -> tuple:
    """Writes one note per Name. Returns (created, updated)."""
    everyone = data.asma_ul_husna
    folder = config.VAULT_PATH / config.ASMA_DIR
    created = updated = 0

    for name in everyone:
        # Notes were once named '10 - ٱلْجَبَّار.md', with no English in the
        # title. Move the old note first, so whatever the reader wrote under it
        # survives the rename instead of being stranded in the old file.
        notes.rename_note(
            folder,
            f"{name['number']} - {name['arabic']}.md",
            f"{note_name(name)}.md",
        )

        is_new = notes.write_note(
            folder,
            f"{note_name(name)}.md",
            build(name, everyone),
            notes.ASMA_PERSONAL,
        )
        if is_new:
            created += 1
        else:
            updated += 1

    _write_master_index(everyone, folder)

    return created, updated
