# ============================================================
# Pair Exercise #4: Wikipedia (Sequential vs Concurrent)
# Course: IST 303 - Fall 2025
# File: pe4.py
#
# Student: Adiya King
# Partner: N/A (solo)
#
# Description:
#   Section A: Sequentially fetch topics from Wikipedia, grab each
#   page's title and references, and write references to "<title>.txt".
#   Section B: Do the same work concurrently with ThreadPoolExecutor.
#
# Notes:
#   - Requires: pip install wikipedia
#   - Network must be available (calls Wikipedia).
#   - Files are written to the current folder.
# ============================================================

import time
import re
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

import wikipedia
from wikipedia.exceptions import DisambiguationError, PageError

# ---------- small helpers ----------

def sanitize_filename(title: str) -> str:
    """Make a safe filename from a Wikipedia title (replace illegal chars)."""
    return re.sub(r'[\\/:*?"<>|]+', "_", title).strip()

def write_references_to_file(title: str, references) -> Path:
    """
    Write references (one per line) to "<title>.txt".
    references is usually a list of strings (URLs).
    """
    safe = sanitize_filename(title)
    out_path = Path(f"{safe}.txt")
    with out_path.open("w", encoding="utf-8", errors="ignore") as f:
        for ref in references:
            f.write(f"{ref}\n")
    return out_path

# ---------- SECTION A: Sequential ----------

def run_sequential(query: str = "generative artificial intelligence") -> None:
    start = time.perf_counter()

    topics = wikipedia.search(query)
    print(f"[Sequential] topics found: {len(topics)}")

    for topic in topics:
        try:
            # assignment asks for a variable named `page` and auto_suggest=False
            page = wikipedia.page(title=topic, auto_suggest=False)
            title = page.title
            references = page.references
            write_references_to_file(title, references)
            print(f"[Sequential] Saved refs for: {title}")
        except DisambiguationError as e:
            print(f"[Sequential] SKIP disambiguation: {topic} ({len(e.options)} options)")
        except PageError:
            print(f"[Sequential] SKIP page not found: {topic}")
        except Exception as e:
            print(f"[Sequential] SKIP unexpected for {topic}: {e}")

    elapsed = time.perf_counter() - start
    print(f"[Sequential] Finished in {elapsed:.2f} seconds")

# ---------- SECTION B: Concurrent ----------

def wiki_dl_and_save(topic: str) -> str:
    """
    Per assignment spec:
    - retrieve page for `topic` (auto_suggest=False)
    - get title and references
    - write them to "<title>.txt" (one ref per line)
    Return a short status string.
    """
    try:
        page = wikipedia.page(title=topic, auto_suggest=False)
        title = page.title
        references = page.references
        write_references_to_file(title, references)
        return f"OK: {title}"
    except DisambiguationError as e:
        return f"SKIP disambiguation: {topic} ({len(e.options)} options)"
    except PageError:
        return f"SKIP page not found: {topic}"
    except Exception as e:
        return f"SKIP unexpected for {topic}: {e}"

def run_concurrent(query: str = "generative artificial intelligence", max_workers: int = 8) -> None:
    start = time.perf_counter()

    topics = wikipedia.search(query)
    print(f"[Concurrent] topics found: {len(topics)}")

    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        for status in ex.map(wiki_dl_and_save, topics):
            print(f"[Concurrent] {status}")

    elapsed = time.perf_counter() - start
    print(f"[Concurrent] Finished in {elapsed:.2f} seconds")

# ---------- main ----------

if __name__ == "__main__":
    # Being polite to Wikipedia if it rate-limits
    wikipedia.set_rate_limiting(True)

    print("=== SECTION A: Sequential ===")
    run_sequential()

    print("\n=== SECTION B: Concurrent ===")
    run_concurrent()
