# Tadabbur — Note Generator
> Bismillah. This repo generates the Quran knowledge base vault.

---

## What This Repo Does

Reads structured Quran data from `/data` and generates 6,500+ Obsidian
markdown notes into the vault directory (`../Mushaf` by default).
The output is consumed by the Tadabbur Quartz site repo.

---

## Repo Structure

```
tadabbur-generator/
├── main.py                        ← entry point — run this to generate notes
├── quranConnections.py            ← tag vocabulary (THEMES), retired names, related topics
├── ayah_tags/                     ← ayah→theme map, one file per surah (s001.py … s114.py)
├── tag_audit.py                   ← validates every tag + tracks tagging progress
├── TAGGING_PROGRESS.md            ← tagging rules, changelog & per-surah status
├── quran_personalities.py         ← 79 Quranic personalities (Python source)
├── personalities_functions.py     ← note builders for personalities
├── audio_config.py                ← audio embed (3 modes: local/api/r2)
├── thumbnail_copy_function.py     ← copies thumbnails to vault attachments
├── data/                          ← ⚠️  READ BELOW BEFORE TOUCHING
│   ├── quran.json                 ← Arabic text
│   ├── en.json                    ← English translation (Sahih International)
│   ├── ur.json                    ← Urdu translation (Jalandhry)
│   ├── asma_ul_husna.json         ← 99 names of Allah
│   ├── quran_personalities.json   ← 79 personalities (JSON, used by main.py)
│   ├── chapters/
│   │   ├── en.json                ← Surah names in English
│   │   └── ur.json                ← Surah names in Urdu/Arabic
│   ├── ur-tazkirul-quran/         ← Urdu tafsir, one JSON per ayah
│   └── audio/                     ← ⚠️  MP3 files, gitignored, local only
└── thumbnailGenerator/
    └── thumbnails/                ← surah_001.png … surah_114.png
```

---

## ⚠️  PROTECTED — Do Not Touch Without Strong Reason

### `/data` folder — SOURCE DATA
The files in `/data` are the raw Quran dataset. **Do not edit, restructure,
rename, or delete any file here unless explicitly asked.**

- `quran.json`, `en.json`, `ur.json` — never edit, these are the authoritative source
- `ur-tazkirul-quran/` — 6,236 individual JSON files, do not restructure
- `data/audio/` — gitignored local files, never commit these
- If a data file seems wrong, report it — do not fix it silently

### Sentinel blocks in vault notes
Every generated note contains:
```
<!-- GENERATED:START -->
...script-owned content...
<!-- GENERATED:END -->
```
**Never edit content between these markers.** Everything after
`<!-- GENERATED:END -->` is user-written personal content — never delete,
move, or overwrite it.

---

## Key Configuration (top of main.py)

```python
VAULT_PATH      = "../Mushaf"        # where vault notes are written
AUDIO_BASE_PATH = "./data/audio"     # local audio path (local mode only)
AUDIO_MODE      = "api"              # "local" | "api" | "r2"
R2_BASE_URL     = "https://assets.yourdomain.com"  # r2 mode only
API_RECITER     = "ar.alafasy"       # cdn.islamic.app reciter slug
```

**Before generating for the website:** set `AUDIO_MODE = "api"`
**Before generating for local Obsidian:** set `AUDIO_MODE = "local"`

---

## How to Run

```bash
# Generate all 6,500+ notes
python main.py

# Output summary shows:
#   [NEW]     — first time a note is created
#   [UPDATED] — regenerated, personal notes preserved
```

---

## Knowledge Graph Files

These are the files most commonly edited during study work:

### `quranConnections.py`
- `THEMES` — the one tag vocabulary (category, title, urdu, description).
  Ayaat, personalities and Asma notes may only use keys from here.
- `RETIRED_TAGS` — old/duplicate tag names and the theme that replaced them.
  Never reuse a retired name.
- `RELATED_TOPICS` — cross-theme relationships
- `AYAH_TAGS` — built from `ayah_tags/` (don't edit it here)

### `ayah_tags/sNNN.py`
One file per surah: `STATUS` (`todo` / `seed` / `deep`) and
`TAGS = {ayah_number: [theme keys]}`.

**To add a thematic connection:**
```python
# In ayah_tags/s018.py:
TAGS = {
    28: ["dhikr", "taqwa"],   # add or edit the ayah's list
}
```

The deep tagging pass runs surah by surah — rules, changelog and status are in
`TAGGING_PROGRESS.md`. After any tag change run `python tag_audit.py`
(`--write` refreshes the progress table, `--surah N` prints a surah with its tags).

### `data/quran_personalities.json`
Each entry has: `id`, `name_arabic`, `name_english`, `name_urdu`,
`also_known_as`, `type`, `path`, `path_reason`, `era`, `mentioned_in`,
`story_summary`, `urdu_summary`, `lessons`, `connections`, `tags`

**To add a personality:** append a new object to the JSON array.
**Tags:** use `THEMES` keys only, including the figure's `story_*` tag.
Path and type are fields, not tags.
**To fix a connection:** edit the `connections` array — values must match
existing `id` fields or the link will be broken.

### `data/asma_ul_husna.json`
99 entries. Fields: `number`, `arabic`, `transliteration`, `english`,
`urdu`, `root`, `root_meaning`, `category`, `explanation`,
`urdu_explanation`, `daily_life`, `quran_occurrences`, `key_ayaat`, `tags`
(`asma_ul_husna` + `THEMES` keys)

---

## Ayah Filename Format

```
{surah_number}_{ayah_number}: {english_name} {arabic_name}.md
# Example:
2_255: Al-Baqarah البقرة.md
```

Wikilinks follow the same format:
```
[[2_255: Al-Baqarah البقرة]]
```

---

## Audio — Global Ayah Numbers

`cdn.islamic.app` uses a single number 1–6236 across all surahs.
Use `get_global_ayah(surah, ayah)` from `audio_config.py` to convert.

```python
get_global_ayah(1, 1)    →  1      # Al-Fatihah 1:1
get_global_ayah(2, 255)  →  262    # Ayat al-Kursi
get_global_ayah(114, 6)  →  6236   # last ayah
```

CDN URL pattern:
```
https://cdn.islamic.app/quran/audio/ar.alafasy/{global_ayah}.mp3
```

---

## Common Tasks

| Task | What to change |
|------|---------------|
| Add thematic tag to an ayah | `ayah_tags/sNNN.py`, then `python tag_audit.py` |
| Add a new theme / category | `THEMES` + `RELATED_TOPICS` in `quranConnections.py` |
| Continue the deep tagging pass | follow `TAGGING_PROGRESS.md` |
| Add/fix a personality | `data/quran_personalities.json` |
| Add/fix an Asma note | `data/asma_ul_husna.json` |
| Change audio mode | `AUDIO_MODE` at top of `main.py` |
| Change vault output path | `VAULT_PATH` at top of `main.py` |
| Regenerate everything | `python main.py` |

---

## What NOT to Do

- ❌ Do not edit any file inside `../Mushaf/` (the vault) directly
- ❌ Do not restructure `/data` folder or rename any data file
- ❌ Do not delete or modify `<!-- GENERATED:START/END -->` sentinels
- ❌ Do not commit `data/audio/` — it is gitignored and local only
- ❌ Do not change `get_global_ayah()` logic — it is verified against all 6,236 ayaat
- ❌ Do not change the ayah filename format — Quartz links depend on it
