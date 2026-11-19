"""The Multiplication subdeck: the tables 2–20 × 2–20, generated here. ../build.py packages it.

Three kinds of card, in one new-card order (easiest first, see order()):
- product:   a × b = ?   typed, timed (361, both orders)
- division:  ab ÷ a = ?  typed, timed (361, one per ordered pair)
- factoring: n = ? × ?   every factor pair within 2–20, self-graded (143, one per distinct product)
"""
import genanki

DECK = "Mathematics::Multiplication"
DECK_ID = 2995290244489620564
TYPED_MODEL_ID = 3106140163166293080
FACTOR_MODEL_ID = 1970006236520606976

LOW, HIGH = 2, 20
FACTORS = range(LOW, HIGH + 1)
HARD = {13, 14, 16, 17, 18, 19}  # the last band; ×11, ×12, ×15 and ×20 come before it
DIVISION_DELAY = 30  # a division card follows its product card by 30 products (~3 days at 20 new cards/day)

CSS = """
.card { font-family: -apple-system, "Segoe UI", Roboto, sans-serif; font-size: 22px;
        text-align: center; max-width: 640px; margin: 0 auto; padding: 12px; }
.q { font-size: 44px; font-weight: 700; margin: 24px 0 8px; font-variant-numeric: tabular-nums; }
.timer { font-size: 15px; opacity: .55; font-variant-numeric: tabular-nums; min-height: 1.4em; }
.hint { font-size: 15px; opacity: .55; }
.pairs { font-size: 28px; line-height: 1.6; margin-top: 12px; font-variant-numeric: tabular-nums; }
#typeans { text-align: center; font-size: 28px; }
hr#answer { opacity: .3; }
"""

# The timer: the front counts whole seconds from when the card appears; the back shows the time it
# took. Anki desktop keeps one page for both sides (window state survives), AnkiDroid loads the back
# as a new page (sessionStorage survives), so the start time is kept in both, keyed by the question.
TIMER_FRONT = """<script>
(function () {
  var t = window.mathTimer = window.mathTimer || {};
  if (t.id) clearInterval(t.id);
  t.key = document.getElementById("math-q").textContent;
  t.start = Date.now();
  try { sessionStorage.setItem("mathTimer", JSON.stringify({ key: t.key, start: t.start })); } catch (e) {}
  var el = document.getElementById("math-timer");
  function tick() { el.textContent = Math.floor((Date.now() - t.start) / 1000) + " s"; }
  tick();
  t.id = setInterval(tick, 250);
})();
</script>"""

TIMER_BACK = """<script>
(function () {
  var t = window.mathTimer || {};
  if (t.id) { clearInterval(t.id); t.id = null; }
  var key = document.getElementById("math-q").textContent;
  var start = t.key === key ? t.start : null;
  if (start == null) {
    try {
      var s = JSON.parse(sessionStorage.getItem("mathTimer"));
      if (s && s.key === key) start = s.start;
    } catch (e) {}
  }
  if (start != null) {
    document.getElementById("math-timer").textContent = ((Date.now() - start) / 1000).toFixed(1) + " s";
  }
})();
</script>"""

TYPED_Q = """<div class="q" id="math-q">{{Question}}</div>
<div class="timer" id="math-timer"></div>
{{type:Answer}}
""" + TIMER_FRONT

TYPED_A = """<div class="q" id="math-q">{{Question}}</div>
<div class="timer" id="math-timer"></div>
<hr id="answer">
{{type:Answer}}
""" + TIMER_BACK

FACTOR_Q = """<div class="q">{{Product}} = ? × ?</div>
<div class="hint">{{Count}}, factors 2–20</div>"""

FACTOR_A = """{{FrontSide}}
<hr id="answer">
<div class="pairs">{{Pairs}}</div>"""

