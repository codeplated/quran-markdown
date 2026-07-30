# ══════════════════════════════════════════════════════════════════════════════
#  PERSONALITIES — Quran figures, angels, jinn, companions, groups
#  Drop these functions into main.py alongside the existing functions.
#
#  SETUP:
#    1. Add this line with the other load_json() calls at the top of main():
#         personalities = load_json("data/quran_personalities.json")
#
#    2. Call this at the end of main(), after asma_ul_husna_reader():
#         personalities_reader(personalities)
#
#  That's it. Everything else is self-contained below.
# ══════════════════════════════════════════════════════════════════════════════
import os
VAULT_PATH       = "../Mushaf" 
DEFAULT_PERSONALITY_PERSONAL = """
## 📝 Study Notes


## 💡 Personal Reflection


## 🔗 Related Ayaat & Personalities

"""

PATH_META = {
    "straight":  ("✅", "Straight Path",  "صراط مستقیم"),
    "deviated":  ("❌", "Deviated Path",   "گمراہی"),
    "mixed":     ("⚠️",  "Mixed — Erred then repented or complex", "مخلوط"),
    "unknown":   ("❓", "Unknown / Not enough information", "نامعلوم"),
}

TYPE_META = {
    "prophet":   ("🌙", "Prophet / Messenger",  "نبی / رسول"),
    "angel":     ("👼", "Angel",                "فرشتہ"),
    "jinn":      ("🔥", "Jinn",                 "جن"),
    "companion": ("⭐", "Companion",            "صحابی"),
    "person":    ("👤", "Person",               "شخصیت"),
    "group":     ("👥", "Group / Nation",       "قوم / گروہ"),
}


def _ayah_wikilink(surah: int, ayah: int) -> str:
    """
    Builds an Obsidian wikilink for a given surah/ayah using the same
    filename format as the ayah notes:
        [[2_255: Al-Baqarah البقرة]]
    Relies on eng_surah_names and arb_surah_names being populated by main().
    """
    try:
        en = eng_surah_names[surah - 1]
        ar = arb_surah_names[surah - 1]
        return f"[[{surah}_{ayah}: {en} {ar}]]"
    except IndexError:
        return f"[[{surah}_{ayah}]]"


def _personality_wikilink(personality_id: str, all_personalities: list) -> str:
    """
    Builds an Obsidian wikilink to another personality note.
    Falls back to the raw id if not found.
    """
    match = next((p for p in all_personalities if p["id"] == personality_id), None)
    if match:
        return f"[[{match['name_english']} — {match['name_arabic']}]]"
    return f"[[{personality_id}]]"


def build_personality_generated_block(p: dict, all_personalities: list) -> str:
    """
    Builds the script-owned section of a personality note.
    Wrapped in SENTINEL_START / SENTINEL_END so redeployment never
    overwrites personal notes below the sentinel.
    """
    path_emoji, path_en, path_ur = PATH_META.get(
        p["path"], ("❓", p["path"], p["path"])
    )
    type_emoji, type_en, type_ur = TYPE_META.get(
        p["type"], ("👤", p["type"], p["type"])
    )

    # ── Ayah wikilinks
    ayah_links = "\n".join(
        f"- {_ayah_wikilink(s, a)}"
        for s, a in p.get("mentioned_in", [])
    ) or "_No specific ayaat recorded._"

    # ── Connection wikilinks
    connection_links = "\n".join(
        f"- {_personality_wikilink(cid, all_personalities)}"
        for cid in p.get("connections", [])
    ) or "_No direct connections recorded._"

    # ── Also known as
    aliases = ", ".join(p.get("also_known_as", [])) or "—"

    # ── Lessons as a numbered list
    lessons = "\n".join(
        f"{i+1}. {lesson}"
        for i, lesson in enumerate(p.get("lessons", []))
    ) or "_No lessons recorded._"

    # ── Tags for YAML frontmatter
    tags_str = json.dumps(p.get("tags", []))

    return f"""{SENTINEL_START}
---
id: {p['id']}
name: {p['name_english']} / {p['name_arabic']} / {p['name_urdu']}
type: {type_en}
path: {path_en}
era: {p.get('era', '—')}
tags: {tags_str}
---

# {type_emoji} {p['name_english']} — {p['name_arabic']}
### {p['name_urdu']}

> **Also known as:** {aliases}

---

## {path_emoji} Path — {path_en} | {path_ur}

**Reason:** {p.get('path_reason', '—')}

---

## 📖 Story — English

{p.get('story_summary', '—')}

---

## 📖 کہانی — اردو

{p.get('urdu_summary', '—')}

---

## 💡 Lessons from the Quran

{lessons}

---

## 📍 Mentioned in Quran

{ayah_links}

---

## 🔗 Connected Personalities

{connection_links}

{SENTINEL_END}"""


def build_personality_note(p: dict, all_personalities: list) -> str:
    """Combines the generated block with the preserved personal section."""
    folder   = f"{VAULT_PATH}/Personalities"
    filename = f"{p['name_english']} — {p['name_arabic']}.md"
    filepath = os.path.join(folder, filename)

    generated = build_personality_generated_block(p, all_personalities)
    personal  = read_personal_section(filepath)

    return generated + personal, folder, filename


