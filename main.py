import json
import os
import re

import QuranConnections as connections

VAULT_PATH       = "../Mushaf"          # root of your Obsidian vault
AUDIO_BASE_PATH  = "./data/audio"       # where audio files live on disk
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

# ══════════════════════════════════════════════════════════════════════════════
#  AUDIO HELPERS
# ══════════════════════════════════════════════════════════════════════════════

def audio_path(surah_num: int, ayah_num: int) -> str:
    """Returns the relative audio path: 017/001.mp3"""
    folder = str(surah_num).zfill(3)
    file   = str(ayah_num).zfill(3)
    return f"{folder}/{file}{AUDIO_EXT}"


def audio_embed(surah_num: int, ayah_num: int) -> str:
    """Returns the Obsidian markdown snippet to play the audio."""
    rel_path = audio_path(surah_num, ayah_num)

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

## 🔊 Recitation

{audio}

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
- **Thematic:** *(add [[wikilinks]] here)*

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
                print(f"  [UPDATED] {filename}")

    print()
    print("=" * 60)
    print(f"  ✅  {created} created,  {updated} updated")
    print("       Personal notes and reflections preserved.")
    print("=" * 60)


if __name__ == "__main__":
    main()
    