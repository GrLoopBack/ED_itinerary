#!/usr/bin/env python3
"""
Elite Dangerous – Smart Itinerary Helper (v2.7)
"""

import os
import time
import json
import glob
import subprocess
from pathlib import Path
from typing import List, Optional, Set

# ----------------------------------------------------------------------
# CONFIGURATION
# ----------------------------------------------------------------------
CONFIG_FILE = Path("config.json")

def load_config() -> dict:
    default = {
        "JOURNAL_DIR": str(Path.home() / ".local" / "share" / "Frontier Developments" / "Elite Dangerous"),
        "ITINERARY_FILE": "itinerary.txt",
        "POLL_INTERVAL": 2.0
    }
    if CONFIG_FILE.is_file():
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                user_cfg = json.load(f)
            default.update(user_cfg)
            print(f"Config loaded from {CONFIG_FILE}")
        except Exception as e:
            print(f"Bad config.json ({e}) → using defaults")
    else:
        print("No config.json → using defaults")
    return default

# ----------------------------------------------------------------------
# HELPERS
# ----------------------------------------------------------------------
def get_latest_journal(jdir: Path) -> Optional[Path]:
    pattern = str(jdir / "Journal.*.log")
    files = sorted(glob.glob(pattern), key=os.path.getmtime, reverse=True)
    return Path(files[0]) if files else None

def tail_journal(jpath: Path, pos: int) -> tuple[str, int]:
    with open(jpath, "r", encoding="utf-8", errors="ignore") as f:
        f.seek(pos)
        text = f.read()
        new_pos = f.tell()
    return text, new_pos

def extract_visited(lines: List[str], itinerary: List[str]) -> Set[str]:
    visited: Set[str] = set()
    for line in reversed(lines):
        try:
            data = json.loads(line)
            if data.get("event") in ("FSDJump", "Location", "CarrierJump"):
                sys = data.get("StarSystem")
                if sys in itinerary:
                    visited.add(sys)
        except json.JSONDecodeError:
            continue
    return visited

def copy_to_clipboard(text: str) -> None:
    try:
        subprocess.run(
            ["xclip", "-selection", "clipboard"],
            input=text.encode("utf-8"),
            check=True
        )
    except Exception as e:
        print(f"Clipboard failed: {e}")

def load_itinerary(path: Path) -> List[str]:
    if not path.is_file():
        print(f"Itinerary file not found: {path}")
        return []
    systems = []
    with open(path, "r", encoding="utf-8") as f:
        for raw in f:
            line = raw.split("#", 1)[0].strip()
            if line:
                systems.append(line)
    return systems

# ----------------------------------------------------------------------
# MAIN LOGIC – TRUE SKIP DETECTION ONLY
# ----------------------------------------------------------------------
def main() -> None:
    print("Elite Dangerous Itinerary Helper v2.7 – TRUE SKIP DETECTION")
    cfg = load_config()
    JOURNAL_DIR = Path(cfg["JOURNAL_DIR"])
    ITINERARY_FILE = Path(cfg["ITINERARY_FILE"])
    POLL_INTERVAL = float(cfg["POLL_INTERVAL"])

    print(f"Journal: {JOURNAL_DIR}")
    print(f"Itinerary: {ITINERARY_FILE}")
    print(f"Poll: {POLL_INTERVAL}s")

    itinerary = load_itinerary(ITINERARY_FILE)
    if not itinerary:
        print("No systems in itinerary. Exiting.")
        return

    print(f"Loaded {len(itinerary)} system(s): {', '.join(itinerary[:5])}...")

    current_journal: Optional[Path] = None
    pos = 0
    known_lines: List[str] = []
    last_visited_str = ""
    last_copied = ""

    while True:
        latest = get_latest_journal(JOURNAL_DIR)
        if latest != current_journal:
            if current_journal:
                print(f"New journal: {latest.name}")
            current_journal = latest
            pos = 0
            known_lines = []

        if not current_journal:
            time.sleep(POLL_INTERVAL)
            continue

        new_text, pos = tail_journal(current_journal, pos)
        if new_text:
            known_lines.extend(new_text.splitlines())

        visited = extract_visited(known_lines, itinerary)
        visited_str = ", ".join(sorted(visited))

        if visited_str != last_visited_str:
            last_visited_str = visited_str
            print(f"\n[*] Visited: {visited_str or 'none yet'}")

            # Find expected next (first unvisited in sequence)
            expected_next_idx = 0
            for i, sys in enumerate(itinerary):
                if sys not in visited:
                    expected_next_idx = i
                    break

            if expected_next_idx == len(itinerary):
                print("🎉 ALL SYSTEMS VISITED! Mission complete! o7")
            else:
                next_sys = itinerary[expected_next_idx]
                print(f"    NEXT SYSTEM (on clipboard): **{next_sys}**")
                if next_sys != last_copied:
                    copy_to_clipboard(next_sys)
                    print("       Copied! (Ctrl+V in-game)")
                    last_copied = next_sys
                else:
                    print("       Already on clipboard")

                # TRUE SKIP: Check if ANY system AFTER expected_next is visited
                has_skipped = any(sys in visited for sys in itinerary[expected_next_idx + 1:])

                if has_skipped:
                    print(f"    ⚠️  SKIPPED ahead: visit {next_sys} next")
                else:
                    print("    ✅ On track - no skips.")

        time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nStopped by user.")
