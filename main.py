import json
import os
import re

import quranConnections as connections



VAULT_PATH       = "../Mushaf"          # root of your Obsidian vault
#AUDIO_BASE_PATH  = "./data/audio"
AUDIO_BASE_PATH  = "./data/AlafasyAudio"       # where audio files live on disk
AUDIO_EXT        = ".mp3"

# USE_EXTERNAL_LINK = True  → <audio> tag with absolute file:// path (Option B)
# USE_EXTERNAL_LINK = False → ![[vault/relative/path]] embed    (Option A)
USE_EXTERNAL_LINK = True

SENTINEL_START = "<!-- GENERATED:START -->"
SENTINEL_END   = "<!-- GENERATED:END -->"

BISMILLAH = "بِسۡمِ ٱللَّهِ ٱلرَّحۡمَٰنِ ٱلرَّحِيمِ"
#BISMILLAH = "﷽"

DEFAULT_PERSONAL_SECTION = """
## 📝 Tafsir Notes


## 💡 Personal Reflection


## 🔗 Thematic Links

"""

# ══════════════════════════════════════════════════════════════════════════════
#  DATA LOADING
# ══════════════════════════════════════════════════════════════════════════════

def load_json(path: str) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)

quran      = load_json("data/quran.json")
english    = load_json("data/en.json")
urdu       = load_json("data/ur.json")
urChapters = load_json("data/chapters/ur.json")
enChapters = load_json("data/chapters/en.json")
asmaUlHusna = load_json("data/asma_ul_husna.json")
personalities = load_json("data/quran_personalities.json")
eng_surah_names = []
arb_surah_names = []

# ══════════════════════════════════════════════════════════════════════════════
#  AUDIO HELPERS
# ══════════════════════════════════════════════════════════════════════════════

def asma_ul_husna_reader() -> None:
    for name in asmaUlHusna:
        number = name["number"]
        arabic = name["arabic"]
        transliteration = name["transliteration"]
        english = name["english"]
        urdu = name["urdu"]
        root = name["root"]
        root_meaning = name["root_meaning"]
        category = name["category"]
        explanation = name["explanation"]
        urdu_explanation = name["urdu_explanation"]
        daily_life = name["daily_life"]
        quran_occurrences = name["quran_occurrences"]
        key_ayaat = name["key_ayaat"]

        content = build_asma_ul_husna_note(
            number,
            arabic,
            transliteration,
            english,
            urdu,
            root,
            root_meaning,
            category,
            explanation,
            urdu_explanation,
            daily_life,
            quran_occurrences,
            key_ayaat
        )
        folder = f"{VAULT_PATH}/Asma Ul Husna"
        filename     = f"{number} - {arabic}.md"
        write_note(folder, filename, content)

def build_asma_ul_husna_note(
    number:     int,
    arabic:      str,
    transliteration:   int,
    english:       str,
    urdu:       str,
    root:       str,
    root_meaning:  str,
    category:          list,
    explanation:     str,
    urdu_explanation:     str,
    daily_life:  str,
    quran_occurrences:str,
    key_ayaat:   list,
    ) -> str:
    ayat_links = []
    for k in key_ayaat:
        ayat_link = f"[[{k[0]}_{k[1]}: {eng_surah_names[k[0]-1]} {arb_surah_names[k[0]-1]}]]"
        ayat_links.append(ayat_link)
    return f"""---
number: {number}
name: {english} / {arabic} / {urdu} / {transliteration} / {root}
root_meaning: {root_meaning}
category: {category}
quran_occurrences: {quran_occurrences}
key_ayaat: {key_ayaat}
---
## English Explanation 

{explanation}

## Urdu Explaination
 
{urdu_explanation}

## Daily Life

{daily_life}

## Key Ayaat

{"\n".join(ayat_links)}

{SENTINEL_END}

## Personal Notes
"""
    

def audio_path(surah_num: int, ayah_num: int) -> str:
    """Returns the relative audio path: 017/001.mp3"""
    folder = str(surah_num).zfill(3)
    file   = str(ayah_num).zfill(3)
    return f"{folder}/{file}{AUDIO_EXT}"

def alafasy_audio_path(surah_num: int, ayah_num: int) -> str:
    """Returns the relative audio path: 017001.mp3"""
    folder = str(surah_num).zfill(3)
    file   = str(ayah_num).zfill(3)
    return f"{folder}{file}{AUDIO_EXT}"


