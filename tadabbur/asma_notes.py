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
"""

import json

import config
from tadabbur import data, notes

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


def _table_link(name: dict) -> str:
    """
    A wikilink safe inside a table cell: the pipe in [[file|alias]] has to be
    escaped, or the parser reads it as a column break.
    """
    return f"[[{note_name(name)}\\|{name['transliteration']} {name['arabic']}]]"


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
    })

    body = f"""# {name['transliteration']} — {name['arabic']}
### {_meanings(name['english'])}
#### {_meanings(name['urdu'])}

> **Root:** {name['root']} — {name['root_meaning']}
>
> **Category:** {name['category']} · **In the Quran:** {_occurrences(name['quran_occurrences'])}

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


def _write_master_index(everyone: list, folder) -> None:
    """
    The folder's own page, grouped by category.

    Without an index.md the site falls back to listing the folder, which sorts
    the notes as text — 1, 10, 11, … 2 — and says nothing about any of them.
    """
    lines = [
        f"# Asma ul Husna — The 99 Names\n\n",
        f"**Total: {len(everyone)}**\n\n",
        "The Names in their traditional order, grouped by what they tell us. "
        "Each links to its own note: the meaning in English and Urdu, the root "
        "it grows from, and the ayaat it appears in.\n\n",
    ]

    for category in _categories(everyone):
        group = sorted(
            (name for name in everyone if name["category"] == category),
            key=lambda name: name["number"],
        )

        lines.append(f"\n## {category} — {len(group)}\n\n")
        lines.append("| # | Name | Meaning | Root |\n")
        lines.append("|---|------|---------|------|\n")

        for name in group:
            lines.append(
                f"| {name['number']} | {_table_link(name)} "
                f"| {_meanings(name['english'])} | {name['root']} |\n"
            )

    notes.write_plain(folder, "index.md", "".join(lines))


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
