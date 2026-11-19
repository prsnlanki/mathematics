"""Build the Mathematics Anki deck (Mathematics.apkg): every subdeck folder here, packaged into one file.

Each subdeck's build.py makes its notes and checks them; this writes them all into Mathematics, so
one import adds or updates the whole deck.
"""
import importlib.util
import os

import genanki

HERE = os.path.dirname(os.path.abspath(__file__))
PARTS = ["multiplication"]
OUT = os.path.join(HERE, "Mathematics.apkg")


def part(name):
    """A subdeck's build module, loaded under its own name (every subdeck's file is build.py)."""
    spec = importlib.util.spec_from_file_location(f"{name}_build", os.path.join(HERE, name, "build.py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def build(out=OUT):
    decks, media = [], {}
    for name in PARTS:
        part_decks, part_media = part(name).build()
        decks += part_decks
        media |= {os.path.basename(path): path for path in part_media}
    package = genanki.Package(decks)
    package.media_files = sorted(media.values())
    package.write_to_file(out)
    print(f"{sum(len(d.notes) for d in decks)} notes, {len(media)} media files -> {out}")


if __name__ == "__main__":
    build()
