"""
The 79 Quranic personalities — prophets, angels, jinn, companions, groups —
plus the master index and the per-path indexes under Personalities/Filtered/.

`type` and `path` are fields on each entry, not tags. The icons below label
the notes; they are unrelated to the theme vocabulary in quranConnections.py.
"""

import json

import config
from tadabbur import data, notes

PATH_META = {
    "straight": ("✅", "Straight Path", "صراط مستقیم"),
    "deviated": ("❌", "Deviated Path", "گمراہی"),
    "mixed":    ("⚠️", "Mixed — Erred, Repented, or Complex", "مخلوط"),
    "unknown":  ("❓", "Unknown", "نامعلوم"),
}

TYPE_META = {
    "prophet":   ("🌙", "Prophet / Messenger", "نبی / رسول"),
    "angel":     ("👼", "Angel", "فرشتہ"),
    "jinn":      ("🔥", "Jinn", "جن"),
    "companion": ("⭐", "Companion", "صحابی"),
    "person":    ("👤", "Person", "شخصیت"),
    "group":     ("👥", "Group / Nation", "قوم / گروہ"),
}

PATH_INDEX_FILES = {
    "straight": "Straight Path.md",
    "deviated": "Deviated Path.md",
    "mixed": "Mixed Path.md",
}

PATH_INTROS = {
    "deviated": (
        "> Understanding why they deviated is as important as understanding "
        "why the righteous succeeded. The Quran presents them as warnings, "
        "not as targets for hatred.\n\n"
    ),
    "mixed": (
        "> These figures neither fit cleanly into straight nor deviated. "
        "Their stories show the complexity of moral life and the power of repentance.\n\n"
    ),
}


def path_meta(person: dict) -> tuple:
    return PATH_META.get(person["path"], ("❓", person["path"], ""))


def type_meta(person: dict) -> tuple:
    return TYPE_META.get(person["type"], ("👤", person["type"], ""))


def note_name(person: dict) -> str:
    """Note name, which is also the wikilink target."""
    return f"{person['name_english']} — {person['name_arabic']}"


def _truncate(text: str, limit: int = 60) -> str:
    """Shortens a value so it does not blow out a table column."""
    return text if len(text) <= limit else text[:limit - 1] + "…"


def _table_link(person: dict) -> str:
    """
    A wikilink safe inside a table cell: the pipe in [[file|alias]] has to be
    escaped, or the parser reads it as a column break.
    """
    return f"[[{note_name(person)}\\|{person['name_english']}]]"


def _by_id(person_id: str, everyone: list) -> str:
    match = next((p for p in everyone if p["id"] == person_id), None)
    return f"[[{note_name(match)}]]" if match else f"[[{person_id}]]"


def build(person: dict, everyone: list) -> str:
    """Frontmatter plus the script-owned block for one personality."""
    path_icon, path_en, path_ur = path_meta(person)
    type_icon, type_en, _ = type_meta(person)

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
        "tags": json.dumps(person.get("tags", [])),
    })

    body = f"""# {type_icon} {person['name_english']} — {person['name_arabic']}
### {person['name_urdu']}

> **Also known as:** {aliases}

---

## {path_icon} Path — {path_en} | {path_ur}

**Reason:** {person.get('path_reason', '—')}

---

## 📖 Story — English

{person.get('story_summary', '—')}

---

## 📖 کہانی — اردو

{person.get('urdu_summary', '—')}

---

## 💡 Lessons from the Quran

{lessons}

---

## 📍 Mentioned in Quran

{ayah_links}

---

## 🔗 Connected Personalities

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
    for path in PATH_INDEX_FILES:
        _write_path_index(everyone, folder / "Filtered", path)

    return created, updated


def _write_master_index(everyone: list, folder) -> None:
    """One table per type, in the order TYPE_META declares."""
    lines = [
        "# 👥 Quranic Personalities — Master Index\n\n",
        f"**Total: {len(everyone)}**\n\n",
    ]

    for type_key, (type_icon, type_en, type_ur) in TYPE_META.items():
        group = [p for p in everyone if p["type"] == type_key]
        if not group:
            continue

        lines.append(f"\n## {type_icon} {type_en} — {type_ur}\n\n")
        lines.append("| # | Name | Path | Era |\n")
        lines.append("|---|------|------|-----|\n")

        for number, person in enumerate(group, 1):
            path_icon, path_en, _ = path_meta(person)
            era = _truncate(person.get("era", "—"), 35)
            lines.append(
                f"| {number} | {_table_link(person)} | {path_icon} {path_en} | {era} |\n"
            )

    notes.write_plain(folder, "index.md", "".join(lines))


def _write_path_index(everyone: list, folder, path: str) -> None:
    """
    One index per path. The reason text goes in a card below the table rather
    than in a cell, where its length would wreck the column alignment.
    """
    path_icon, path_en, path_ur = PATH_META[path]
    group = [p for p in everyone if p["path"] == path]
    if not group:
        return

    lines = [
        f"# {path_icon} {path_en} — {path_ur}\n\n",
        f"**Total: {len(group)}**\n\n",
        PATH_INTROS.get(path, ""),
        "| # | Name | Type | Era |\n",
        "|---|------|------|-----|\n",
    ]

    for number, person in enumerate(group, 1):
        type_icon, type_en, _ = type_meta(person)
        era = _truncate(person.get("era", "—"), 35)
        lines.append(
            f"| {number} | {_table_link(person)} | {type_icon} {type_en} | {era} |\n"
        )

    lines.append("\n---\n\n## Details\n\n")

    for person in group:
        type_icon, _, _ = type_meta(person)
        lines.append(f"### {type_icon} [[{note_name(person)}]] — {person['name_urdu']}\n\n")
        lines.append(f"**Era:** {person.get('era', '—')}\n\n")
        lines.append(f"**Reason:** {person.get('path_reason', '—')}\n\n")

        tags = person.get("tags", [])
        if tags:
            lines.append("**Tags:** " + " ".join(f"`{tag}`" for tag in tags) + "\n\n")

        lines.append("---\n\n")

    notes.write_plain(folder, PATH_INDEX_FILES[path], "".join(lines))
