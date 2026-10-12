"""
The 79 Quranic personalities — prophets, angels, jinn, companions, groups —
plus the Personalities page that lists them.

`type` and `path` are fields on each entry, not tags. Both are spelled out in
English and Urdu wherever they appear, so a note says what a figure is without
leaning on an icon to carry the meaning.

The Personalities page is written the way the Themes page is: every figure as
a line in a plain list under its type's heading. It reads as it is, in Obsidian
and with scripts off; the site lays the lists out in columns and adds a filter
and other arrangements (by path, A to Z, most ayaat) from what each line
already carries.
"""

import json

import config
import quranConnections as connections
from tadabbur import data, notes

# The class that says which listing this is; notes.INDEX_PAGE_CLASS says it is
# one. The site's styling and script look for both.
INDEX_CLASS = "people-index"

COUNTS_NOTE = ("The number beside a name is how many ayaat its page lists "
               "for it.")

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

# The headings on the Personalities page, one per type, in TYPE_META's order.
TYPE_HEADINGS = {
    "prophet":   "Prophets and Messengers",
    "angel":     "Angels",
    "jinn":      "Jinn",
    "companion": "Companions",
    "person":    "People",
    "group":     "Groups and Nations",
}

# A path's short name, as the Personalities page and a note's summary line say
# it, in the order the page's "By Path" arrangement shows them. PATH_META holds
# the long form, which a note's Path section spells out.
PATH_NAMES = {
    "straight": "Straight Path",
    "mixed":    "Mixed Path",
    "deviated": "Deviated Path",
}

# Said once under the lists, where each used to open a page of its own.
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

# Each path once had a page of its own under Personalities/Filtered/. The "By
# Path" arrangement replaces them; layout.migrate removes the old pages.
RETIRED_PATH_PAGES = ("Straight Path.md", "Deviated Path.md", "Mixed Path.md")
RETIRED_PATH_FOLDER = "Filtered"


def path_meta(person: dict) -> tuple:
    return PATH_META.get(person["path"], (person["path"], ""))


def type_meta(person: dict) -> tuple:
    return TYPE_META.get(person["type"], (person["type"], ""))


def path_name(person: dict) -> str:
    return PATH_NAMES.get(person["path"], path_meta(person)[0])


def type_heading(person: dict) -> str:
    return TYPE_HEADINGS.get(person["type"], type_meta(person)[0])


def note_name(person: dict) -> str:
    """Note name, which is also the wikilink target."""
    return f"{person['name_english']} — {person['name_arabic']}"


def ayah_count(person: dict) -> int:
    """How many ayaat the note lists under "Mentioned in Quran"."""
    return len(person.get("mentioned_in", []))


def listing_order(everyone: list) -> dict:
    """
    Each figure's place on the Personalities page, by id: types in the order
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
        "tags": json.dumps(person.get("tags", [])),
        "cssclasses": f"[{notes.PROFILE_CLASS}]",
    })

    body = f"""# {person['name_english']} — {person['name_arabic']}

{person['name_urdu']}

{summary(person)}

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


def summary(person: dict) -> str:
    """
    The lines under a note's heading: what the figure is, as a link to its
    type on the Personalities page; its path, its era and how many ayaat the
    note lists; then its other names and its themes, each a link to the theme.

    The site used to draw a properties box here, with the fields under their
    raw names (`id`, `path`, `era`) and the tags as keys (`#story_adam`).
    """
    type_en, _ = type_meta(person)
    facts = [
        f"[[{config.PERSONALITIES_DIR}/index#{type_heading(person)}|{type_en}]]",
        path_name(person),
        person.get("era", ""),
    ]
    count = ayah_count(person)
    if count:
        unit = "ayah" if count == 1 else "ayaat"
        facts.append(f"[[#Mentioned in Quran|{count} {unit}]]")

    lines = [" · ".join(fact for fact in facts if fact)]

    aliases = ", ".join(person.get("also_known_as", []))
    if aliases:
        lines.append(f"**Also known as:** {aliases}")

    themes = notes.theme_links(person.get("tags", []), connections.THEMES,
                               config.THEMES_DIR)
    if themes:
        lines.append(f"**Themes:** {themes}")

    return "\n>\n".join(f"> {line}" for line in lines)


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


def index_line(person: dict) -> str:
    """
    One figure on the Personalities page: the name as a link, the Arabic name,
    how many ayaat the note lists, and in the details its path, its era and its
    name in Urdu.

    Each part is in its own element so the site can lay them out, filter on
    them, sort by the count and group by the path. The path carries its place
    among the paths, which is the order the site shows them in. Arabic and Urdu
    are marked here, at the source: the two share most of their letters, so the
    site could only guess.
    """
    count = ayah_count(person)
    rank = list(PATH_NAMES).index(person["path"]) + 1 if person["path"] in PATH_NAMES else 0
    details = " · ".join(part for part in (
        f'<span class="path" data-rank="{rank}">{path_name(person)}</span>',
        person.get("era", ""),
        f'<span lang="ur">{person["name_urdu"]}</span>',
    ) if part)

    return " ".join(part for part in (
        f"- [[{note_name(person)}|{person['name_english']}]]",
        f'<span lang="ar">{person["name_arabic"]}</span>',
        notes.index_count(count, "ayah", "ayaat") if count else "",
        f"<small>{details}</small>",
    ) if part)


def index_body(everyone: list) -> str:
    """Every figure under a heading for its type, in listing_order."""
    order = listing_order(everyone)
    sections = {}
    for person in sorted(everyone, key=lambda person: order[person["id"]]):
        sections.setdefault(type_heading(person), []).append(index_line(person))

    return "\n\n".join(
        f"## {heading}\n\n" + "\n".join(lines)
        for heading, lines in sections.items()
    )


def _write_master_index(everyone: list, folder) -> None:
    """The Personalities page: every figure, by type."""
    lines = [
        notes.frontmatter({"title": "Personalities",
                           "cssclasses": notes.index_classes(INDEX_CLASS)}),
        f"The {len(everyone)} prophets, angels, companions, groups and other "
        "figures the Quran speaks about. Open one for its story, its lessons "
        "and the ayaat that mention it.\n\n",
        index_body(everyone) + "\n\n",
        COUNTS_NOTE + "\n",
    ]
    for key, name in PATH_NAMES.items():
        if key in PATH_NOTES:
            lines.append(f"\n**{name}.** {PATH_NOTES[key]}\n")

    notes.write_plain(folder, "index.md", "".join(lines))
