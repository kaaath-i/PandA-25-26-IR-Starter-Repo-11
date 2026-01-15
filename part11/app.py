#!/usr/bin/env python3
"""
Part 11 starter.

WHAT'S NEW IN PART 11. A positional Index. It's almost done, only the finishing touches remain.
"""
from typing import List
import time

from .constants import BANNER, HELP
from .models import SearchResult, Searcher

from .file_utilities import load_config, load_sonnets, highlight_cmd, search_mode_cmd, hl_mode_cmd


def print_results(
    query: str | None,
    results: List[SearchResult],
    highlight: bool,
    query_time_ms: float | None = None,
    highlight_mode: str = "DEFAULT"
) -> None:
    total_docs = len(results)
    matched = [r for r in results if r.matches > 0]

    line = f'{len(matched)} out of {total_docs} sonnets contain "{query}".'
    if query_time_ms is not None:
        line += f" Your query took {query_time_ms:.2f}ms."
    print(line)

    for idx, r in enumerate(matched, start=1):
        r.print(idx, highlight, total_docs, highlight_mode)

# ---------- CLI loop ----------
def main() -> None:
    print(BANNER)
    config = load_config()

    # Load sonnets (from cache or API)
    start = time.perf_counter()
    sonnets = load_sonnets()

    elapsed = (time.perf_counter() - start) * 1000
    print(f"Loading sonnets took: {elapsed:.3f} [ms]")

    print(f"Loaded {len(sonnets)} sonnets.")

    searcher = Searcher(sonnets)

    while True:
        try:
            raw = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye.")
            break

        if not raw:
            continue

        # commands
        if raw.startswith(":"):
            if raw == ":quit":
                print("Bye.")
                break

            if raw == ":help":
                print(HELP)
                continue

            if highlight_cmd.get_mode(raw, config):
                continue

            if search_mode_cmd.get_mode(raw, config):
                continue

            if hl_mode_cmd.get_mode(raw, config):
                continue


            continue

        # ---------- Query evaluation ----------

        words = raw.split()
        if not words:
            continue

        start = time.perf_counter()

        results = searcher.search(raw, config.search_mode)

        # Initialize elapsed_ms to contain the number of milliseconds the query evaluation took
        elapsed_ms = (time.perf_counter() - start) * 1000

        print_results(raw, results, config.highlight, elapsed_ms, config.hl_mode)

if __name__ == "__main__":
    main()