def audio_embed(surah_num: int, ayah_num: int) -> str:
    """Returns the Obsidian markdown snippet to play the audio."""
    rel_path = alafasy_audio_path(surah_num, ayah_num)

    if USE_EXTERNAL_LINK:
        abs_path = os.path.abspath(
            os.path.join(AUDIO_BASE_PATH, rel_path)
        ).replace("\\", "/")
        return f'<audio controls src="file://{abs_path}"></audio>'
    else:
        return f"![[audio/{rel_path}]]"

# ══════════════════════════════════════════════════════════════════════════════
#  TAFSIR LOADER
# ══════════════════════════════════════════════════════════════════════════════

def load_tafsir_ur(surah_num: str, ayah_num: int) -> str:
    path = f"data/ur-tazkirul-quran/{surah_num}/{ayah_num}.json"
    try:
        data = load_json(path)
        return data.get("text", "")
    except FileNotFoundError:
        return "_Tafsir not available for this ayah._"

# ══════════════════════════════════════════════════════════════════════════════
#  SENTINEL — PERSONAL SECTION PRESERVATION
# ══════════════════════════════════════════════════════════════════════════════

def read_personal_section(filepath: str) -> str:
    """
    Returns the user-owned content that lives after SENTINEL_END.

    - New file          → returns the default blank template
    - Sentinel present  → returns everything after SENTINEL_END unchanged
    - Legacy file       → migrates old sections on first run (nothing lost)
    """
    if not os.path.exists(filepath):
        return DEFAULT_PERSONAL_SECTION

    content = open(filepath, encoding="utf-8").read()

    if SENTINEL_END in content:
        after = content.split(SENTINEL_END, 1)[1]
        return after if after.strip() else DEFAULT_PERSONAL_SECTION

    # ── One-time migration for files created before sentinels were introduced
    return _migrate_legacy_personal(content)


def _migrate_legacy_personal(content: str) -> str:
    """
    Extracts personal sections from old-format notes (no sentinels).
    Called exactly once per file during the first sentinel-aware redeploy.
    """
    headings = ["## Tafsir Notes", "## Personal Reflection", "## 🔗 Thematic Links"]
    extracted = []

    for heading in headings:
        match = re.search(
            rf"({re.escape(heading)}.*?)(?=\n## |\Z)",
            content,
            re.DOTALL,
        )
        if match:
            extracted.append(match.group(1).strip())

    if extracted:
        return "\n\n" + "\n\n".join(extracted) + "\n"

    return DEFAULT_PERSONAL_SECTION

# ══════════════════════════════════════════════════════════════════════════════
#  NOTE BUILDERS
# ══════════════════════════════════════════════════════════════════════════════

def build_ayah_text(surah_num: int, ayah_num: int, raw_text: str) -> str:
    """Prepends Bismillah to the first ayah of every surah except Al-Fatihah (1) and At-Tawbah (9)."""
    if surah_num > 1 and surah_num != 9 and ayah_num == 1:
        return f"{BISMILLAH}\n\n{raw_text}"
    return raw_text


def build_generated_block(
    surah_num:     int,
    ayah_num:      int,
    total_ayahs:   int,
    en_name:       str,
    ar_name:       str,
    ur_name:       str,
    chapter_type:  str,
    tags:          list,
    ayah_text:     str,
    urdu_text:     str,
    english_text:  str,
    tafsir_text:   str,
    prev_link:     str,
    next_link:     str,
) -> str:
    """Returns the script-owned block, wrapped in sentinel markers."""

    audio   = audio_embed(surah_num, ayah_num)
    tag_str = json.dumps(tags)           # produces ["tag1", "tag2"] for YAML

    return f"""---
surah: {surah_num} / 114
surah_name: {en_name} / {ar_name} / {ur_name}
ayah: {ayah_num} / {total_ayahs}
type: {chapter_type}
tags: {tag_str}
---
{SENTINEL_START}
## 🔊 Recitation

{audio}
**Next:** {next_link}

---

## Arabic

{ayah_text}

---

## 🇵🇰 Urdu

{urdu_text}

---

## 🇬🇧 English

{english_text}

---

## 🇵🇰 Tafsir — Bayan ul Quran

{tafsir_text}

---

## Connections

- **Previous:** {prev_link}
- **Next:** {next_link}
- **Thematic:** *(add links here)*

{SENTINEL_END}"""


def write_note(folder: str, filename: str, content: str) -> bool:
    """Writes content to folder/filename. Returns True if the file is new."""
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, filename)
    is_new   = not os.path.exists(filepath)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    return is_new

