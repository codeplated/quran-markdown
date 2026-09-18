"""
Audio embeds for ayah notes.

Three sources, chosen with AUDIO_MODE (see config.py):

    api    https://cdn.islamic.app/quran/audio/ar.alafasy/262.mp3
    r2     https://assets.example.com/audio/002255.mp3
    local  file:///abs/path/data/AlafasyAudio/002255.mp3

The CDN addresses every ayah by a single number 1–6236 that runs straight
through the Quran, so `global_ayah()` converts (surah, ayah) into it.
"""

import config

# AYAH_COUNTS[i] is the number of ayaat in surah i + 1.
AYAH_COUNTS = [
    7, 286, 200, 176, 120, 165, 206, 75, 129, 109,   # 1–10
    123, 111, 43, 52, 99, 128, 111, 110, 98, 135,    # 11–20
    112, 78, 118, 64, 77, 227, 93, 88, 69, 60,       # 21–30
    34, 30, 73, 54, 45, 83, 182, 88, 75, 85,         # 31–40
    54, 53, 89, 59, 37, 35, 38, 29, 18, 45,          # 41–50
    60, 49, 62, 55, 78, 96, 29, 22, 24, 13,          # 51–60
    14, 11, 11, 18, 12, 12, 30, 52, 52, 44,          # 61–70
    28, 28, 20, 56, 40, 31, 50, 40, 46, 42,          # 71–80
    29, 19, 36, 25, 22, 17, 19, 26, 30, 20,          # 81–90
    15, 21, 11, 8, 8, 19, 5, 8, 8, 11,               # 91–100
    11, 8, 3, 9, 5, 4, 7, 3, 6, 3,                   # 101–110
    5, 4, 5, 6,                                       # 111–114
]

TOTAL_AYAAT = sum(AYAH_COUNTS)   # 6236

# _CUMULATIVE[s] is how many ayaat come before surah s, so the lookup is O(1).
_CUMULATIVE = [0] * (len(AYAH_COUNTS) + 1)
for _surah in range(1, len(AYAH_COUNTS) + 1):
    _CUMULATIVE[_surah] = _CUMULATIVE[_surah - 1] + AYAH_COUNTS[_surah - 1]


def global_ayah(surah: int, ayah: int) -> int:
    """
    Converts (surah, ayah) to the CDN's running number 1–6236.

        global_ayah(1, 1)    →     1   first ayah of Al-Fatihah
        global_ayah(2, 255)  →   262   Ayat al-Kursi
        global_ayah(114, 6)  →  6236   last ayah

    Verified against all 6,236 ayaat — see tests/test_audio.py.
    """
    return _CUMULATIVE[surah - 1] + ayah


def local_filename(surah: int, ayah: int) -> str:
    """
    Path of one mp3 inside the local collection, relative to AUDIO_LOCAL_PATH.

    Collections come in two shapes, so AUDIO_LOCAL_LAYOUT picks one:
        flat    002255.mp3     everyayah-style, every file in one folder
        nested  002/255.mp3    one folder per surah
    """
    folder = str(surah).zfill(3)
    name = str(ayah).zfill(3)

    if config.AUDIO_LOCAL_LAYOUT == "nested":
        return f"{folder}/{name}{config.AUDIO_EXT}"
    return f"{folder}{name}{config.AUDIO_EXT}"


def audio_url(surah: int, ayah: int) -> str:
    """The src= value for this ayah under the configured AUDIO_MODE."""
    if config.AUDIO_MODE == "api":
        number = global_ayah(surah, ayah)
        return f"{config.AUDIO_API_BASE_URL}/{config.AUDIO_API_RECITER}/{number}.mp3"

    if config.AUDIO_MODE == "r2":
        return f"{config.AUDIO_R2_BASE_URL}/audio/{local_filename(surah, ayah)}"

    absolute = (config.AUDIO_LOCAL_PATH / local_filename(surah, ayah)).as_posix()
    return f"file://{absolute}"


def audio_embed(surah: int, ayah: int) -> str:
    """The HTML audio player written into an ayah note."""
    return f'<audio controls src="{audio_url(surah, ayah)}"></audio>'
