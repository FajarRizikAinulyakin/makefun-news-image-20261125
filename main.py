#!/usr/bin/env python3
"""Write the finished front page to the output directory.

The poster for Wednesday 25 November 2026 lives in this repository as
entry.png. This program places an exact copy of it at
<output>/entry.png, where <output> is the directory named by the
MAKEFUN_OUTPUT_DIR environment variable, or /output when that variable
is not set.

The copy is verified with a SHA-256 digest: the digest of the file
written is compared with the digest of the file in the repository, and
the program fails loudly if they differ, so a partial or corrupted
copy can never pass as the entry.

Standard library only. No arguments, no network, no clock, no random
input: the same poster in gives the same bytes out, every run.
"""

import hashlib
import os
import sys

POSTER = "entry.png"
FALLBACK_OUTPUT = "/output"
OUTPUT_ENV = "MAKEFUN_OUTPUT_DIR"


def poster_path():
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, POSTER)


def output_path():
    folder = os.environ.get(OUTPUT_ENV) or FALLBACK_OUTPUT
    return os.path.join(folder, POSTER)


def digest(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            chunk = f.read(65536)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def main():
    src = poster_path()
    dst = output_path()
    parent = os.path.dirname(dst)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(src, "rb") as fin, open(dst, "wb") as fout:
        while True:
            chunk = fin.read(65536)
            if not chunk:
                break
            fout.write(chunk)
    if os.path.getsize(src) != os.path.getsize(dst):
        raise SystemExit(
            "entry.png copy failed size check: source "
            f"{os.path.getsize(src)} bytes, copy "
            f"{os.path.getsize(dst)} bytes"
        )
    written_digest = digest(dst)
    if digest(src) != written_digest:
        raise SystemExit("entry.png copy failed digest check")
    print("wrote", dst, "sha256", written_digest[:16])
    return 0


if __name__ == "__main__":
    sys.exit(main())
