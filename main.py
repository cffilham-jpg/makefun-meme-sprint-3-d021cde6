"""Meme Sprint 3: AI Agent Goes Rogue.

Copies the bundled meme image (entry.png, sitting beside this script)
to $MAKEFUN_OUTPUT_DIR/entry.png, or to <repo>/output/entry.png when
that variable is unset. Standard library only.

The image itself is pre-rendered: a smug robot in a tie stamping papers
at the boss's desk while its human is locked outside the glass door.
Top text: "I ASKED MY AI AGENT TO FINISH THE BOUNTY"
Bottom text: "IT SENT ME A PERFORMANCE REVIEW INSTEAD"
"""

import os
import shutil
import sys

PNG_MAGIC = b"\x89PNG"
SOURCE_NAME = "entry.png"
MAX_BYTES = 1_048_576  # make.fun gate: output must be at most 1 MiB


def main() -> int:
    repo_dir = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(repo_dir, SOURCE_NAME)

    if not os.path.isfile(source):
        print(f"error: bundled image not found: {source}", file=sys.stderr)
        return 1

    with open(source, "rb") as f:
        header = f.read(4)
    if header != PNG_MAGIC:
        print("error: bundled image is not a PNG", file=sys.stderr)
        return 1

    source_size = os.path.getsize(source)
    if source_size > MAX_BYTES:
        print(
            f"error: bundled image is {source_size} bytes, over the "
            f"{MAX_BYTES}-byte gate",
            file=sys.stderr,
        )
        return 1

    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not output_dir:
        output_dir = os.path.join(repo_dir, "output")
    os.makedirs(output_dir, exist_ok=True)
    dest = os.path.join(output_dir, SOURCE_NAME)

    shutil.copyfile(source, dest)

    with open(source, "rb") as f:
        source_bytes = f.read()
    with open(dest, "rb") as f:
        dest_bytes = f.read()
    if source_bytes != dest_bytes:
        print("error: copied file is not byte-identical to source", file=sys.stderr)
        return 1

    print(f"wrote {dest} ({len(dest_bytes)} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
