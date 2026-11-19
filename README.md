# Mathematics

My mathematics deck: 865 notes in `Mathematics`, one subdeck per kind of card. It starts with **Multiplication**: the tables 2–20 × 2–20, so the answers come instantly.

**Import:** download [`Mathematics.apkg`](https://github.com/prsnlanki/mathematics/releases/download/v1.0.0/Mathematics.apkg) from the deck's [release](https://github.com/prsnlanki/mathematics/releases/tag/v1.0.0) (version 1.0.0; [all versions](https://github.com/prsnlanki/mathematics/releases), [changelog](CHANGELOG.md)) and open it with Anki (or **File → Import**). It adds or updates every subdeck at once. Notes keep stable IDs, so re-importing updates existing cards instead of duplicating them.

## Subdecks

| Subdeck | Notes | What's in it |
|---|---|---|
| [Multiplication](multiplication/) | 865 | 361 products (7 × 8, both orders) and 361 divisions (56 ÷ 7), typed, with a timer; 143 factoring cards (36 → every factor pair within 2–20), self-graded. New cards come easiest first |

Each folder has its `build.py` (its notes and checks) and a README on its cards and how to change them.

## Rebuilding

Each publish is a new version on the releases page, tagged `vx.y.z`: a major version when importing it needs a step in Anki (a renamed deck, say), a minor one for new cards, a patch for fixes. Before publishing, add the version and what changed to [`CHANGELOG.md`](CHANGELOG.md) and point the download link above at it; `scripts/check-release-links.sh` (part of `.local-ci`) fails until the links match. `.local-ci` also imports the built deck into a throwaway Anki collection (`tests/test_import.py`) and checks counts, re-import, card order and typed answers. Once merged, run `scripts/publish.sh` from the repository root: it builds the `.apkg` and creates the release, with that changelog section as its notes.

`build.py` here builds every subdeck in `PARTS` into `Mathematics.apkg`. To add a new kind of card, add a folder with its own `build.py` that returns its decks and media files from `build()`, and list it in `PARTS`.
