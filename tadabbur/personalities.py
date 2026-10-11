"""
The 79 Quranic personalities — prophets, angels, jinn, companions, groups —
plus the Personalities page that lists them, with a tab for each path.

`type` and `path` are fields on each entry, not tags. Both are spelled out in
English and Urdu wherever they appear, so a note says what a figure is without
leaning on an icon to carry the meaning.
"""

import json

import config
from tadabbur import data, notes

PATH_META = {
    "straight": ("Straight Path", "صراط مستقیم"),
    "deviated": ("Deviated Path", "گمراہی"),
    "mixed":    ("Mixed — Erred, Repented, or Complex", "مخلوط"),
    "unknown":  ("Unknown", "نامعلوم"),
}

TYPE_META = {
    "prophet":   ("Prophet / Messenger", "نبی / رسول"),
    "angel":     ("Angel", "فرشتہ"),
    "jinn":      ("Jinn", "جن"),
    "companion": ("Companion", "صحابی"),
    "person":    ("Person", "شخصیت"),
    "group":     ("Group / Nation", "قوم / گروہ"),
}

# The tabs on the Personalities page after "All": the tab's name, and the path
# it shows.
PATH_TABS = (
    ("Straight Path", "straight"),
    ("Mixed Path", "mixed"),
    ("Deviated Path", "deviated"),
)

# Said once under the table, where each used to open a page of its own.
PATH_NOTES = {
    "deviated": (
        "Understanding why they deviated is as important as understanding "
        "why the righteous succeeded. The Quran presents them as warnings, "
        "not as targets for hatred."
    ),
    "mixed": (
        "These figures fit cleanly into neither the straight path nor the "
        "deviated one. Their stories show the complexity of moral life and the "
        "power of repentance."
    ),
}

# Each path once had a page of its own under Personalities/Filtered/. The tabs
# replace them; layout.migrate removes the old pages.
RETIRED_PATH_PAGES = ("Straight Path.md", "Deviated Path.md", "Mixed Path.md")
RETIRED_PATH_FOLDER = "Filtered"


def path_meta(person: dict) -> tuple:
    return PATH_META.get(person["path"], (person["path"], ""))


def type_meta(person: dict) -> tuple:
    return TYPE_META.get(person["type"], (person["type"], ""))


def note_name(person: dict) -> str:
    """Note name, which is also the wikilink target."""
    return f"{person['name_english']} — {person['name_arabic']}"


def listing_order(everyone: list) -> dict:
    """
    Each figure's place in the Personalities table, by id: types in the order
    TYPE_META declares, and within a type the order of the data, which runs
    roughly from the earliest figure to the latest.
    """
    rank = {key: position for position, key in enumerate(TYPE_META)}
    ordered = sorted(
        enumerate(everyone),
        key=lambda pair: (rank.get(pair[1]["type"], len(rank)), pair[0]),
    )
    return {person["id"]: place for place, (_, person) in enumerate(ordered, 1)}


def _by_id(person_id: str, everyone: list) -> str:
    match = next((p for p in everyone if p["id"] == person_id), None)
    return f"[[{note_name(match)}]]" if match else f"[[{person_id}]]"


def build(person: dict, everyone: list) -> str:
    """Frontmatter plus the script-owned block for one personality."""
    path_en, path_ur = path_meta(person)
    type_en, _ = type_meta(person)

    aliases = ", ".join(person.get("also_known_as", [])) or "—"

    ayah_links = "\n".join(
        f"- {data.wikilink(surah, ayah)}"
        for surah, ayah in person.get("mentioned_in", [])
    ) or "_No specific ayaat recorded._"

    connections = "\n".join(
        f"- {_by_id(person_id, everyone)}"
        for person_id in person.get("connections", [])
    ) or "_No connections recorded._"

    lessons = "\n".join(
        f"{number}. {lesson}"
        for number, lesson in enumerate(person.get("lessons", []), 1)
    ) or "_No lessons recorded._"

    head = notes.frontmatter({
        "id": person["id"],
        "name": f"\"{person['name_english']} / {person['name_arabic']} / {person['name_urdu']}\"",
        "type": type_en,
        "path": path_en,
        "era": f"\"{person.get('era', '—')}\"",
        # Not shown to the reader: it sorts the table on the Personalities page.
        "order": listing_order(everyone)[person["id"]],
        "tags": json.dumps(person.get("tags", [])),
    })

    body = f"""# {person['name_english']} — {person['name_arabic']}
### {person['name_urdu']}

> **Also known as:** {aliases}

---

## Path — {path_en} | {path_ur}

**Reason:** {person.get('path_reason', '—')}

---

## Story — English

{person.get('story_summary', '—')}

---

## کہانی — اردو

{person.get('urdu_summary', '—')}

---

## Lessons from the Quran

{lessons}

---

## Mentioned in Quran

{ayah_links}

---

## Connected Personalities

{connections}
"""

    return head + notes.wrap(body)


def generate() -> tuple:
    """Writes every personality note and its indexes. Returns (created, updated)."""
    everyone = data.personalities
    folder = config.VAULT_PATH / config.PERSONALITIES_DIR
    created = updated = 0

    for person in everyone:
        is_new = notes.write_note(
            folder,
            f"{note_name(person)}.md",
            build(person, everyone),
            notes.PERSONALITY_PERSONAL,
        )
        if is_new:
            created += 1
        else:
            updated += 1

    _write_master_index(everyone, folder)

    return created, updated


def _view(name: str, columns: tuple, path: str | None = None) -> str:
    """One tab of the Personalities table, as a view in a `base` block."""
    lines = ["  - type: table", f"    name: {name}"]
    if path:
        lines += ["    filters:", "      and:",
                  f'        - note.path == "{PATH_META[path][0]}"']
    else:
        # Rows are sorted by `order`, which runs through one type at a time,
        # so the groups come out in TYPE_META's order rather than A to Z.
        lines += ["    groupBy:", "      property: note.type", "      direction: ASC"]
    lines += ["    order:", *(f"      - {column}" for column in columns)]
    lines += ["    sort:", "      - property: note.order", "        direction: ASC"]
    return "\n".join(lines) + "\n"


def index_base() -> str:
    """
    The table on the Personalities page: every figure, and a tab per path.

    Only personality notes carry both `path` and `era`, which is what picks
    them out. Obsidian and the site both draw a `base` block in place, with
    the views as tabs and columns that sort when their heading is clicked.
    """
    return (
        "filters:\n"
        "  and:\n"
        '    - file.hasProperty("path")\n'
        '    - file.hasProperty("era")\n'
        "views:\n"
        + _view("All", ("file.name", "note.path", "note.era"))
        + "".join(_view(name, ("file.name", "note.type", "note.era"), path)
                  for name, path in PATH_TABS)
    )


def _write_master_index(everyone: list, folder) -> None:
    """The Personalities page: one table, filtered by path with tabs."""
    lines = [
        notes.frontmatter({"title": "Personalities"}),
        f"The {len(everyone)} prophets, angels, companions, groups and other "
        "figures the Quran speaks about. Choose a path to narrow the list, or "
        "click a column heading to sort by it.\n\n",
        f"```base\n{index_base()}```\n",
    ]
    for name, path in PATH_TABS:
        if path in PATH_NOTES:
            lines.append(f"\n**{name}.** {PATH_NOTES[path]}\n")

    notes.write_plain(folder, "index.md", "".join(lines))
