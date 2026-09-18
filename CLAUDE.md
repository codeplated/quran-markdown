# Tadabbur — Note Generator
> Bismillah. This repo generates the Quran knowledge base vault.

---

## What This Repo Does

Reads the dataset in `/data` and writes 6,400+ Obsidian markdown notes into
the vault directory (`../Tadabbur` by default). The output is consumed by the
Tadabbur Quartz site repo.

No third-party dependencies. Python 3.12 or newer. Clone and run.

---

## Repo Structure

```
tadabbur-generator/
├── main.py                 ← entry point; orchestration only
├── config.py               ← every setting, overridable via .env
├── .env.example            ← copy to .env to change settings locally
├── tadabbur/               ← the generator internals
│   ├── data.py             ← loads the source JSON once; surah names, wikilinks
│   ├── audio.py            ← audio embeds + global ayah numbering
│   ├── notes.py            ← writing notes & preserving personal sections
│   ├── ayah_notes.py       ← the 6,236 ayah notes
│   ├── asma_notes.py       ← the 99 Names of Allah
│   ├── personalities.py    ← the 79 figures + their indexes
│   ├── explore.py          ← front page, Explore hub + Quran.base view
│   └── assets.py           ← thumbnails & vault_files copying
├── quranConnections.py     ← tag vocabulary (THEMES), retired names, related topics
├── ayah_tags/              ← ayah→theme map, one file per surah (s001.py … s114.py)
├── tag_audit.py            ← validates every tag + tracks tagging progress
├── TAGGING_PROGRESS.md     ← tagging rules, changelog & per-surah status
├── tests/                  ← python -m unittest discover -s tests -t .
├── docs/LICENSES.md        ← third-party content provenance & open questions
├── data/                   ← READ BELOW BEFORE TOUCHING
│   ├── quran.json          ← Arabic text
│   ├── en.json             ← English translation (Sahih International)
│   ├── ur.json             ← Urdu translation (Jalandhry)
│   ├── asma_ul_husna.json  ← 99 names of Allah
│   ├── quran_personalities.json  ← 79 personalities
│   ├── chapters/{en,ur}.json     ← surah names
│   ├── ur-tazkirul-quran/  ← Urdu tafsir, one JSON per ayah
│   ├── audio/              ← gitignored, local only, licensed
│   └── AlafasyAudio/       ← gitignored, local only, licensed
└── thumbnailGenerator/
    └── thumbnails/         ← surah_001.png … surah_114.png
```

---

## PROTECTED — Do Not Touch Without Strong Reason

### `/data` folder — SOURCE DATA
The files in `/data` are the raw Quran dataset. **Do not edit, restructure,
rename, or delete any file here unless explicitly asked.**

- `quran.json`, `en.json`, `ur.json` — never edit, these are the authoritative source
- `ur-tazkirul-quran/` — 6,350 JSON files, do not restructure
- `data/audio/`, `data/AlafasyAudio/` — gitignored, licensed, never commit these
- If a data file seems wrong, report it — do not fix it silently

### Sentinel blocks in vault notes
Every generated note has this shape:
```
---  frontmatter  ---
<!-- GENERATED:START -->
...script-owned content, rebuilt every run...
<!-- GENERATED:END -->
...the reader's own notes, never touched...
```
**Never edit content between these markers** — it is overwritten on the next
run. Everything after `<!-- GENERATED:END -->` is user-written; never delete,
move, or overwrite it.

`tadabbur/notes.py:write_note` is the **only** way a note reaches disk, and it
always carries the personal section across. Do not bypass it — the Names of
Allah notes once used a separate path that skipped this, and every run silently
erased what had been written under them.

---

## Configuration

All settings live in `config.py` with working defaults. Override them by
copying `.env.example` to `.env` (gitignored) or by exporting environment
variables. Paths resolve against the repo root, never the shell's directory.

| Setting | Default | Notes |
|---|---|---|
| `VAULT_PATH` | `../Tadabbur` | where notes are written |
| `AUDIO_MODE` | `api` | `api` \| `local` \| `r2` |
| `AUDIO_API_RECITER` | `ar.alafasy` | cdn.islamic.app reciter slug |
| `AUDIO_R2_BASE_URL` | *(empty)* | required when `AUDIO_MODE=r2` |
| `AUDIO_LOCAL_PATH` | `data/AlafasyAudio` | required when `AUDIO_MODE=local` |
| `AUDIO_LOCAL_LAYOUT` | `flat` | `flat` = `002255.mp3`, `nested` = `002/255.mp3` |

`config.validate()` runs before anything is written and fails loudly on an
unknown mode, an `r2` URL that was never set, or a missing local audio folder.

**For the website:** `AUDIO_MODE=api` · **For offline Obsidian:** `AUDIO_MODE=local`

---

## How to Run

```bash
python main.py                      # build everything
python main.py --only ayaat         # one part: ayaat|surahs|asma|personalities|index|assets
python main.py --vault ../Test      # write elsewhere without touching .env
python main.py --quiet              # summary only

python -m unittest discover -s tests -t .    # 18 tests, no deps
python tag_audit.py                          # validate every tag
```

---

## Folder Index Notes

A folder with no `index.md` gets whatever the site invents for it: a file list
sorted as text (2_1, 2_10, 2_100 …) that says nothing about the folder. Every
folder a reader lands on therefore writes its own:

| Folder | Written by | Holds |
|---|---|---|
| vault root | `explore.write_index` | the thematic index of every theme |
| `0 - Explore/` | `explore.write_explore_index` | links to the Quran grid, Names, Personalities, themes |
| `0 - Explore/Asma Ul Husna/` | `asma_notes._write_master_index` | the 99 Names by category |
| `0 - Explore/Personalities/` | `personalities._write_master_index` | the 79 figures by type |
| each surah folder | `surah_index.generate` | the surah's identity, themes, and every ayah in order |

