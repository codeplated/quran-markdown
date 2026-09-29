"""
The 6,236 ayah notes — one per verse, grouped into a folder per surah.
"""

import json

import config
import quranConnections as connections
from tadabbur import audio, data, notes


def thumbnail_link(surah: int) -> str:
    """Vault path of the surah thumbnail used as the note's cover image."""
    return f"/{config.ATTACHMENTS_DIR}/surah_{str(surah).zfill(3)}.png"


def arabic_text(surah: int, ayah: int, raw_text: str) -> str:
    """
    Prepends the Bismillah to the opening ayah of every surah except
    Al-Fatihah, where it is already ayah 1, and At-Tawbah, which has none.
    """
    if surah > 1 and surah != 9 and ayah == 1:
        return f"{config.BISMILLAH}\n\n{raw_text}"
    return raw_text


def build(surah: data.Surah, ayah: int, texts: dict) -> str:
    """Builds the frontmatter and the script-owned block for one ayah."""
    previous = (
        f"[[{surah.note_name(ayah - 1)}]]" if ayah > 1 else "_(Start of Surah)_"
    )
    following = (
        f"[[{surah.note_name(ayah + 1)}]]"
        if ayah < surah.total_ayaat else "_(End of Surah)_"
    )

    tags = connections.get_ayah_themes(surah.number, ayah)

    head = notes.frontmatter({
        "title": notes.quote(surah.display_name(ayah)),
        "surah": f"{surah.number} / {data.SURAH_COUNT}",
        "surah_name": f"{surah.english} / {surah.arabic} / {surah.urdu}",
        "ayah": f"{ayah} / {surah.total_ayaat}",
        "type": surah.type,
        "tags": json.dumps(tags),
        "image": f'"{thumbnail_link(surah.number)}"',
    })

    body = f"""## Recitation

{audio.audio_embed(surah.number, ayah)}
**Next:** {following}

---

## Arabic

{texts['arabic']}

---

## Urdu

{texts['urdu']}

---

## English

{texts['english']}

---

## Tafsir — Bayan ul Quran

{texts['tafsir']}

---

## Connections

- **Previous:** {previous}
- **Next:** {following}
- **Thematic:** *(add links here)*
"""

    return head + notes.wrap(body)


def generate() -> tuple:
    """Writes every ayah note. Returns (created, updated)."""
    created = updated = 0

    for surah_number_str, ayaat in data.quran.items():
        surah = data.SURAHS[int(surah_number_str)]

        # Folders used to be named '2 - The Cow البقرة', then '2 The Cow'.
        # Move anything still at an old path first, so a reader's personal
        # sections survive the rename instead of being stranded.
        for old_name in (f"{surah.number} - {surah.english} {surah.arabic}",
                         f"{surah.number} {surah.english}"):
            notes.rename_folder(config.VAULT_PATH, old_name, surah.folder_name)
        folder = config.VAULT_PATH / surah.folder_name

        for entry in ayaat:
            ayah = entry["verse"]
            index = ayah - 1

            texts = {
                "arabic": arabic_text(surah.number, ayah, entry["text"]),
                "urdu": data.urdu[surah_number_str][index]["text"],
                "english": data.english[surah_number_str][index]["text"],
                "tafsir": data.load_tafsir(surah.number, ayah),
            }

            notes.rename_note(
                folder,
                f"{surah.number}_{ayah}: {surah.english} {surah.arabic}.md",
                f"{surah.note_name(ayah)}.md",
            )

            is_new = notes.write_note(
                folder,
                f"{surah.note_name(ayah)}.md",
                build(surah, ayah, texts),
                notes.AYAH_PERSONAL,
            )

            if is_new:
                created += 1
            else:
                updated += 1

    return created, updated