TYPED_MODEL = genanki.Model(
    TYPED_MODEL_ID, "Mathematics (typed, timed)",
    fields=[{"name": "Question"}, {"name": "Answer"}],
    templates=[{"name": "Typed", "qfmt": TYPED_Q, "afmt": TYPED_A}],
    css=CSS,
)
FACTOR_MODEL = genanki.Model(
    FACTOR_MODEL_ID, "Mathematics (factor pairs)",
    fields=[{"name": "Product"}, {"name": "Pairs"}, {"name": "Count"}],
    templates=[{"name": "Factor pairs", "qfmt": FACTOR_Q, "afmt": FACTOR_A}],
    css=CSS,
)


def band(a, b):
    """1: the 2–10 table; 2: ×11, ×12, ×15, ×20; 3: anything with 13, 14, 16, 17, 18 or 19."""
    if a in HARD or b in HARD:
        return 3
    return 2 if max(a, b) > 10 else 1


def facts():
    """Every ordered pair, easiest first: by band, then by the larger factor, then the smaller,
    with a × b right before b × a."""
    return sorted(((a, b) for a in FACTORS for b in FACTORS),
                  key=lambda f: (band(*f), max(f), min(f), f[0] != max(f)))


def pairs(n):
    """The factor pairs of n within 2–20, smaller factor first: 36 -> [(2, 18), (3, 12), (4, 9), (6, 6)]."""
    return [(a, n // a) for a in FACTORS if n % a == 0 and a <= n // a <= HIGH]


def order():
    """The new-card order, as ("product" | "division", (a, b)) and ("factoring", n) items.

    Products go in facts() order; each division comes DIVISION_DELAY products after its product; a
    product's factoring card comes right after the last division card that gives it."""
    fs = facts()
    divisions_left = {}
    for a, b in fs:
        divisions_left[a * b] = divisions_left.get(a * b, 0) + 1
    items = []

    def division(f):
        items.append(("division", f))
        n = f[0] * f[1]
        divisions_left[n] -= 1
        if divisions_left[n] == 0:
            items.append(("factoring", n))

    for i, f in enumerate(fs):
        items.append(("product", f))
        if i >= DIVISION_DELAY:
            division(fs[i - DIVISION_DELAY])
    for f in fs[len(fs) - DIVISION_DELAY:]:
        division(f)
    return items


def note(item, position):
    kind, value = item
    tags = ["mathematics::multiplication", f"kind::{kind}"]
    if kind == "factoring":
        ps = pairs(value)
        count = f"{len(ps)} pair" + ("s" if len(ps) > 1 else "")
        return genanki.Note(
            FACTOR_MODEL, [str(value), "<br>".join(f"{a} × {b}" for a, b in ps), count],
            guid=genanki.guid_for("mathematics", "multiplication", "factoring", value),
            tags=tags, due=position)
    a, b = value
    question, answer = (f"{a} × {b}", a * b) if kind == "product" else (f"{a * b} ÷ {a}", b)
    return genanki.Note(
        TYPED_MODEL, [question, str(answer)],
        guid=genanki.guid_for("mathematics", "multiplication", kind, a, b),
        tags=tags + [f"band::{band(a, b)}"], due=position)


def check(items):
    kinds = [k for k, _ in items]
    counts = {k: kinds.count(k) for k in ("product", "division", "factoring")}
    assert counts == {"product": 361, "division": 361, "factoring": 143}, counts
    seen = set()
    for kind, value in items:
        if kind == "division":
            assert ("product", value) in seen, f"division {value} before its product"
        if kind == "factoring":
            assert all(("division", p) in seen and ("division", p[::-1]) in seen for p in pairs(value)), value
        seen.add((kind, value))


def build():
    items = order()
    check(items)
    deck = genanki.Deck(DECK_ID, DECK)
    for position, item in enumerate(items):
        deck.add_note(note(item, position))
    assert len({n.guid for n in deck.notes}) == len(deck.notes), "duplicate GUIDs"
    return [deck], []
