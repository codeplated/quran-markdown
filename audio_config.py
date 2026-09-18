# ══════════════════════════════════════════════════════════════════════════════
#  AUDIO CONFIGURATION
#  Replace the existing audio config block and functions in main.py with this.
#
#  AUDIO_MODE options:
#    "local"  →  file:// absolute path  (Obsidian on your machine)
#    "api"    →  cdn.islamic.app CDN    (website — no upload needed)
#    "r2"     →  your Cloudflare R2     (website — your own bucket)
# ══════════════════════════════════════════════════════════════════════════════
import os
AUDIO_MODE      = "api"                              # "local" | "api" | "r2"
#AUDIO_BASE_PATH = "./data/audio"                     # used in "local" mode only
AUDIO_BASE_PATH  = "./data/AlafasyAudio"  
AUDIO_EXT       = ".mp3"
R2_BASE_URL     = "https://assets.yourdomain.com"   # used in "r2" mode only
API_RECITER     = "ar.alafasy"                       # used in "api" mode only

# ── Global ayah number lookup (required for "api" mode) ───────────────────────
#
# cdn.islamic.app addresses every ayah by a single number 1–6236,
# counting sequentially across all surahs.
# e.g. Al-Fatihah has 7 ayaat → Al-Baqarah starts at global ayah 8.
#
# AYAH_COUNTS[i] = number of ayaat in surah (i+1), index 0 = surah 1.

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
    5, 4, 5, 6,                                        # 111–114
]

# Pre-compute cumulative ayah offset for each surah so get_global_ayah()
# is O(1) instead of looping every call.
_CUMULATIVE = [0] * 115          # _CUMULATIVE[s] = total ayaat before surah s
for _s in range(1, 115):
    _CUMULATIVE[_s] = _CUMULATIVE[_s - 1] + AYAH_COUNTS[_s - 1]


def get_global_ayah(surah_num: int, ayah_num: int) -> int:
    """
    Converts (surah, ayah) to a global ayah number 1–6236.

    Examples:
        get_global_ayah(1, 1)   →  1   (first ayah of Al-Fatihah)
        get_global_ayah(1, 7)   →  7   (last ayah of Al-Fatihah)
        get_global_ayah(2, 1)   →  8   (first ayah of Al-Baqarah)
        get_global_ayah(2, 255) →  262 (Ayat al-Kursi)
        get_global_ayah(114, 6) →  6236 (last ayah of Quran)
    """
    return _CUMULATIVE[surah_num - 1] + ayah_num


def audio_path(surah_num: int, ayah_num: int) -> str:
    """
    Returns the relative audio path used in "local" and "r2" modes.
    Matches your existing folder structure: 017/000.mp3
    (ayah_num is 1-based in your data, stored as 0-padded in folders)
    """
    folder = str(surah_num).zfill(3)
    file   = str(ayah_num).zfill(3)
    return f"{folder}{file}{AUDIO_EXT}"


def audio_embed(surah_num: int, ayah_num: int) -> str:
    """
    Returns the HTML audio embed for an ayah.
    Behaviour is controlled by AUDIO_MODE at the top of this block.

    "local"  →  <audio controls src="file:///abs/path/017/000.mp3"></audio>
    "api"    →  <audio controls src="https://cdn.islamic.app/.../262.mp3"></audio>
    "r2"     →  <audio controls src="https://assets.yourdomain.com/audio/017/000.mp3"></audio>
    """
    if AUDIO_MODE == "api":
        global_ayah = get_global_ayah(surah_num, ayah_num)
        url = f"https://cdn.islamic.app/quran/audio/{API_RECITER}/{global_ayah}.mp3"

    elif AUDIO_MODE == "r2":
        rel_path = audio_path(surah_num, ayah_num)
        url = f"{R2_BASE_URL}/audio/{rel_path}"

    else:  # "local"
        rel_path = audio_path(surah_num, ayah_num)
        abs_path = os.path.abspath(
            os.path.join(AUDIO_BASE_PATH, rel_path)
        ).replace("\\", "/")
        url = f"file://{abs_path}"

    return f'<audio controls src="{url}"></audio>'
