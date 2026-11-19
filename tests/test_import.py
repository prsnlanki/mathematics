"""Import the built deck into a throwaway Anki collection (the real `anki` package, no GUI) and check
what the owner will see: the deck, the note counts, re-import updating instead of duplicating, the
new-card order, and the typed-answer comparison. Run by .local-ci."""
import os
import sys
import tempfile

from anki.collection import Collection, ImportAnkiPackageOptions, ImportAnkiPackageRequest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import build  # noqa: E402

DECK = "Mathematics::Multiplication"


def import_apkg(col, path):
    col.import_anki_package(ImportAnkiPackageRequest(
        package_path=path, options=ImportAnkiPackageOptions(with_scheduling=False)))


def main():
    with tempfile.TemporaryDirectory() as tmp:
        apkg = os.path.join(tmp, "Mathematics.apkg")
        build.build(apkg)
        col = Collection(os.path.join(tmp, "collection.anki2"))
        import_apkg(col, apkg)

        nids = col.find_notes(f'"deck:{DECK}"')
        assert len(nids) == 865, len(nids)
        kinds = {k: len(col.find_notes(f'"deck:{DECK}" tag:kind::{k}')) for k in ("product", "division", "factoring")}
        assert kinds == {"product": 361, "division": 361, "factoring": 143}, kinds

        # Re-importing a rebuild updates the same notes.
        import_apkg(col, apkg)
        assert len(col.find_notes("")) == 865, len(col.find_notes(""))

        # New cards come in the built order: 2 × 2 first; every 2–10 product before any 13–19 product.
        cards = sorted((col.get_card(cid) for cid in col.find_cards(f'"deck:{DECK}"')), key=lambda c: c.due)
        assert all(c.type == 0 for c in cards)
        fields = [c.note().fields for c in cards]
        assert fields[0][:2] == ["2 × 2", "4"], fields[0]
        position = {f[0]: i for i, f in enumerate(fields)}
        last_easy = max(position[f"{a} × {b}"] for a in range(2, 11) for b in range(2, 11))
        first_hard = min(position[f"{a} × {b}"] for a in range(2, 21) for b in (13, 14, 16, 17, 18, 19))
        assert last_easy < first_hard, (last_easy, first_hard)
        assert position["56 ÷ 7"] > position["7 × 8"] + 30

        # The scheduler's queue starts at the same place.
        col.decks.select(col.decks.id(DECK))
        first = col.sched.get_queued_cards(fetch_limit=1).cards[0]
        assert col.get_card(first.card.id).note().fields[0] == "2 × 2"

        # A product card: typed input and timer on the front; a wrong answer is marked on the back.
        card = cards[position["7 × 8"]]
        front = card.question()
        assert "typeans" in front and 'id="math-timer"' in front and "7 × 8" in front, front
        assert col.compare_answer("56", "54") != col.compare_answer("56", "56")
        assert "typeBad" in col.compare_answer("56", "54") or "typeMissed" in col.compare_answer("56", "54")

        # A factoring card lists every pair.
        back = cards[position["36"]].answer()
        for pair in ("2 × 18", "3 × 12", "4 × 9", "6 × 6"):
            assert pair in back, back
        assert "4 pairs" in cards[position["36"]].question()
        col.close()
    print("import test passed: 865 notes, re-import updates, order and typed answers as built")


if __name__ == "__main__":
    main()
