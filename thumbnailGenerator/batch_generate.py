#!/usr/bin/env python3
"""
Batch-generates all 114 surah thumbnails through a running local ComfyUI
instance, using the exported API-format workflow and the surah_themes.csv
theme list.

Requirements:
    pip install requests

Before running:
    1. Start ComfyUI normally (it must be listening on COMFY_URL below).
    2. Confirm the workflow JSON below is your exported "Save (API Format)"
       file, and that PROMPT_NODE_ID / FILENAME_NODE_ID match the node IDs
       in your graph (defaults below match ImageGenerationTest.json:
       node "4" = positive CLIPTextEncode, node "12" = SaveImage).

Usage:
    python3 batch_generate.py

Resumable: if interrupted, re-running will skip surahs already marked
"success" in generation_log.csv.
"""
import copy
import csv
import json
import time
from pathlib import Path

import requests

# ---- Config -----------------------------------------------------------
COMFY_URL = "http://127.0.0.1:8188"
WORKFLOW_PATH = Path("TextToImageQuran.json")
CSV_PATH = Path("surah_themes.csv")
LOG_PATH = Path("generation_log.csv")

PROMPT_NODE_ID = "4"      # CLIPTextEncode (positive prompt) node id
FILENAME_NODE_ID = "12"   # SaveImage node id

STYLE_SUFFIX = (
    ", minimalist digital matte painting, muted earthy palette, "
    "soft cinematic lighting, symmetrical composition, "
    "consistent art direction"
)

POLL_INTERVAL_SEC = 2
TIMEOUT_SEC = 600
# ------------------------------------------------------------------------


def load_workflow():
    with open(WORKFLOW_PATH, encoding="utf-8") as f:
        return json.load(f)


def load_rows():
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def load_completed():
    """Returns the set of surah numbers already marked 'success' in the log,
    so a re-run skips them instead of regenerating."""
    if not LOG_PATH.exists():
        return set()
    with open(LOG_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return {row["number"] for row in reader if row["status"] == "success"}


def queue_prompt(workflow):
    resp = requests.post(f"{COMFY_URL}/prompt", json={"prompt": workflow}, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    if "prompt_id" not in data:
        raise RuntimeError(f"Unexpected response from ComfyUI: {data}")
    return data["prompt_id"]


def wait_for_completion(prompt_id):
    start = time.time()
    while True:
        if time.time() - start > TIMEOUT_SEC:
            raise TimeoutError(f"Timed out waiting for prompt {prompt_id}")
        resp = requests.get(f"{COMFY_URL}/history/{prompt_id}", timeout=30)
        resp.raise_for_status()
        history = resp.json()
        if prompt_id in history:
            entry = history[prompt_id]
            status = entry.get("status", {})
            if status.get("completed") is True or status.get("status_str") == "success":
                return entry
            if status.get("status_str") == "error":
                raise RuntimeError(f"ComfyUI reported an error: {status}")
        time.sleep(POLL_INTERVAL_SEC)


def main():
    base_workflow = load_workflow()
    rows = load_rows()
    already_done = load_completed()

    print(f"Loaded {len(rows)} surahs. {len(already_done)} already completed, will skip.")

    write_header = not LOG_PATH.exists()
    with open(LOG_PATH, "a", newline="", encoding="utf-8") as logf:
        logwriter = csv.writer(logf)
        if write_header:
            logwriter.writerow(["number", "transliteration", "status", "prompt_id", "error"])

        for row in rows:
            number = row["number"].zfill(3)

            if number in already_done:
                continue

            name = row["transliteration"]
            prompt_text = row["flux_prompt"] + STYLE_SUFFIX
            prefix = f"surah_{number}_{name}"
        
            wf = copy.deepcopy(base_workflow)
            wf[PROMPT_NODE_ID]["inputs"]["text"] = prompt_text
            wf[FILENAME_NODE_ID]["inputs"]["filename_prefix"] = prefix

            print(f"[{number}/114] Generating {name}...", flush=True)
            try:
                prompt_id = queue_prompt(wf)
                wait_for_completion(prompt_id)
                print(f"    done.")
                logwriter.writerow([number, name, "success", prompt_id, ""])
            except Exception as e:
                print(f"    ERROR: {e}")
                logwriter.writerow([number, name, "error", "", str(e)])
            logf.flush()

    print("Batch complete. See generation_log.csv for a full report.")


if __name__ == "__main__":
    main()
