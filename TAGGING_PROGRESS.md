# Tag Rework — Progress Record

The goal: one shared, deduplicated tag vocabulary (`THEMES` in `quranConnections.py`)
used by every ayah, personality and Name of Allah, applied in depth across the whole
Quran. The work is too big for one sitting, so it runs in steps and this file is the
record.

**Resume in a new session with:** *"Continue the tag rework — read TAGGING_PROGRESS.md
and tag the next surahs."*

---

## Phases

| # | Phase | Status |
|---|-------|--------|
| 1 | Taxonomy — merge duplicates, deepen themes (76 → 138), record retired names, related topics for every theme | done 2026-09-17 |
| 2 | Personalities — all 79 retagged on the shared vocabulary | done 2026-09-17 |
| 3 | Asma ul Husna — all 99 names tagged, duplicate categories merged | done 2026-09-17 |
| 4 | Ayaat — surah-by-surah deep pass, all 114 surahs (status table at the bottom) | done 2026-09-18 |
| 5 | Final review — theme sizes, exact-count checks, consistency sweep | done 2026-09-18 |

---

## How to do one step (Phase 4)

1. Pick the next surah that is not marked deep in the table below.
2. `python tag_audit.py --surah N` — prints every ayah's English translation beside
   its current tags (add `--from A --to B` for long surahs).
3. Write every ayah into `ayah_tags/sNNN.py`, grouping passages with
   `# a–b · passage` comments. Keep seed tags that are right, replace ones that are
   wrong, and set `STATUS = "deep"`.
4. `python tag_audit.py --write` — must report 0 errors; it refreshes the table below.
5. Add a line to the session log.

---

## Tagging rules

1. **Every ayah gets at least one tag.** Aim for 2–4, up to 6 for dense ayaat
   (7 only for exceptional ones like 2:83 or 2:177). Put the most central theme first.
2. **Tag what the ayah is about**, not every word in it. An ayah that ends "Allah is
   Forgiving and Merciful" is not automatically `rahmah` or `asma_ul_husna`; use them
   only when mercy or the Names are the point of the ayah.
3. **Stories:** every ayah of a narrative passage gets its `story_*` tag, even when
   the prophet is not named in that ayah. Add `history_lessons` where the passage
   draws the lesson or describes a nation's destruction.
4. **Seerah events** (`battle_*`, `hijrah`, `incident_ifk`, …) go on the ayaat about
   that event. Add `conflict` only where the ayah deals with fighting itself.
5. **Meta tags are literal:** `o_believers` / `o_mankind` only on the actual address;
   `they_ask_you` only on "they ask you" ayaat; `oaths` only where Allah swears;
   `parables` only on explicit similitudes and examples; `muqattaat` on the opening
   letters; `sajdah_tilawah` on the 15 marked ayaat.
6. **`commands` / `prohibitions`** are explicit instructions or bans addressed to
   believers or mankind, not commands inside a story ("strike the sea with your staff").
7. **`glad_tidings` / `warnings`** mark an explicit promise of reward or threat of
   punishment.
