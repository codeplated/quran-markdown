#!/usr/bin/env python3
"""
Generates the Tadabbur Obsidian vault from the dataset in data/.

    python main.py                 build everything
    python main.py --only ayaat    build one part (ayaat, surahs, asma,
                                   personalities, index, assets) — repeatable
    python main.py --vault ../Test write somewhere else, without touching .env
    python main.py --quiet         only the summary

Settings live in config.py and can be overridden from .env — see .env.example.
Anything a reader writes below the GENERATED:END marker in a note is preserved
on every run.
"""

import argparse
import sys
import time

import config


def _banner(text: str) -> None:
    print("=" * 62)
    print(f"  {text}")
    print("=" * 62)


def build(parts: set, quiet: bool) -> None:
    """Runs the requested build steps in dependency order."""
    # Imported here so that --help and config errors are reported before the
    # dataset is read into memory.
    from tadabbur import (assets, asma_notes, ayah_notes, explore, personalities,
                          surah_index)

    results = []

    if "index" in parts:
        explore.write_index()
        explore.write_explore_index()
        explore.write_quran_base()
        results.append(("Index & base view", None, None))

    if "assets" in parts:
        copied = assets.copy_vault_files() + assets.copy_thumbnails()
        results.append(("Assets copied", copied, None))

    if "ayaat" in parts:
        if not quiet:
            print("  Ayaat …", flush=True)
        results.append(("Ayaat", *ayah_notes.generate()))

    if "surahs" in parts:
        if not quiet:
            print("  Surah indexes …", flush=True)
        results.append(("Surah indexes", *surah_index.generate()))

    if "asma" in parts:
        if not quiet:
            print("  Names of Allah …", flush=True)
        results.append(("Names of Allah", *asma_notes.generate()))

    if "personalities" in parts:
        if not quiet:
            print("  Personalities …", flush=True)
        results.append(("Personalities", *personalities.generate()))

    print()
    _banner("Summary")
    for label, created, updated in results:
        if created is None:
            print(f"  {label}")
        elif updated is None:
            print(f"  {label:<22} {created}")
        else:
            print(f"  {label:<22} {created:>5} new   {updated:>5} updated")
    print(f"\n  Vault: {config.VAULT_PATH}")
    print("  Personal sections below GENERATED:END were preserved.")
    print("=" * 62)


ALL_PARTS = ("index", "assets", "ayaat", "surahs", "asma", "personalities")


def parse_args(argv=None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--only",
        action="append",
        choices=ALL_PARTS,
        metavar="PART",
        help=f"build only this part; repeatable. one of: {', '.join(ALL_PARTS)}",
    )
    parser.add_argument("--vault", help="write to this vault path instead of the configured one")
    parser.add_argument("--quiet", action="store_true", help="print only the summary")
    return parser.parse_args(argv)


def main(argv=None) -> int:
    args = parse_args(argv)

    if args.vault:
        config.VAULT_PATH = (config.ROOT / args.vault).resolve()

    try:
        config.validate()
    except config.ConfigError as error:
        print(f"Configuration error: {error}", file=sys.stderr)
        print("Check .env or see .env.example for the available settings.", file=sys.stderr)
        return 1

    parts = set(args.only) if args.only else set(ALL_PARTS)

    if not args.quiet:
        _banner("Quran → Obsidian  ·  Tadabbur note generator")
        print(f"  Vault      {config.VAULT_PATH}")
        print(f"  Audio      {config.AUDIO_MODE}")
        print(f"  Building   {', '.join(sorted(parts))}\n")

    started = time.perf_counter()
    build(parts, args.quiet)
    print(f"  Finished in {time.perf_counter() - started:.1f}s")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
