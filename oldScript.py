import json, os
import QuranConnections as connections

with open('data/quran.json') as f:
    quran = json.load(f)

with open('data/en.json') as f:
    english = json.load(f)

with open('data/ur.json') as f:
    urdu = json.load(f)

with open('data/chapters/ur.json') as f:
    urChapters = json.load(f)

with open('data/chapters/en.json') as f:
    enChapters = json.load(f)

basePath = "../Mushaf"

# ─── Audio Configuration ───────────────────────────────────────────────────
#
# Your audio folder structure:
#   source/audio/017/000.mp3   ← Surah 17, Ayah 1  (000 = ayah index, 0-based)
#   source/audio/017/001.mp3   ← Surah 17, Ayah 2
#   source/audio/002/085.mp3   ← Surah 2,  Ayah 86
#
# AUDIO_BASE_PATH: path from THIS script to the audio folder.
# Adjust this if your folder layout differs.
#   e.g. if script is in  project/src/  and audio is in  project/source/audio/
#   then AUDIO_BASE_PATH = "../source/audio"
#
AUDIO_BASE_PATH = "./data/audio"

# AUDIO_VAULT_PATH: how Obsidian sees the audio files inside the vault.
# Obsidian resolves ![[filename]] by searching the whole vault,
# so the simplest approach is to keep audio INSIDE the vault under a subfolder.
#
# Option A (recommended): copy/symlink your audio folder INTO the vault:
#   ../Mushaf/audio/017/000.mp3
#   Then AUDIO_VAULT_PATH = "audio"
#
# Option B: keep audio outside vault and use a relative file:// link.
#   Less portable but avoids duplicating files.
#   Then set USE_EXTERNAL_LINK = True below.
#
# AUDIO_VAULT_PATH = "audio"        # subfolder name inside vault (Option A)

USE_EXTERNAL_LINK = True         # set True to use Option B (external path)
AUDIO_EXT = ".mp3"

# ──────────────────────────────────────────────────────────────────────────────


def audio_filename(surah_num: int, ayah_num: int) -> str:
    """
    Returns the audio filename for a given surah + ayah.
    Surah folder: zero-padded to 3 digits  → 017
    Ayah file:    zero-padded to 3 digits, 0-based index → 000 for ayah 1
    """
    surah_folder = str(surah_num).zfill(3)
    ayah_file    = str(ayah_num ).zfill(3)   # 0-based: ayah 1 → 000
    return f"{surah_folder}/{ayah_file}{AUDIO_EXT}"


def audio_embed(surah_num: int, ayah_num: int) -> str:
    """
    Returns the Obsidian markdown to embed or link the audio file.

    Obsidian natively plays audio embedded with  ![[path/to/file.mp3]]
    when the file lives inside the vault.  For external files it falls back
    to an HTML <audio> tag which also works in Reading View.
    """
    fname = audio_filename(surah_num, ayah_num)

    if USE_EXTERNAL_LINK:
        # Absolute path — works locally, not portable across machines
        abs_audio = os.path.abspath(
            os.path.join(AUDIO_BASE_PATH, fname)
        ).replace("\\", "/")
        return (
            f'<audio controls src="file://{abs_audio}">'
            f'</audio>'
        )
    else:
        # Obsidian wikilink embed — file must be inside the vault
        vault_rel = f"{AUDIO_VAULT_PATH}/{fname}"
        return f"![[{vault_rel}]]"

def getAyahTafseerUr(surahNum:str, ayahNum:str )-> str:
    with open(f'data/ur-tazkirul-quran/{surahNum}/{ayahNum}.json') as f:
        urTafseer = json.load(f)
    return urTafseer["text"]

def createNote(vaultPath:str, filename:str, content:str):
    if not os.path.exists(vaultPath):
            os.makedirs(vaultPath)

    with open(os.path.join(vaultPath, filename), 'w', encoding='utf-8') as f:
            f.write(content)

def createIndex():
    counter = 0
    category = ""
    content = "# The General Topics of Quran."

    for key, (emoji, theme , english, urdu, description) in connections.THEMES.items():
        if(theme != category):
            category = theme
            content += f"""

### The {theme}.

| # | Topic | Description |
| --- | --- | --- |
"""
        counter += 1
        content += f"| {counter} | {emoji} [{english}   {urdu}] | {description} |\n"
    content += f"the end\n"
    createNote(f"{basePath}/0 - index", "index.md", content)
createIndex()
indi = connections.build_index()
# print(indi)

# ─── Main generation loop ──────────────────────────────────────────────────────

for sorahNum, surah in quran.items():
    bismillah      = "بِسۡمِ ٱللَّهِ ٱلرَّحۡمَٰنِ ٱلرَّحِيمِ"
    sorahNumMinus  = int(sorahNum) - 1
    urChapterName  = urChapters[sorahNumMinus]["translation"]
    enChapterName  = enChapters[sorahNumMinus]["translation"]
    chapterName    = urChapters[sorahNumMinus]["name"]
    chapterType    = urChapters[sorahNumMinus]["type"]
    totalAyah      = urChapters[sorahNumMinus]["total_verses"]

    for ayah in surah:
        ayahNum    = ayah["verse"]
        ayahText   = ayah['text']
        urTafseer  = getAyahTafseerUr(sorahNum, ayahNum)
        vaultPath  = f"{basePath}/{sorahNum} - {enChapterName} {chapterName}"
        filename   = f"{sorahNum}_{ayahNum}: {enChapterName} {chapterName}.md"
        if int(sorahNum) > 1 and ayahNum == 1 and int(sorahNum) != 9:
            ayahText = bismillah+"\n\n"+ayahText
        prev = (
            f"[[{sorahNum}_{ayahNum-1}: {enChapterName} {chapterName}]]"
            if ayahNum > 1
            else "_(Start of Surah)_"
        )
        next_ = (
            f"[[{sorahNum}_{ayahNum+1}: {enChapterName} {chapterName}]]"
            if ayahNum < totalAyah
            else "_(End of Surah)_"
        )

        ayahNumMinus = int(ayahNum) - 1
        audio        = audio_embed(int(sorahNum), ayahNum)
        tags = connections.get_ayah_themes(int(sorahNum), ayahNum)
        print(tags)

        content = f"""---
surah: {sorahNum} / 114
surah_name: {enChapterName} / {chapterName} / {urChapterName}
ayah: {ayahNum} / {totalAyah}
type: {chapterType}
tags: {tags}
---

## 🔊 Recitation

{audio}

---

## Arabic

{ayahText}

---

## 🇵🇰 Urdu

{urdu[sorahNum][ayahNumMinus]['text']}

---

## 🇬🇧 English

{english[sorahNum][ayahNumMinus]['text']}

---


## 🇵🇰 Tafsir Bayan ul Quran

{urTafseer}

 ---

## Connections
- **Previous:** {prev}
- **Next:** {next_}
- **Thematic:** 

## Tafsir Notes

## Personal Reflection
"""

        createNote(vaultPath, filename, content)