8. **Close pairs — pick the right one** (or both, when the ayah really does both):
   - `rahmah` Allah's mercy · `hope_raja` the servant's hope and not despairing
   - `tawheed` affirming oneness · `shirk` refuting partners
   - `kufr` disbelief and denial · `shirk` polytheism · `nifaq` hidden disbelief
   - `resurrection` proofs that the dead will rise · `akhirah` the Day, reckoning, scales
   - `death_reminder` death and the grave · `akhirah` what comes after
   - `sidq` truthfulness · `amanah` trusts, promises, covenants
   - `adl` justice · `social_justice` rights of the poor · `oppression` dhulm
   - `zakat` giving · `wealth` attitude to money · `rizq` Allah as Provider
   - `dhikr` remembrance · `dua` asking · `quran_recitation` reciting and reflecting
   - `revelation` what the Quran is · `quran_recitation` what we do with it
   - `tazkiyah` the soul's inner struggle · `taqwa` God-consciousness
   - `dunya` the worldly life and its pull · `trial_test` hardship and ease as a test
   - `speech_ethics` the tongue · `adab` manners and conduct
   - `nature_signs` · `human_creation` · `animals` · `miracles` (prophets' signs only)
   - `story_bani_israil` their history · `ahl_al_kitab` Jews and Christians in the Prophet's ﷺ time
9. **Never invent a tag.** If a real theme is missing, add it to `THEMES` (unique
   title) and to `RELATED_TOPICS`, then note it in the changelog.
10. **Never reuse a retired name** — `RETIRED_TAGS` lists them all.

---

## Changelog — merged, split & retired tags

### Ayah themes (76 → 138)
- **Merged:** `tawbah_return` → `tawbah` ("Return to Allah" meant the same as Tawbah).
- **Renamed:** `gratitude_life` → `purpose_of_life` (the key said gratitude but the theme
  was Purpose of Life; gratitude is `shukr`). Used on 51:56 and 95:4.
- **Split:** `sidq` "Sidq & Amanah" → `sidq` + `amanah` (23:8 already used an `amanah`
  tag that was never defined).
- **Split:** `dhikr` "Dhikr & Dua" → `dhikr` + `dua`.
- **Split:** `angels` "Angels, Jinn & the Unseen" → `angels` + `jinn` + `shaytan`.
- **Sharper scope, same key:** `akhirah`, `anxiety_fear` (now also sakinah),
  `revelation`, `quran_recitation`, `kibr` (arrogance *and* humility), `ikhlas`,
  `conflict` (jihad, war & peace), `environment`, `social_justice`, `history_lessons`.
- **Titles:** every theme title is now unique. Emojis were made unique first (before, 14
  emojis were shared by 30 themes — one mosque glyph for both Tawheed and Salah, one scales glyph for Akhirah, Adl
  and Social Justice, …), then dropped entirely on 2026-09-18: `THEMES` entries are now
  `(category, title, urdu_title, description)` and the index carries a **Notes** column
  counting how many notes use each tag instead.
- **New themes:**
  - Belief: `rahmah`, `iman`, `shirk`, `kufr`, `nifaq`, `hidayah`
  - Hereafter (new category): `resurrection` (+ `akhirah`, `jannah`, `jahannam`, `death_reminder` moved in)
  - Prophets: all 25 prophets named in the Quran now have a `story_*` tag (was 11)
  - Narratives (new): `story_maryam`, `story_luqman`, `story_dhulqarnayn`, `story_ashab_al_kahf`, `story_bani_israil`
  - Seerah (new): `sahabah`, `prophets_household`, `hijrah`, `isra_miraj`, `battle_badr`, `battle_uhud`, `battle_ahzab`, `treaty_hudaybiyah`, `battle_hunayn`, `expedition_tabuk`, `incident_ifk`
  - Worship: `taharah`, `kaaba`
  - Character: `haya`, `speech_ethics`, `adab`
  - Spirit: `tazkiyah`, `dunya`, `love_of_allah`
  - Life: `riba`
  - Relations: `women`
  - Society: `wala_bara`, `ahl_al_kitab`, `dawah`, `criminal_law`
  - Signs: `human_creation`, `animals`, `miracles`
  - Meta: `muqattaat`, `sajdah_tilawah`, `o_believers`, `o_mankind`, `they_ask_you`
- **RELATED_TOPICS:** `akhirah` no longer lists itself; every theme now has an entry.
- **Storage:** `AYAH_TAGS` moved out of `quranConnections.py` into `ayah_tags/s001.py …
  s114.py`, so each step touches one surah file. The 344 seed ayaat (62 surahs) were
  carried over unchanged, apart from the rename above.

### Personalities (197 free-form tags → shared vocabulary)
- All 79 retagged with theme keys, 2–7 each, including a `story_*` tag that ties each
  figure to their narrative (so the `story_musa` tag page lists Musa, Harun, Firawn,
  Haman, Qarun, Samiri, Khidr and Asiya alongside the ayaat).
- Same-meaning tags merged, e.g. `patience`+`sabr` → `sabr`; `arrogance`+`kibr` → `kibr`;
  `envy`/`jealousy`/`hasad` → `hasad`; `paradise`+`jannah` → `jannah`;
  `tyrant`/`oppressor`/`persecutor`/`persecutors`/`persecution` → `oppression`;
  `woman`/`women`/`greatest-women`/`mother` → `women`; `destroyed`/`destruction` →
  `history_lessons`; `revelation`+`wahi` → `revelation`; `young`/`youth` → the figure's
  story tag. Every one-to-one replacement is listed in `RETIRED_TAGS`.
- `prophet` → `prophethood`, `angel` → `angels`, `companion` → `sahabah`.
- Removed `straight`, `deviated`, `mixed`, `group` — they repeated the `path` and `type`
  fields (already in frontmatter and in the Filtered indexes), and were inconsistent
  (52 of the 54 straight-path figures had the tag).
- Tags that depended on context were replaced one by one, e.g. `power` → `leadership`,
  `egypt` → `story_musa`, `cave` → `hijrah` (Abu Bakr) or `story_ashab_al_kahf`,
  `trust` → `tawakkul` (Abu Bakr), `sacrifice` → `trial_test` (Ibrahim, Ismail) or
  `ihsan` (Ali), `most-mentioned` → dropped (the `mentioned_in` list shows it).

### Asma ul Husna
- All 99 names tagged: `asma_ul_husna` + 1–4 themes (e.g. Ar-Razzaq → `rizq`,
  `tawakkul`, `work_ethics`; Al-Wadud → `love_of_allah`, `rahmah`, `tawbah`).
- Duplicate categories merged: "Essential Names" + "Names of Essential Names" →
  "Names of Essential Nature"; "Names of Mercy" → "Names of Forgiveness & Mercy".
- `main.py` now writes `tags:` into each Asma note's frontmatter.

---

## Data notes (reported, not changed)

- Asma #49 and #66 are both transliterated "Al-Majid" (المجيد / الماجد); #56 and #78
  are both "Al-Wali" (الولي / الوالي).
- `data/quran_personalities.py` is out of sync with the JSON: `connections` already
  differed for 6 entries before this work, and tags now differ for all 79.
  `main.py` reads only the JSON.
- `munkar_nakeer` and `sumayyah` have no `mentioned_in` ayaat (neither is named in the
  Quran).
- Asma notes are written without reading back the personal section after
  `GENERATED:END`, so anything written there would be overwritten on the next run.

---

## Phase 5 — review notes (2026-09-18)

- **Coverage:** 6,236 / 6,236 ayaat, average 2.56 tags per ayah. All 138 themes are
  used on ayaat; none is empty.
- **Exact-count checks passed** (`tag_audit.py` plus a text comparison against
  `data/en.json`):
  - `sajdah_tilawah` — exactly the 15 marked ayaat of the Mushaf.
  - `muqattaat` — exactly the 29 surahs that open with disjointed letters (30 ayaat,
    counting 42:2).
  - `o_believers` — 89 ayaat, matching every "O you who have believed" in the
    translation, with none mistagged and none missed.
- **Largest themes:** `akhirah` 794, `kufr` 733, `revelation` 439, `story_musa` 405,
  `nature_signs` 400. **Smallest:** `story_alyasa` 1, `story_dhulkifl` 2,
  `story_idris` 3, `battle_hunayn` 3 — each matching how briefly the Quran mentions them.
- **Cross-type reach:** every theme page on the site can now mix ayaat, personalities
  and Names of Allah, e.g. `sabr` = 112 ayaat + 15 personalities + 1 Name;
  `oppression` = 150 + 11 + 6; `story_musa` = 405 ayaat + 8 personalities.

---

## Session log

| Date | Work |
|------|------|
| 2026-09-17 | Phases 1–3 done. Created `ayah_tags/` and `tag_audit.py`; migrated 344 seed ayaat. |
| 2026-09-17 | Phase 4: surahs 1–72 deep-tagged. |
| 2026-09-18 | Phase 4 finished: surahs 73–114. All 6,236 ayaat tagged, all 138 themes in use. Phase 5 review done. |
| 2026-09-18 | Emojis removed from `THEMES` (5-tuple → 4-tuple). Index gained a **Notes** column from `main.theme_counts()` — ayaat + personalities + Names per tag. |

---

## Surah status

Generated by `python tag_audit.py --write` — do not edit by hand.
seed = partial tags from the original seed set · deep = every ayah reviewed.

<!-- AUDIT:START -->
- **Ayaat tagged:** 6236 / 6236 (100.0%)
- **Surahs deep-tagged:** 114 / 114 (6236 ayaat, 100.0% of the Quran)
- **Surahs with seed tags only:** 0 · **untouched:** 0
- **Themes:** 138 · on ayaat: 138 · not yet on any ayah: 0
- **Personalities tagged:** 79 / 79 · **Names of Allah tagged:** 99 / 99

| # | Surah | Ayaat | Tagged | Tags/ayah | Status |
|---|-------|-------|--------|-----------|--------|
| 1 | Al-Fatihah | 7 | 7 | 3.1 | deep |
| 2 | Al-Baqarah | 286 | 286 | 3.2 | deep |
| 3 | Ali 'Imran | 200 | 200 | 3.0 | deep |
| 4 | An-Nisa | 176 | 176 | 3.0 | deep |
| 5 | Al-Ma'idah | 120 | 120 | 3.2 | deep |
| 6 | Al-An'am | 165 | 165 | 2.7 | deep |
| 7 | Al-A'raf | 206 | 206 | 2.7 | deep |
| 8 | Al-Anfal | 75 | 75 | 2.9 | deep |
| 9 | At-Tawbah | 129 | 129 | 3.1 | deep |
| 10 | Yunus | 109 | 109 | 2.5 | deep |
| 11 | Hud | 123 | 123 | 2.6 | deep |
| 12 | Yusuf | 111 | 111 | 2.8 | deep |
| 13 | Ar-Ra'd | 43 | 43 | 3.0 | deep |
| 14 | Ibrahim | 52 | 52 | 2.8 | deep |
| 15 | Al-Hijr | 99 | 99 | 2.1 | deep |
| 16 | An-Nahl | 128 | 128 | 2.6 | deep |
| 17 | Al-Isra | 111 | 111 | 2.5 | deep |
| 18 | Al-Kahf | 110 | 110 | 2.5 | deep |
| 19 | Maryam | 98 | 98 | 2.5 | deep |
| 20 | Taha | 135 | 135 | 2.4 | deep |
| 21 | Al-Anbya | 112 | 112 | 2.3 | deep |
| 22 | Al-Hajj | 78 | 78 | 2.7 | deep |
| 23 | Al-Mu'minun | 118 | 118 | 2.1 | deep |
| 24 | An-Nur | 64 | 64 | 2.9 | deep |
| 25 | Al-Furqan | 77 | 77 | 2.4 | deep |
| 26 | Ash-Shu'ara | 227 | 227 | 2.0 | deep |
| 27 | An-Naml | 93 | 93 | 2.6 | deep |
| 28 | Al-Qasas | 88 | 88 | 2.6 | deep |
| 29 | Al-'Ankabut | 69 | 69 | 2.6 | deep |
| 30 | Ar-Rum | 60 | 60 | 2.4 | deep |
| 31 | Luqman | 34 | 34 | 3.1 | deep |
| 32 | As-Sajdah | 30 | 30 | 2.4 | deep |
| 33 | Al-Ahzab | 73 | 73 | 3.0 | deep |
| 34 | Saba | 54 | 54 | 2.5 | deep |
| 35 | Fatir | 45 | 45 | 2.4 | deep |
| 36 | Ya-Sin | 83 | 83 | 1.9 | deep |
| 37 | As-Saffat | 182 | 182 | 1.8 | deep |
| 38 | Sad | 88 | 88 | 2.2 | deep |
| 39 | Az-Zumar | 75 | 75 | 2.5 | deep |
| 40 | Ghafir | 85 | 85 | 2.5 | deep |
| 41 | Fussilat | 54 | 54 | 2.7 | deep |
| 42 | Ash-Shuraa | 53 | 53 | 2.9 | deep |
| 43 | Az-Zukhruf | 89 | 89 | 2.6 | deep |
| 44 | Ad-Dukhan | 59 | 59 | 2.1 | deep |
| 45 | Al-Jathiyah | 37 | 37 | 2.7 | deep |
| 46 | Al-Ahqaf | 35 | 35 | 3.1 | deep |
| 47 | Muhammad | 38 | 38 | 3.0 | deep |
| 48 | Al-Fath | 29 | 29 | 3.3 | deep |
| 49 | Al-Hujurat | 18 | 18 | 3.7 | deep |
| 50 | Qaf | 45 | 45 | 2.3 | deep |
| 51 | Adh-Dhariyat | 60 | 60 | 2.4 | deep |
| 52 | At-Tur | 49 | 49 | 2.2 | deep |
| 53 | An-Najm | 62 | 62 | 2.3 | deep |
| 54 | Al-Qamar | 55 | 55 | 2.4 | deep |
| 55 | Ar-Rahman | 78 | 78 | 1.8 | deep |
| 56 | Al-Waqi'ah | 96 | 96 | 1.8 | deep |
| 57 | Al-Hadid | 29 | 29 | 3.3 | deep |
| 58 | Al-Mujadila | 22 | 22 | 3.4 | deep |
| 59 | Al-Hashr | 24 | 24 | 3.4 | deep |
| 60 | Al-Mumtahanah | 13 | 13 | 4.3 | deep |
| 61 | As-Saf | 14 | 14 | 3.4 | deep |
| 62 | Al-Jumu'ah | 11 | 11 | 3.4 | deep |
| 63 | Al-Munafiqun | 11 | 11 | 3.5 | deep |
| 64 | At-Taghabun | 18 | 18 | 3.2 | deep |
| 65 | At-Talaq | 12 | 12 | 3.6 | deep |
| 66 | At-Tahrim | 12 | 12 | 4.4 | deep |
| 67 | Al-Mulk | 30 | 30 | 2.7 | deep |
| 68 | Al-Qalam | 52 | 52 | 2.4 | deep |
| 69 | Al-Haqqah | 52 | 52 | 2.1 | deep |
| 70 | Al-Ma'arij | 44 | 44 | 2.2 | deep |
| 71 | Nuh | 28 | 28 | 3.1 | deep |
| 72 | Al-Jinn | 28 | 28 | 3.2 | deep |
| 73 | Al-Muzzammil | 20 | 20 | 2.6 | deep |
| 74 | Al-Muddaththir | 56 | 56 | 2.2 | deep |
| 75 | Al-Qiyamah | 40 | 40 | 2.0 | deep |
| 76 | Al-Insan | 31 | 31 | 2.3 | deep |
| 77 | Al-Mursalat | 50 | 50 | 1.9 | deep |
| 78 | An-Naba | 40 | 40 | 2.0 | deep |
| 79 | An-Nazi'at | 46 | 46 | 2.3 | deep |
| 80 | 'Abasa | 42 | 42 | 2.0 | deep |
| 81 | At-Takwir | 29 | 29 | 2.3 | deep |
| 82 | Al-Infitar | 19 | 19 | 2.1 | deep |
| 83 | Al-Mutaffifin | 36 | 36 | 2.0 | deep |
| 84 | Al-Inshiqaq | 25 | 25 | 2.4 | deep |
| 85 | Al-Buruj | 22 | 22 | 2.4 | deep |
| 86 | At-Tariq | 17 | 17 | 1.8 | deep |
| 87 | Al-A'la | 19 | 19 | 2.2 | deep |
| 88 | Al-Ghashiyah | 26 | 26 | 1.6 | deep |
| 89 | Al-Fajr | 30 | 30 | 2.5 | deep |
| 90 | Al-Balad | 20 | 20 | 2.5 | deep |
| 91 | Ash-Shams | 15 | 15 | 2.5 | deep |
| 92 | Al-Layl | 21 | 21 | 2.4 | deep |
| 93 | Ad-Duhaa | 11 | 11 | 3.0 | deep |
| 94 | Ash-Sharh | 8 | 8 | 2.8 | deep |
| 95 | At-Tin | 8 | 8 | 2.6 | deep |
| 96 | Al-'Alaq | 19 | 19 | 2.4 | deep |
| 97 | Al-Qadr | 5 | 5 | 2.8 | deep |
| 98 | Al-Bayyinah | 8 | 8 | 3.4 | deep |
| 99 | Az-Zalzalah | 8 | 8 | 2.4 | deep |
| 100 | Al-'Adiyat | 11 | 11 | 2.7 | deep |
| 101 | Al-Qari'ah | 11 | 11 | 1.5 | deep |
| 102 | At-Takathur | 8 | 8 | 2.2 | deep |
| 103 | Al-'Asr | 3 | 3 | 3.3 | deep |
| 104 | Al-Humazah | 9 | 9 | 1.7 | deep |
| 105 | Al-Fil | 5 | 5 | 2.6 | deep |
| 106 | Quraysh | 4 | 4 | 3.2 | deep |
| 107 | Al-Ma'un | 7 | 7 | 2.9 | deep |
| 108 | Al-Kawthar | 3 | 3 | 3.7 | deep |
| 109 | Al-Kafirun | 6 | 6 | 2.8 | deep |
| 110 | An-Nasr | 3 | 3 | 3.7 | deep |
| 111 | Al-Masad | 5 | 5 | 3.0 | deep |
| 112 | Al-Ikhlas | 4 | 4 | 3.0 | deep |
| 113 | Al-Falaq | 5 | 5 | 3.2 | deep |
| 114 | An-Nas | 6 | 6 | 2.7 | deep |
<!-- AUDIT:END -->
