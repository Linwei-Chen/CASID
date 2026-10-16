#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Verify a downloaded CASID release against release_file_hashes.csv.

Checks, for every row in the manifest:
  1. the file exists
  2. its size matches
  3. its MD5 matches (full read)

Usage:
  python verify_download.py --root CASID-dataset [--workers 8]
"""
import argparse
import csv
import hashlib
import os
import sys
from multiprocessing import Pool

CHUNK = 1 << 20


def check(task):
    root, rel, size, md5 = task
    path = os.path.join(root, rel)
    if not os.path.isfile(path):
        return rel, "MISSING"
    if os.path.getsize(path) != int(size):
        return rel, "SIZE_MISMATCH"
    h = hashlib.md5()
    try:
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(CHUNK), b""):
                h.update(chunk)
    except OSError as e:
        return rel, "READ_ERROR(%s)" % e
    return rel, "OK" if h.hexdigest() == md5 else "MD5_MISMATCH"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True, help="downloaded dataset root")
    ap.add_argument("--workers", type=int, default=8)
    args = ap.parse_args()

    manifest = os.path.join(args.root, "release_file_hashes.csv")
    if not os.path.isfile(manifest):
        sys.exit("ERROR: %s not found (download incomplete?)" % manifest)

    tasks = []
    with open(manifest) as f:
        for row in csv.reader(f):
            if row and row[0] != "path":
                tasks.append((args.root, row[0], row[1], row[2]))
    print("verifying %d files ..." % len(tasks))

    n_ok = n_bad = 0
    bad = []
    with Pool(args.workers) as pool:
        for rel, status in pool.imap_unordered(check, tasks, chunksize=8):
            if status == "OK":
                n_ok += 1
            else:
                n_bad += 1
                bad.append((rel, status))
            if (n_ok + n_bad) % 500 == 0:
                print("  %d/%d" % (n_ok + n_bad, len(tasks)), flush=True)

    print("RESULT: %d OK, %d bad (total %d)" % (n_ok, n_bad, len(tasks)))
    for rel, status in bad[:20]:
        print("  %s: %s" % (status, rel))
    if n_bad:
        sys.exit(1)
    print("ALL FILES VERIFIED ✔")


if __name__ == "__main__":
    main()
