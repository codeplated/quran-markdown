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


# Says what kind of page this is, so the site leaves out its own title,
# properties box, reading time and tag chips: the note's head says all four.
AYAH_CLASS = "ayah"

TAFSIRS = (
    ("tafsir", "Bayan ul Quran", "Dr. Israr Ahmad"),
    ("tazkirul", "Tazkirul Quran", "Maulana Wahiduddin Khan"),
)


def step_links(surah: data.Surah, ayah: int) -> str:
    """
    The ayah before, the player, and the ayah after, in reading order on one
    line. An ayah at either end of its surah keeps an empty <span> in the
    missing slot, so the site can place the three by position.
    """
    previous = (
        f"[[{surah.note_name(ayah - 1)}|Prev {surah.number}:{ayah - 1}]]"
        if ayah > 1 else "<span></span>"
    )
    following = (
        f"[[{surah.note_name(ayah + 1)}|Next {surah.number}:{ayah + 1}]]"
        if ayah < surah.total_ayaat else "<span></span>"
    )
    return f"{previous} {audio.audio_embed(surah.number, ayah)} {following}"


def _tafsir(text: str, title: str, author: str) -> str:
    """
    One tafsir as a section the reader opens. Bayan ul Quran alone is three
    and a half phone screens on Ayat al-Kursi, and it sat between the
    translations and everything after them.
    """
    return f"""<details class="tafsir">
<summary>Tafsir: {title} <span class="by">{author}</span></summary>

{text}

</details>
"""


def build(surah: data.Surah, ayah: int, texts: dict) -> str:
    """
    The frontmatter and the script-owned block for one ayah.

    The verse comes first: a head that says where the ayah is, the player
    between the steps to the ayaat either side, then the Arabic, the English
    and the Urdu, the themes by name, and the two tafsirs folded.
    """
    tags = connections.get_ayah_themes(surah.number, ayah)

    head = notes.frontmatter({
        "title": notes.quote(surah.display_name(ayah)),
        "surah": f"{surah.number} / {data.SURAH_COUNT}",
        "surah_name": f"{surah.english} / {surah.arabic} / {surah.urdu}",
        "ayah": f"{ayah} / {surah.total_ayaat}",
        "type": surah.type,
        "tags": json.dumps(tags),
        "image": f'"{thumbnail_link(surah.number)}"',
        "cssclasses": f"[{AYAH_CLASS}]",
    })

    # The surah link lands on this ayah in the surah's full text.
    context = (
        f"[[{surah.index_path}#{ayah}|{surah.english}]] "
        f'<span lang="ur">{surah.urdu}</span> · <span lang="ar">{surah.arabic}</span> · '
        f"{surah.type.capitalize()} · Ayah {ayah} of {surah.total_ayaat}"
    )

    themes = notes.theme_links(tags, connections.THEMES, config.THEMES_DIR)
    themes_section = f"""
## Themes

{themes}
""" if themes else ""

    tafsirs = "\n".join(_tafsir(texts[key], title, author) for key, title, author in TAFSIRS)

    # Plain text: the site's contents list and Obsidian's outline print a
    # heading's markup as written.
    body = f"""# {surah.transliteration} {surah.number}:{ayah}

{context}

{step_links(surah, ayah)}

<small class="reciter">Recited by {config.AUDIO_RECITER_NAME}</small>

## Arabic

{texts['arabic']}

## English (Sahih International)

{texts['english']}

## Urdu (Syed Abul A'la Maududi)

{texts['urdu']}
{themes_section}
{tafsirs}"""

    return head + notes.wrap(body)


def generate() -> tuple:
    """Writes every ayah note. Returns (created, updated)."""
    created = updated = 0

    for surah_number_str, ayaat in data.quran.items():
        surah = data.SURAHS[int(surah_number_str)]

        # Folders at an older path were moved here by layout.migrate.
        folder = config.VAULT_PATH / surah.folder

        for entry in ayaat:
            ayah = entry["verse"]
            index = ayah - 1

            texts = {
                "arabic": arabic_text(surah.number, ayah, entry["text"]),
                "urdu": data.urdu[surah_number_str][index]["text"],
                "english": data.english[surah_number_str][index]["text"],
                "tafsir": data.load_tafsir(surah.number, ayah),
                "tazkirul": data.load_tazkirul(surah.number, ayah),
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
