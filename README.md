# Tadabbur — Quran Note Generator

**Tadabbur** (تدبّر) means to reflect deeply, to ponder. This tool turns a
structured Quran dataset into a cross-linked [Obsidian](https://obsidian.md)
vault — every ayah of all 114 surahs with recitation audio, Arabic text, Urdu
and English translation, tafsir, and thematic links between them.

It generates **6,400+ notes**: 6,236 ayaat, 99 Names of Allah, 79 Quranic
personalities, and the indexes that tie them together.

> **Your own writing is safe.** Everything you write below the
> `<!-- GENERATED:END -->` marker in any note is preserved across every
> rebuild. Rerun as often as you like.

---

## Quick start

```bash
git clone https://github.com/codeplated/quran-markdown.git
cd quran-markdown
python main.py
```

That's it. **Python 3.12+, no dependencies to install.** The vault is written
to `../Tadabbur` — open that folder in Obsidian.

```bash
python main.py --only ayaat      # build one part while iterating
python main.py --vault ../Test   # try it somewhere harmless first
python main.py --help            # all options
```

---

## Configuration

Everything is in [`config.py`](config.py) with working defaults. To change
something, copy `.env.example` to `.env` and edit it — `.env` is git-ignored,
so your local paths never land in a commit.

```bash
cp .env.example .env
```

The setting most people change first is audio:

| `AUDIO_MODE` | What you get | Needs |
|---|---|---|
| `api` *(default)* | streams from a public CDN | nothing |
| `local` | `file://` links to mp3s on your machine | your own audio, see [docs/LICENSES.md](docs/LICENSES.md) |
| `r2` | your own bucket or CDN | `AUDIO_R2_BASE_URL` |

Bad settings are caught before any file is written, with a message saying
what to fix.

---

## How the code is laid out

`main.py` is the whole pipeline on one screen — start there. Each module under
`tadabbur/` owns one kind of note and can be read on its own:

| File | Responsibility |
|---|---|
| [`config.py`](config.py) | every setting, and validation |
| [`tadabbur/data.py`](tadabbur/data.py) | loads the source JSON once; surah names, wikilinks |
| [`tadabbur/audio.py`](tadabbur/audio.py) | audio embeds, global ayah numbering |
| [`tadabbur/notes.py`](tadabbur/notes.py) | writing notes, preserving personal sections |
| [`tadabbur/ayah_notes.py`](tadabbur/ayah_notes.py) | the 6,236 ayah notes |
| [`tadabbur/asma_notes.py`](tadabbur/asma_notes.py) | the 99 Names of Allah |
| [`tadabbur/personalities.py`](tadabbur/personalities.py) | the 79 figures and their indexes |
| [`tadabbur/explore.py`](tadabbur/explore.py) | the thematic index |
| [`tadabbur/assets.py`](tadabbur/assets.py) | thumbnails, hand-made vault files |

Separately, the **knowledge graph** — the part that is study work rather than
code:

| File | Responsibility |
|---|---|
| [`quranConnections.py`](quranConnections.py) | `THEMES`, the single tag vocabulary (138 themes) |
| [`ayah_tags/`](ayah_tags/) | which themes each ayah carries, one file per surah |
| [`tag_audit.py`](tag_audit.py) | validates every tag; tracks tagging progress |
| [`TAGGING_PROGRESS.md`](TAGGING_PROGRESS.md) | tagging rules, changelog, per-surah status |

---

## What a note looks like

```markdown
---
surah: 2 / 114
surah_name: The Cow / البقرة / گائے
ayah: 255 / 286
type: medinan
tags: ["tawheed", "asma_ul_husna"]
image: "/attachments/surah_002.png"
---
<!-- GENERATED:START -->
## Recitation
...Arabic, Urdu, English, tafsir, navigation...
<!-- GENERATED:END -->

## Tafsir Notes          ← everything from here down is yours
```

The generator rewrites only what sits between the two markers.

---

## Contributing

Two kinds of contribution, and they rarely collide:

**Study work** — adding thematic tags, personalities, or Names. You only need
to touch `ayah_tags/`, `quranConnections.py`, or the JSON in `data/`. Read
[`TAGGING_PROGRESS.md`](TAGGING_PROGRESS.md) first; it has the rules and the
current status of all 114 surahs. Run `python tag_audit.py` when you're done —
it must report 0 errors.

**Code** — everything under `tadabbur/`. Before opening a PR:

```bash
python -m unittest discover -s tests -t .   # must pass
python tag_audit.py                         # must report 0 errors
```

A few rules the code depends on:

- **Never write a note except through `notes.write_note`.** It is what keeps
  readers' personal sections alive.
- **Never change the ayah filename format.** The published site links to it.
- **Never change `global_ayah()`.** It is verified against all 6,236 ayaat.
- **Never commit audio.** See below.

[`CLAUDE.md`](CLAUDE.md) has the fuller version of these conventions.

---

## Content and licensing

The code is ours; nearly everything it reads is not. Recitation audio is
**not distributed with this repo** — it is licensed third-party material and
is git-ignored.

Some datasets here still have unresolved provenance.
**[`docs/LICENSES.md`](docs/LICENSES.md) records what is known, what is not,
and what has to be settled before publishing.** Please read it before
redistributing anything this tool produces.