def personalities_reader(all_personalities: list) -> None:
    """
    Reads quran_personalities.json and writes one Obsidian note per entry.
    Also writes three index notes:
      - Personalities/_Index/All Personalities.md
      - Personalities/_Index/Straight Path.md
      - Personalities/_Index/Deviated Path.md
    """
    print()
    print("=" * 60)
    print("  Personalities → Obsidian")
    print("=" * 60)

    created = 0
    updated = 0

    # ── Write individual notes
    for p in all_personalities:
        content, folder, filename = build_personality_note(p, all_personalities)
        is_new = write_note(folder, filename, content)

        if is_new:
            created += 1
            print(f"  [NEW]     {filename}")
        else:
            updated += 1

    # ── Write index notes
    _write_personalities_indexes(all_personalities)

    print()
    print(f"  ✅  {created} created,  {updated} updated")
    print("=" * 60)


def _write_personalities_indexes(all_personalities: list) -> None:
    """Writes three index notes for navigating personalities in Obsidian."""

    index_folder = f"{VAULT_PATH}/Personalities/_Index"

    # ── 1. Master index — all personalities grouped by type
    lines = ["# 👥 Quranic Personalities — Master Index\n\n"]

    for ptype, (emoji, type_en, type_ur) in TYPE_META.items():
        group = [p for p in all_personalities if p["type"] == ptype]
        if not group:
            continue
        lines.append(f"\n## {emoji} {type_en} — {type_ur}\n\n")
        lines.append("| Name | Path | Era \n")
        lines.append("|------|------|-----\n")
        for p in group:
            path_emoji = PATH_META.get(p["path"], ("❓",))[0]
            link = f"[[{p['name_english']} — {p['name_arabic']}|{p['name_english']}]]"
            lines.append(
                f"| {link} | {p['name_arabic']} | "
                f"{path_emoji} {p['path'].capitalize()} | {p.get('era', '—')} |\n"
            )

    write_note(index_folder, "All Personalities.md", "".join(lines))
    print(f"  [INDEX]   Personalities/_Index/All Personalities.md")

    # ── 2. Straight path index
    straight = [p for p in all_personalities if p["path"] == "straight"]
    lines = ["# ✅ On the Straight Path — صراط مستقیم\n\n"]
    lines.append(f"**Total: {len(straight)}**\n\n")
    lines.append("| # | Name | Type | Era | Why |\n")
    lines.append("|---|------|------|-----|-----|\n")
    for i, p in enumerate(straight, 1):
        type_emoji = TYPE_META.get(p["type"], ("👤",))[0]
        link = f"[[{p['name_english']} — {p['name_arabic']}|{p['name_english']}]]"
        lines.append(
            f"| {i} | {link} | {type_emoji} {p['type'].capitalize()} | "
            f"{p.get('era', '—')} | {p.get('path_reason', '—')} |\n"
        )

    write_note(index_folder, "Straight Path.md", "".join(lines))
    print(f"  [INDEX]   Personalities/_Index/Straight Path.md")

    # ── 3. Deviated path index
    deviated = [p for p in all_personalities if p["path"] == "deviated"]
    lines = ["# ❌ Deviated from the Path — گمراہی\n\n"]
    lines.append(f"**Total: {len(deviated)}**\n\n")
    lines.append(
        "> These are the figures the Quran presents as warnings — "
        "understanding why they deviated is as important as understanding "
        "why the righteous succeeded.\n\n"
    )
    lines.append("| # | Name | Type | Era | Why Deviated |\n")
    lines.append("|---|------|------|-----|---------------|\n")
    for i, p in enumerate(deviated, 1):
        type_emoji = TYPE_META.get(p["type"], ("👤",))[0]
        link = f"[[{p['name_english']} — {p['name_arabic']}|{p['name_english']}]]"
        lines.append(
            f"| {i} | {link} | {type_emoji} {p['type'].capitalize()} | "
            f"{p.get('era', '—')} | {p.get('path_reason', '—')} |\n"
        )

    write_note(index_folder, "Deviated Path.md", "".join(lines))
    print(f"  [INDEX]   Personalities/_Index/Deviated Path.md")

    # ── 4. Mixed / complex path index
    mixed = [p for p in all_personalities if p["path"] == "mixed"]
    if mixed:
        lines = ["# ⚠️ Complex Path — Erred, Repented, or Both\n\n"]
        lines.append(f"**Total: {len(mixed)}**\n\n")
        lines.append(
            "> These figures neither fit cleanly into 'straight' nor 'deviated'. "
            "Their stories show the complexity of human moral life and the power of repentance.\n\n"
        )
        lines.append("| # | Name | Type | Era | Notes |\n")
        lines.append("|---|------|------|-----|-------|\n")
        for i, p in enumerate(mixed, 1):
            type_emoji = TYPE_META.get(p["type"], ("👤",))[0]
            link = f"[[{p['name_english']} — {p['name_arabic']}|{p['name_english']}]]"
            lines.append(
                f"| {i} | {link} | {type_emoji} {p['type'].capitalize()} | "
                f"{p.get('era', '—')} | {p.get('path_reason', '—')} |\n"
            )

        write_note(index_folder, "Mixed Path.md", "".join(lines))
        print(f"  [INDEX]   Personalities/_Index/Mixed Path.md")