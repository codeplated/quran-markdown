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
│   ├── asma_notes.py       ← the 99 Names of Allah + the Asma Ul Husna page (every Name by category)
│   ├── personalities.py    ← the 79 figures + the Personalities page (every figure by type)
│   ├── themes.py           ← one note per theme + the Themes page (every theme by category)
│   ├── explore.py          ← home page (four cards, three entries in each) and the Quran's page
│   ├── layout.py           ← moves an older vault into the section folders
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
│   ├── ur.json             ← Urdu translation (Maududi, Tafheem ul Quran)
│   ├── asma_ul_husna.json  ← 99 names of Allah
│   ├── quran_personalities.json  ← 79 personalities
│   ├── chapters/{en,ur}.json     ← surah names
│   ├── ur-bayan-ul-quran/  ← Urdu tafsir (Dr. Israr Ahmad), one JSON per ayah
│   ├── ur-tazkirul-quran/  ← Urdu tafsir (Maulana Wahiduddin Khan), one JSON per ayah
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
- `ur-bayan-ul-quran/`, `ur-tazkirul-quran/` — 6,236 JSON files each, do not restructure (see docs/LICENSES.md §4)
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

python -m unittest discover -s tests -t .    # 64 tests, no deps
python tag_audit.py                          # validate every tag
```

---

## Vault Layout and Section Pages

The vault has four sections: **The Quran, Personalities, Asma Ul Husna,
Themes**. The home page offers them as four cards, in that order, and the
site's left panel shows the same four as its parents, so the top-level folder
names here are the site's navigation. The site's menu takes its sections from
these folders and their order from the home page's links to them; it names no
folder itself.

A folder with no `index.md` gets whatever the site invents for it: a file list
sorted as text (2_1, 2_10, 2_100 …) that says nothing about the folder. Every
folder a reader lands on therefore writes its own:

| Folder | Written by | Holds |
|---|---|---|
| vault root | `explore.write_index` | the home page: one line on what the site is, the four cards, then what Tadabbur means. A card says what its section holds and how its page can be arranged, then lists three entries from it with their counts. The entries are named in `explore.py` (`THEME_EXAMPLES` …); the counts are computed. The arrangements a card names are the ones the site's listing script offers, so the two change together |
| `The Quran/` | `explore.write_quran_index` | one card per surah, as a `base` block in the page |
| `The Quran/2 - The Cow/` | `surah_index.generate` | the surah's identity, themes, and every ayah in order |
| `Personalities/` | `personalities._write_master_index` | the Personalities page: every figure under its type, as headings and lists |
| `Asma Ul Husna/` | `asma_notes._write_master_index` | the Asma Ul Husna page: every Name under its category, as headings and lists |
| `tags/` | `themes.write_index` | the Themes page: every theme under its category, as headings and lists |

**Themes live in `tags/`.** The site serves a theme's page at `/tags/<key>`,
and a note at `tags/<key>.md` becomes the top of that page, so `themes.generate`
writes one per theme, named by its key. The folder's index note is titled
"Themes", which is the name readers see in the left panel and breadcrumbs.

**The three listing pages are plain headings and lists**, written one way:
Themes, Personalities and Asma Ul Husna. Each has a heading per group and under
it one line per entry. A line is the entry's name as a link, then its name in
Urdu or Arabic, a count and some details, each in an element of its own:

```
- [[tags/tawheed|Tawheed]] <span lang="ur">توحید</span> <span class="count">381 <span class="unit">ayaat</span></span> <small>Oneness of Allah…</small>
- [[Adam — آدَم|Adam]] <span lang="ar">آدَم</span> <span class="count">21 <span class="unit">ayaat</span></span> <small><span class="path" data-rank="1">Straight Path</span> · Beginning of humanity · <span lang="ur">آدم علیہ السلام</span></small>
- <span class="num">2</span> [[2 - Ar-Rahman ٱلرَّحْمَـٰن|Ar-Rahman]] <span lang="ar">ٱلرَّحْمَـٰن</span> <span class="count">57 <span class="unit">times</span></span> <small>The Most Gracious · <span lang="ur">بے حد رحم کرنے والا</span> · <span class="root">root <span lang="ar">ر-ح-م</span></span></small>
```

| Page | Groups, in order | Count | Details |
|---|---|---|---|
| Themes | categories, as `THEMES` declares them | ayaat that carry the theme | description |
| Personalities | types, as `TYPE_META` declares them (`TYPE_HEADINGS` names them) | ayaat the note lists; none when it lists none | path, era, Urdu name |
| Asma Ul Husna | categories, as `CATEGORY_ORDER` declares them, without their "Names of " | times in the Quran; none when not in this form | meaning in English and Urdu, root |

Each page carries `cssclasses: [index-page, X]` (`notes.index_classes`), X being
`themes-index`, `people-index` or `names-index`.

A page reads as it is in Obsidian and with scripts off. The site lays the lines
out in columns and adds a filter and other arrangements from what each line
holds, so the elements and their order are a contract with the site (its
`CLAUDE.md` lists it). These things about a line are deliberate:

- It leads with the Latin name. A line that opens with Urdu is laid out right
  to left.
- Urdu and Arabic are marked (`lang="ur"`, `lang="ar"`) here. The site
  otherwise guesses the language from the letters, and a word like نفاق has
  none that only Urdu uses. A Name with two roots marks each, since the "and"
  between them is English.
- A person's path carries `data-rank`, its place among the paths. The site's
  "By Path" arrangement groups by the path's text and orders by that number.
- A Name's line begins with its number, which the site sorts "1–99" by.
- Parts of the details are separated by " · ", so a Name's several meanings are
  joined with commas there.
- A theme's count is ayaat only (`themes.ayah_counts`). A theme note's own
  `notes` field also counts the personality and Name notes that carry the theme.

Themes was a `base` table until 2026-10-11; the `theme` and `order` fields that
fed it are no longer written on theme notes. Personalities was a `base` table
with a tab per path, and Asma Ul Husna ten markdown tables, until 2026-10-12;
the `order` field that sorted the first is no longer written on figures.

The three path pages under `Personalities/Filtered/` are gone; the "By Path"
arrangement replaces them.

**A person's note and a Name's note say their fields under their heading.**
After the `# heading` comes a line or two (a person's name in Urdu; a Name's
meaning in English, then in Urdu), then a quote block:

```
> [[Personalities/index#Prophets and Messengers|Prophet / Messenger]] · Straight Path · Beginning of humanity · [[#Mentioned in Quran|21 ayaat]]
>
> **Also known as:** The First Human, Abu al-Bashar, Khalifah
>
> **Themes:** [[tags/story_adam|Prophet Adam]] · [[tags/prophethood|Prophethood]] · …
```

The type (or a Name's category) links to its heading on the listing page, so
those headings and these links have to agree; a test checks every one. Themes
are links by name (`notes.theme_links`), not tag keys. Both kinds of note carry
`cssclasses: [profile]`, which tells the site to leave out its own title,
properties box, reading time and tag chips: the note already says all four.
The lines under the heading used to be `###` and `####` headings, which gave
the page an outline that jumped from level 1 to 3.

Older vaults had the surah folders at the top level and Personalities and
Asma Ul Husna under `0 - Explore`. `layout.migrate` moves them into place at
the start of every run, before anything is written, whole folders at a time so
personal sections travel with their notes. It also removes the listings the old
layout needed (`0 - Explore/index.md`, `0 - Explore/Themes.md`, a top-level
`Themes.md`, the pages under `Personalities/Filtered/`) and a `Quran.base`
nobody edited.

Links between these notes must use the **full vault path**,
`[[The Quran/2 - The Cow/index|…]]`, from `data.Surah.index_path`. 114 notes
are named `index`, so a bare `[[index]]` is ambiguous and the site resolves it
to the front page.

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
The Quran/{surah} - {english_name}/                  → The Quran/2 - The Cow/ (surah folder)
{surah}_{ayah}.md                                    → 2_255.md
[[2_255]]                                            → the wikilink form

{number} - {transliteration} {arabic}.md             → 10 - Al-Jabbar ٱلْجَبَّار.md
{name_english} — {name_arabic}.md                    → Abu Bakr As-Siddiq — أَبُو بَكْر.md
```

Built by `data.Surah.note_name()`, `asma_notes.note_name()` and
`personalities.note_name()`. A note's filename is its wikilink target and its
URL on the site, so the published site's links depend on all three. Ayah notes
take their page title from the `title` frontmatter
(`data.Surah.display_name()`, `2_255: The Cow البقرة`) instead.

Anything that finds notes by path has to follow a rename too: canvases store
vault paths, which `assets.relink_canvas` moves from the old layouts.
The surah cards (`explore.QURAN_BASE`) link each card to a surah's `index`
note, picked by `file.name == "index"` plus the `surah_name` property; the
card heading is the index note's `title` (`2 - The Cow البقرة`).

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