# ══════════════════════════════════════════════════════════════════════════════
#  INDEX BUILDER
# ══════════════════════════════════════════════════════════════════════════════

def create_index():
    """Generates the master thematic index note."""
    lines    = ["# 🗂 The General Topics of the Quran\n"]
    counter  = 0
    category = None

    for key, (emoji, theme, en_title, ur_title, description) in connections.THEMES.items():
        if theme != category:
            category = theme
            lines.append(f"\n### {theme}\n")
            lines.append("| # | Topic | Description |\n")
            lines.append("|---|-------|-------------|\n")
        counter += 1
        lines.append(f"| {counter} | {emoji} **{en_title}** {ur_title} | {description} |\n")

    content = "".join(lines)
    write_note(f"{VAULT_PATH}/0 - Index", "index.md", content)
    print("  [INDEX]   0 - Index/index.md")

# ══════════════════════════════════════════════════════════════════════════════
#  PERSONALITIES — Quran figures, angels, jinn, companions, groups
#  Drop these functions into main.py alongside the existing functions.
#
#  SETUP — two lines to add to main.py:
#
#  1. With the other load_json() calls at module level:
#       personalities = load_json("data/quran_personalities.json")
#
#  2. At the end of main(), after asma_ul_husna_reader():
#       personalities_reader(personalities)
# ══════════════════════════════════════════════════════════════════════════════

DEFAULT_PERSONALITY_PERSONAL = """
## 📝 Study Notes


## 💡 Personal Reflection


## 🔗 Related Ayaat & Personalities

"""

PATH_META = {
    "straight": ("✅", "Straight Path",  "صراط مستقیم"),
    "deviated": ("❌", "Deviated Path",  "گمراہی"),
    "mixed":    ("⚠️",  "Mixed — Erred, Repented, or Complex", "مخلوط"),
    "unknown":  ("❓", "Unknown",        "نامعلوم"),
}

TYPE_META = {
    "prophet":   ("🌙", "Prophet / Messenger", "نبی / رسول"),
    "angel":     ("👼", "Angel",               "فرشتہ"),
    "jinn":      ("🔥", "Jinn",                "جن"),
    "companion": ("⭐", "Companion",           "صحابی"),
    "person":    ("👤", "Person",              "شخصیت"),
    "group":     ("👥", "Group / Nation",      "قوم / گروہ"),
}


def _truncate(text: str, limit: int = 60) -> str:
    """Truncates long text for table cells without breaking markdown."""
    return text if len(text) <= limit else text[:limit - 1] + "…"


def _table_link(p: dict) -> str:
    """
    Wikilink alias safe for use inside a markdown table cell.
    The pipe | in [[file|alias]] must be escaped as \\| inside table cells,
    otherwise markdown parsers treat it as a column separator.
    """
    return f"[[{p['name_english']} — {p['name_arabic']}\\|{p['name_english']}]]"


def _ayah_wikilink(surah: int, ayah: int) -> str:
    """
    Builds an Obsidian wikilink for an ayah using the same filename format
    as the ayah notes:  [[2_255: Al-Baqarah البقرة]]
    Relies on eng_surah_names / arb_surah_names populated by main().
    """
    try:
        en = eng_surah_names[surah - 1]
        ar = arb_surah_names[surah - 1]
        return f"[[{surah}_{ayah}: {en} {ar}]]"
    except IndexError:
        return f"[[{surah}_{ayah}]]"


def _personality_wikilink(pid: str, all_personalities: list) -> str:
    """Wikilink to another personality note by its id."""
    match = next((p for p in all_personalities if p["id"] == pid), None)
    if match:
        return f"[[{match['name_english']} — {match['name_arabic']}]]"
    return f"[[{pid}]]"


# ── Note builder ───────────────────────────────────────────────────────────────

