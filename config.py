"""
Central configuration for the Tadabbur note generator.

Every setting has a working default, so `python main.py` runs with no setup at
all. To change something, either export an environment variable or copy
`.env.example` to `.env` and edit that — `.env` is read automatically and is
git-ignored, so your local paths never end up in a commit.

Paths resolve against this file's location, never the shell's working
directory, so the generator behaves identically wherever you launch it from.
"""

from pathlib import Path

# ── Repository layout ────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"


# ── .env loading ─────────────────────────────────────────────────────────────

def _load_dotenv(path: Path) -> dict:
    """
    Reads a minimal .env file: KEY=value per line, # starts a comment.
    Deliberately tiny — the project has no third-party dependencies, and this
    is all the .env syntax we need. Real environment variables always win.
    """
    values = {}
    if not path.is_file():
        return values

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.split("#", 1)[0].strip()
        if not line or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")

    return values


_DOTENV = _load_dotenv(ROOT / ".env")


def _get(key: str, default: str) -> str:
    """Setting lookup: real environment first, then .env, then the default."""
    import os
    return os.environ.get(key) or _DOTENV.get(key) or default


def _path(key: str, default: str) -> Path:
    """Like _get, but resolves relative paths against the repo root."""
    return (ROOT / _get(key, default)).resolve()


# ── Where the vault is written ───────────────────────────────────────────────
VAULT_PATH = _path("VAULT_PATH", "../Tadabbur")

# Folder inside the vault that holds the generated indexes, Names of Allah
# and Personalities notes. Everything else is one folder per surah.
EXPLORE_DIR = _get("EXPLORE_DIR", "0 - Explore")

ASMA_DIR = f"{EXPLORE_DIR}/Asma Ul Husna"
PERSONALITIES_DIR = f"{EXPLORE_DIR}/Personalities"
ATTACHMENTS_DIR = "attachments"


# ── Audio ────────────────────────────────────────────────────────────────────
# "api"   → stream from a public CDN; nothing to download (default)
# "local" → file:// links into a local folder of mp3s, for offline Obsidian
# "r2"    → your own bucket or CDN; requires AUDIO_R2_BASE_URL
AUDIO_MODE = _get("AUDIO_MODE", "api")

AUDIO_API_RECITER = _get("AUDIO_API_RECITER", "ar.alafasy")
AUDIO_API_BASE_URL = _get("AUDIO_API_BASE_URL", "https://cdn.islamic.app/quran/audio")

AUDIO_R2_BASE_URL = _get("AUDIO_R2_BASE_URL", "")

# Local mp3 collections ship in two different shapes, so the layout is a
# setting rather than an assumption:
#   "flat"   → 002001.mp3          (everyayah-style, one folder)
#   "nested" → 002/001.mp3         (one folder per surah)
AUDIO_LOCAL_PATH = _path("AUDIO_LOCAL_PATH", "data/AlafasyAudio")
AUDIO_LOCAL_LAYOUT = _get("AUDIO_LOCAL_LAYOUT", "flat")
AUDIO_EXT = _get("AUDIO_EXT", ".mp3")


# ── Source data files ────────────────────────────────────────────────────────
QURAN_JSON = DATA_DIR / "quran.json"
ENGLISH_JSON = DATA_DIR / "en.json"
URDU_JSON = DATA_DIR / "ur.json"
CHAPTERS_EN_JSON = DATA_DIR / "chapters" / "en.json"
CHAPTERS_UR_JSON = DATA_DIR / "chapters" / "ur.json"
ASMA_JSON = DATA_DIR / "asma_ul_husna.json"
PERSONALITIES_JSON = DATA_DIR / "quran_personalities.json"
TAFSIR_DIR = DATA_DIR / "ur-tazkirul-quran"


# ── Assets copied into the vault ─────────────────────────────────────────────
THUMBNAILS_SRC = _path("THUMBNAILS_SRC", "thumbnailGenerator/thumbnails")
VAULT_FILES_SRC = _path("VAULT_FILES_SRC", "vault_files")


# ── Note formatting ──────────────────────────────────────────────────────────
SENTINEL_START = "<!-- GENERATED:START -->"
SENTINEL_END = "<!-- GENERATED:END -->"

BISMILLAH = "بِسۡمِ ٱللَّهِ ٱلرَّحۡمَٰنِ ٱلرَّحِيمِ"


class ConfigError(Exception):
    """Raised when settings are inconsistent — reported before any file is written."""


def validate() -> None:
    """
    Fails fast on settings that would otherwise produce a broken vault
    silently, which is how a placeholder URL once shipped into every note.
    """
    valid_modes = {"api", "local", "r2"}
    if AUDIO_MODE not in valid_modes:
        raise ConfigError(
            f"AUDIO_MODE is {AUDIO_MODE!r}, expected one of {sorted(valid_modes)}"
        )

    if AUDIO_MODE == "r2" and not AUDIO_R2_BASE_URL:
        raise ConfigError(
            "AUDIO_MODE=r2 needs AUDIO_R2_BASE_URL to be set "
            "(e.g. https://assets.example.com)"
        )

    if AUDIO_MODE == "local":
        if not AUDIO_LOCAL_PATH.is_dir():
            raise ConfigError(
                f"AUDIO_MODE=local but no audio folder at {AUDIO_LOCAL_PATH}.\n"
                "        Audio is not distributed with this repo — see docs/LICENSES.md,\n"
                "        or use the default AUDIO_MODE=api which needs no local files."
            )
        valid_layouts = {"flat", "nested"}
        if AUDIO_LOCAL_LAYOUT not in valid_layouts:
            raise ConfigError(
                f"AUDIO_LOCAL_LAYOUT is {AUDIO_LOCAL_LAYOUT!r}, "
                f"expected one of {sorted(valid_layouts)}"
            )

    missing = [p for p in (QURAN_JSON, ENGLISH_JSON, URDU_JSON, ASMA_JSON,
                           PERSONALITIES_JSON) if not p.is_file()]
    if missing:
        listed = "\n          ".join(str(p) for p in missing)
        raise ConfigError(f"missing source data file(s):\n          {listed}")
