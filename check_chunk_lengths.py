"""
Criterion 4 check: what fraction of ALL stored chunks fall within the target
word-length range?

This reads directly from your existing Chroma collection (same one store.py
builds and searches), rather than rebuilding chunks separately -- so it checks
exactly what's actually indexed and searchable.

Usage:
    python check_chunk_lengths.py
    python check_chunk_lengths.py --corpus city_guides --variant default
"""

import argparse

import config
import store


LOW = 30
HIGH = 150


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus", default=None, help="corpus name (defaults to config.CORPUS)")
    parser.add_argument("--variant", default="default")
    args = parser.parse_args()

    name = config.collection_name(args.corpus, args.variant)
    collection = store._client().get_collection(name)

    raw = collection.get()  # no query needed -- just pull everything stored
    texts = raw["documents"]

    word_counts = [len(t.split()) for t in texts]
    total = len(word_counts)
    in_range = sum(1 for wc in word_counts if LOW <= wc <= HIGH)
    pct = 100 * in_range / total if total else 0

    print(f"Collection: {name}")
    print(f"Total chunks: {total}")
    print(f"In range [{LOW}, {HIGH}] words: {in_range} ({pct:.1f}%)")
    print(f"Shortest: {min(word_counts)} words")
    print(f"Longest: {max(word_counts)} words")
    print(f"Average: {sum(word_counts) / total:.1f} words")

    print("\nChunks outside the range:")
    for t, wc in zip(texts, word_counts):
        if not (LOW <= wc <= HIGH):
            preview = t.strip().replace("\n", " ")[:60]
            print(f"  {wc} words: {preview}...")


if __name__ == "__main__":
    main()