Links between these notes must use the **full vault path** —
`[[2 - The Cow البقرة/index|…]]`. 114 notes are named `index`, so a bare
`[[index]]` is ambiguous and the site resolves it to the front page.

The surah index takes a personal section (`notes.SURAH_PERSONAL`); the other
indexes are pure navigation, rebuilt wholesale with `write_plain`.

---

## No Emoji in Notes

Generated notes carry no emoji: not in headings, not in the personality type
and path labels, not in the front page or the folder indexes. A colour emoji
font paints its own colours over the page, which fights the site's palette, and
every one of those labels already says what it means in English and Urdu.
`tests/test_generator.py` fails if an emoji reaches a note, a scaffolding
default, or an index.

The headings a reader owns are the exception, and only because they are theirs.
`notes.is_untouched_scaffolding` replaces a personal section that is still bare
generator headings — including the old `## Tafsir Notes` shape — with the
current scaffolding. A section with any writing in it is preserved exactly,
emoji and all.

---

## Frontmatter Values

`notes.frontmatter` writes values exactly as given, so anything free-text goes
through `notes.quote()` first. A value that opens with a YAML indicator changes
what the line means: surah 80's transliteration is `'Abasa`, and unquoted that
apostrophe starts a quoted scalar that never closes — which fails the entire
site build, not just that one note.

---

## Knowledge Graph Files

These are the files most commonly edited during study work.

### `quranConnections.py`
- `THEMES` — the one tag vocabulary: `(category, title, urdu, description)`.
  Ayaat, personalities and Asma notes may only use keys from here.
- `RETIRED_TAGS` — old names and the theme that replaced them. Never reuse one.
- `RELATED_TOPICS` — cross-theme relationships
- `AYAH_TAGS` — built from `ayah_tags/` (don't edit it here)

### `ayah_tags/sNNN.py`
One file per surah: `STATUS` (`todo` / `seed` / `deep`) and
`TAGS = {ayah_number: [theme keys]}`.

```python
# In ayah_tags/s018.py:
TAGS = {
    28: ["dhikr", "taqwa"],   # add or edit the ayah's list
}
```

Rules, changelog and status are in `TAGGING_PROGRESS.md`. After any tag change
run `python tag_audit.py` (`--write` refreshes the progress table,
`--surah N` prints a surah with its tags).

### `data/quran_personalities.json`
Fields: `id`, `name_arabic`, `name_english`, `name_urdu`, `also_known_as`,
`type`, `path`, `path_reason`, `era`, `mentioned_in`, `story_summary`,
`urdu_summary`, `lessons`, `connections`, `tags`

**Tags:** `THEMES` keys only, including the figure's `story_*` tag.
Path and type are fields, not tags.
**Connections** must match existing `id` values or the link breaks.

### `data/asma_ul_husna.json`
99 entries. Fields: `number`, `arabic`, `transliteration`, `english`, `urdu`,
`root`, `root_meaning`, `category`, `explanation`, `urdu_explanation`,
`daily_life`, `quran_occurrences`, `key_ayaat`, `tags`
(`asma_ul_husna` + `THEMES` keys)

---

## Note Filename Formats

```
{surah}_{ayah}: {english_name} {arabic_name}.md      → 2_255: The Cow البقرة.md
[[2_255: The Cow البقرة]]                             → the wikilink form

{number} - {transliteration} {arabic}.md             → 10 - Al-Jabbar ٱلْجَبَّار.md
{name_english} — {name_arabic}.md                    → Abu Bakr As-Siddiq — أَبُو بَكْر.md
```

Built by `data.Surah.note_name()`, `asma_notes.note_name()` and
`personalities.note_name()`. A note's filename is its wikilink target and its
page title on the site, so the published site's links depend on all three.

Renaming a note type means moving the existing files, not writing new ones
beside them — `notes.rename_note` does that, so the reader's personal section
travels with the note. The Names of Allah were renamed this way once already,
from `10 - ٱلْجَبَّار.md`; that migration stays in `asma_notes.generate()`
until every vault has been rebuilt at least once.

---

## Audio — Global Ayah Numbers

`cdn.islamic.app` uses a single number 1–6236 across all surahs.
Use `global_ayah(surah, ayah)` from `tadabbur/audio.py`.

```python
global_ayah(1, 1)    →  1      # Al-Fatihah 1:1
global_ayah(2, 255)  →  262    # Ayat al-Kursi
global_ayah(114, 6)  →  6236   # last ayah
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
| Change any setting | `.env` (see `.env.example`) |
| Change what a note looks like | the matching `tadabbur/*_notes.py` builder |
| Rename a note type | build the name in one place, then call `notes.rename_note` before writing |
| Add a new kind of note | new module in `tadabbur/`, add it to `ALL_PARTS` in `main.py` |
| Regenerate everything | `python main.py` |

---

## What NOT to Do

- Do not edit any file inside the vault (`../Tadabbur/`) directly
- Do not restructure `/data` or rename any data file
- Do not write notes except through `tadabbur/notes.py:write_note`
- Do not delete or modify the `<!-- GENERATED:START/END -->` sentinels
- Do not commit `data/audio/` or `data/AlafasyAudio/` — licensed, local only
- Do not change `global_ayah()` logic — verified against all 6,236 ayaat
- Do not change the ayah filename format — Quartz links depend on it
- Do not put emoji in a generated note, heading or index