def _build_personality_generated_block(p: dict, all_personalities: list) -> str:
    """Script-owned content wrapped in sentinels."""

    path_emoji, path_en, path_ur = PATH_META.get(p["path"], ("❓", p["path"], ""))
    type_emoji, type_en, type_ur = TYPE_META.get(p["type"], ("👤", p["type"], ""))

    aliases = ", ".join(p.get("also_known_as", [])) or "—"
    tags_str = json.dumps(p.get("tags", []))

    # Ayah wikilinks — one per line as a list
    ayah_links = "\n".join(
        f"- {_ayah_wikilink(s, a)}"
        for s, a in p.get("mentioned_in", [])
    ) or "_No specific ayaat recorded._"

    # Connection wikilinks
    connection_links = "\n".join(
        f"- {_personality_wikilink(cid, all_personalities)}"
        for cid in p.get("connections", [])
    ) or "_No connections recorded._"

    # Lessons as numbered list
    lessons = "\n".join(
        f"{i + 1}. {lesson}"
        for i, lesson in enumerate(p.get("lessons", []))
    ) or "_No lessons recorded._"

    return f"""{SENTINEL_START}
---
id: {p['id']}
name: "{p['name_english']} / {p['name_arabic']} / {p['name_urdu']}"
type: {type_en}
path: {path_en}
era: "{p.get('era', '—')}"
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


def _get_personality_filepath(p: dict) -> tuple:
    """Returns (folder, filename, filepath) for a personality note."""
    folder   = f"{VAULT_PATH}/Personalities"
    filename = f"{p['name_english']} — {p['name_arabic']}.md"
    filepath = os.path.join(folder, filename)
    return folder, filename, filepath


# ── Main reader ────────────────────────────────────────────────────────────────

def personalities_reader(all_personalities: list) -> None:
    """
    Reads the personalities list and writes one Obsidian note per entry,
    then writes four index notes under Personalities/_Index/.
    """
    print()
    print("=" * 60)
    print("  Personalities → Obsidian")
    print("=" * 60)

    created = 0
    updated = 0

    for p in all_personalities:
        folder, filename, filepath = _get_personality_filepath(p)

        generated = _build_personality_generated_block(p, all_personalities)
        personal  = read_personal_section(filepath)
        is_new    = write_note(folder, filename, generated + personal)

        if is_new:
            created += 1
            print(f"  [NEW]     {filename}")
        else:
            updated += 1

    _write_personalities_indexes(all_personalities)

    print()
    print(f"  ✅  {created} created,  {updated} updated")
    print("=" * 60)


# ── Index builders ─────────────────────────────────────────────────────────────

def _write_personalities_indexes(all_personalities: list) -> None:
    """Writes four clean index notes."""

    folder = f"{VAULT_PATH}/Personalities/_Index"

    _write_all_index(all_personalities, folder)
    _write_path_index(all_personalities, folder, "straight")
    _write_path_index(all_personalities, folder, "deviated")
    _write_path_index(all_personalities, folder, "mixed")


def _write_all_index(all_personalities: list, folder: str) -> None:
    """Master index grouped by type."""

    lines = [
        "# 👥 Quranic Personalities — Master Index\n\n",
        f"**Total: {len(all_personalities)}**\n\n",
    ]

    for ptype, (type_emoji, type_en, type_ur) in TYPE_META.items():
        group = [p for p in all_personalities if p["type"] == ptype]
        if not group:
            continue

        lines.append(f"\n## {type_emoji} {type_en} — {type_ur}\n\n")
        lines.append("| # | Name | Path | Era |\n")
        lines.append("|---|------|------|-----|\n")

        for i, p in enumerate(group, 1):
            path_emoji = PATH_META.get(p["path"], ("❓",))[0]
            path_label = PATH_META.get(p["path"], ("", ""))[1]
            era        = _truncate(p.get("era", "—"), 35)
            link       = _table_link(p)
            lines.append(f"| {i} | {link} | {path_emoji} {path_label} | {era} |\n")

    content = "".join(lines)
    write_note(folder, "All Personalities.md", content)
    print(f"  [INDEX]   Personalities/_Index/All Personalities.md")


def _write_path_index(all_personalities: list, folder: str, path: str) -> None:
    """
    Writes a single-path index (straight / deviated / mixed).
    path_reason is shown as a separate paragraph under each row,
    not crammed into a table cell, to avoid misalignment.
    """

    path_emoji, path_en, path_ur = PATH_META.get(path, ("❓", path, ""))
    group = [p for p in all_personalities if p["path"] == path]

    if not group:
        return

    # ── Header
    lines = [
        f"# {path_emoji} {path_en} — {path_ur}\n\n",
        f"**Total: {len(group)}**\n\n",
    ]

    if path == "deviated":
        lines.append(
            "> Understanding why they deviated is as important as understanding "
            "why the righteous succeeded. The Quran presents them as warnings, "
            "not as targets for hatred.\n\n"
        )
    elif path == "mixed":
        lines.append(
            "> These figures neither fit cleanly into straight nor deviated. "
            "Their stories show the complexity of moral life and the power of repentance.\n\n"
        )

    # ── Summary table — no path_reason column (too long, breaks alignment)
    lines.append("| # | Name | Type | Era |\n")
    lines.append("|---|------|------|-----|\n")

    for i, p in enumerate(group, 1):
        type_emoji = TYPE_META.get(p["type"], ("👤",))[0]
        type_label = TYPE_META.get(p["type"], ("", ""))[1]
        era        = _truncate(p.get("era", "—"), 35)
        link       = _table_link(p)
        lines.append(f"| {i} | {link} | {type_emoji} {type_label} | {era} |\n")

    # ── Detailed cards below the table — each person gets a mini section
    lines.append("\n---\n\n## Details\n\n")

    for p in group:
        type_emoji = TYPE_META.get(p["type"], ("👤",))[0]
        link       = f"[[{p['name_english']} — {p['name_arabic']}]]"
        lines.append(f"### {type_emoji} {link} — {p['name_urdu']}\n\n")
        lines.append(f"**Era:** {p.get('era', '—')}\n\n")
        lines.append(f"**Reason:** {p.get('path_reason', '—')}\n\n")

        tags = p.get("tags", [])
        if tags:
            tag_str = " ".join(f"`{t}`" for t in tags)
            lines.append(f"**Tags:** {tag_str}\n\n")

        lines.append("---\n\n")

    # ── File name map
    filename_map = {
        "straight": "Straight Path.md",
        "deviated": "Deviated Path.md",
        "mixed":    "Mixed Path.md",
    }

    filename = filename_map[path]
    content  = "".join(lines)
    write_note(folder, filename, content)
    print(f"  [INDEX]   Personalities/_Index/{filename}")
# ══════════════════════════════════════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════════════════════════════════════

def main():
    print("=" * 60)
    print("  Quran → Obsidian  |  note generator")
    print("=" * 60)

    create_index()
    created = 0
    updated = 0

    for surah_num_str, surah_ayahs in quran.items():
        surah_num    = int(surah_num_str)
        idx          = surah_num - 1
        en_name      = enChapters[idx]["translation"]
        ar_name      = urChapters[idx]["name"]
        ur_name      = urChapters[idx]["translation"]
        chapter_type = urChapters[idx]["type"]
        total_ayahs  = urChapters[idx]["total_verses"]
        folder       = f"{VAULT_PATH}/{surah_num_str} - {en_name} {ar_name}"
        eng_surah_names.append(en_name)
        arb_surah_names.append(ar_name)
        for ayah in surah_ayahs:
            ayah_num     = ayah["verse"]
            ayah_idx     = ayah_num - 1
            filename     = f"{surah_num_str}_{ayah_num}: {en_name} {ar_name}.md"
            filepath     = os.path.join(folder, filename)
            # ── Navigation links
            prev_link = (
                f"[[{surah_num_str}_{ayah_num - 1}: {en_name} {ar_name}]]"
                if ayah_num > 1 else "_(Start of Surah)_"
            )
            next_link = (
                f"[[{surah_num_str}_{ayah_num + 1}: {en_name} {ar_name}]]"
                if ayah_num < total_ayahs else "_(End of Surah)_"
            )

            # ── Content assembly
            ayah_text    = build_ayah_text(surah_num, ayah_num, ayah["text"])
            urdu_text    = urdu[surah_num_str][ayah_idx]["text"]
            english_text = english[surah_num_str][ayah_idx]["text"]
            tafsir_text  = load_tafsir_ur(surah_num_str, ayah_num)
            tags         = connections.get_ayah_themes(surah_num, ayah_num)

            # ── Build & write
            generated = build_generated_block(
                surah_num, ayah_num, total_ayahs,
                en_name, ar_name, ur_name, chapter_type, tags,
                ayah_text, urdu_text, english_text, tafsir_text,
                prev_link, next_link,
            )
            personal  = read_personal_section(filepath)
            is_new    = write_note(folder, filename, generated + personal)

            if is_new:
                created += 1
                print(f"  [NEW]     {filename}")
            else:
                updated += 1
                #print(f"  [UPDATED] {filename}")

    print()
    print("=" * 60)
    print(f"  ✅  {created} created,  {updated} updated")
    print("       Personal notes and reflections preserved.")
    print("=" * 60)
    asma_ul_husna_reader()
    personalities_reader(personalities)

if __name__ == "__main__":
    main()
    