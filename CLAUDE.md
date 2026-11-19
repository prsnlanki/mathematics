# Mathematics deck

The owner's mathematics Anki deck, `Mathematics` in Anki. It starts with one subdeck, **Multiplication** (`Mathematics::Multiplication`): the tables 2–20 × 2–20 as typed, timed product and division cards plus self-graded factoring cards, so the owner knows them instantly. The other Anki repos are in `~/organizations/prsnlanki` (GitHub org `prsnlanki`); follow the structure of `deutsch` (`build.py` with `PARTS`, `CHANGELOG.md`, `scripts/publish.sh`, `scripts/check-release-links.sh`).

The spec is `docs/BRIEF.md`; decisions are in `docs/DECISIONS.md`.

1. **Making or changing cards:** read `FLASHCARD_GUIDE.md` in [prsnlanki/anki-setup](https://github.com/prsnlanki/anki-setup) in full first and follow it.
2. **Keep note GUIDs stable**, so re-importing updates cards instead of duplicating them.
3. A new kind of card is a new subdeck folder (listed in `build.py`'s `PARTS`), not a new deck.
4. **Every release** adds a `## x.y.z (date)` section to `CHANGELOG.md` and points `README.md`'s download link at it; publish from `main` with `scripts/publish.sh`. When the deck's notes or description change, update its row in the Decks table of anki-setup's `README.md`.

## Not doing

- Audio.
- A speed limit or colour on the timer.
- Prime factorisation cards.

## Constraints

- Follow anki-setup's `FLASHCARD_GUIDE.md` and the prsnlanki deck conventions (see deutsch's `CLAUDE.md`).
- $0 development: local-ci, no GitHub Actions.
