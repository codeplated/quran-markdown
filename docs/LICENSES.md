# Third-party content — provenance and what is still unresolved

The generator's own code is ours. Almost everything it *reads* is someone
else's work. This file records where each dataset came from and what is
known about its terms, so the question can be answered without re-deriving it.

**Status: two of the four datasets have no verifiable licence.** That is a
blocker for publishing, not for developing. It is tracked below.

This is a record of what the files say, not legal advice.

---

## 1. Recitation audio — unresolved, not distributed

| | |
|---|---|
| **Files** | `data/AlafasyAudio/` (6,238 mp3, ~1.7 GB), `data/audio/` (6,348 mp3, ~440 MB) |
| **Reciters** | Mishary Rashid Alafasy; Saad al-Ghamdi (`data/audio/.sources` says "Ghamadi ~ 40kbps") |
| **Stated source** | `http://www.versebyversequran.com/site/licence/` — recorded in `data/audio/.sources` and in `data/AlafasyAudio/000_license.html` |
| **In git?** | **No.** Untracked and git-ignored as of the "Stop tracking recitation audio" commit. Files remain on local disk. |

### What the licence file actually says

`data/AlafasyAudio/000_license.html` contains one sentence and a link:

> Please note that use of these MP3s is only allowed if you comply with the
> license details: http://www.versebyversequran.com/site/license

### Why this is unresolved

That link is dead. Checked 2026-09-18:

- `versebyversequran.com/site/license` → **HTTP 404**
- `versebyversequran.com/site/licence/` → **HTTP 404**
- the domain now serves **everyayah.com**, whose recitation listing
  (`everyayah.com/recitations_ayat.html`) publishes **no licence, copyright
  or redistribution terms at all**

So the terms these files tell you to comply with cannot currently be read.
The obligation does not disappear because the page is gone — it just means
compliance is unverifiable today.

### What is needed from you

1. **Contact everyayah.com** (contact form on the site) and ask for the terms
   that applied to the Alafasy and Ghamdi ayah-by-ayah mp3 sets, in writing.
   Save the reply in this folder.
2. **Or go to the reciter's own distributor.** Alafasy audio is published in
   several places with explicit terms; sourcing from one that states them is
   simpler than reconstructing a dead page.
3. **Decide what the site actually serves.** Right now `AUDIO_MODE=api`
   hotlinks `cdn.islamic.app`, so you are not redistributing anything — but
   you are depending on a third party with no stated terms or uptime promise,
   and hotlinking can be withdrawn without notice. If audio matters to the
   product, self-hosting under a licence you can point to is the stable answer.
4. **Until then, keep the mp3s out of git.** Already enforced by `.gitignore`.

---

## 2. Quran text — `data/quran.json`

The Arabic text of the Quran is not itself under copyright. A *particular
digital edition* can carry rights in its encoding, vocalisation and metadata.
This file records no source.

**Needed from you:** confirm which edition this is (Tanzil, King Fahd Complex,
QuranEnc, …) and add it to the table below. Tanzil, the most common source,
requires an attribution notice and prohibits modifying the text.

---

## 3. Translations — `data/en.json`, `data/ur.json`

| File | Translation | Recorded source |
|---|---|---|
| `en.json` | Sahih International | none in the repo |
| `ur.json` | Fateh Muhammad Jalandhry | none in the repo |

Both are modern works. Sahih International in particular is widely mirrored
but is **not** public domain, and its publisher's terms are usually
non-commercial with attribution.

**Needed from you:** identify where these were obtained and under what terms,
then add an attribution line to the generated notes or the site footer. This
is usually the cheapest item on the list to fix — attribution is normally all
that is asked.

---

## 4. Urdu tafsir — `data/ur-tazkirul-quran/`

6,350 files. Tazkirul Quran is the tafsir of Maulana Wahiduddin Khan,
a 20th-century work under copyright. Notes are generated with the heading
"Tafsir — Bayan ul Quran", which names a *different* work
(Dr. Israr Ahmed / Maulana Ashraf Ali Thanvi, depending on the edition).

**Needed from you:** two things — permission or a licence for the tafsir text,
and a decision on which work the heading should name, since it currently
contradicts the folder.

---

## 5. Thumbnails — `thumbnailGenerator/`

Generated locally with ComfyUI (`batch_generate.py` posts to a local instance).
Rights depend on the checkpoint used and its licence.

**Needed from you:** note which model produced them, so the question can be
answered later without guessing.

---

## Summary of open actions

| # | Item | Action | Blocks publishing? |
|---|---|---|---|
| 1 | Recitation audio | Get terms in writing, or re-source | Only if you self-host audio |
| 2 | Quran text | Identify the edition, add attribution | Low risk |
| 3 | Translations | Identify source, add attribution | **Yes** — attribution is expected |
| 4 | Tafsir | Get permission; fix the mismatched heading | **Yes** |
| 5 | Thumbnails | Record the model | Low risk |

When each is settled, replace the "needed from you" line with the answer and
a link to where it is recorded.
