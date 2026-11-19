# Decisions

Dated entries: the question, the choice, and why. Check here before re-asking.

## 2026-11-19 (from the backlog brief)

- **Repo and visibility?** `prsnlanki/mathematics`, public, each version published as a GitHub Release. Same as the other prsnlanki decks.
- **Deck name in Anki?** `Mathematics::Multiplication`, in English. The user's choice.
- **Range?** 2–20 × 2–20. The user wants instant recall past the classic 12×12 table.
- **7×8 and 8×7 as separate cards?** Yes, both orders (361 product cards), so neither order takes longer to recall.
- **Directions besides a × b → product?** Also the missing factor and factoring a product.
- **Missing-factor format?** Written as division: 56 ÷ 7 = ? → 8. One card per ordered pair (361).
- **Factoring cards?** Product → all its factor pairs within 2–20, self-graded (143 cards), because typed answers would fail on order and spacing.
- **How to answer product and division cards?** Typed, with a timer, so Anki marks right or wrong.
- **Timer behaviour?** Just shows elapsed seconds: no limit, no colours.
- **New-card order?** Easiest first: the 2–10 table, then ×11/×12/×15/×20, then the hard 13–19 facts; a fact's division card a few days after its product card.
- **Allowed under Anthropic's Usage Policy (effective 2026-11-12)?** Yes: educational content, no restricted use. Checked 2026-11-19.

## 2026-11-19 (first build)

- **Difficulty within a band?** By the larger factor, then the smaller, with a × b right before b × a: small facts first, and a fact's two orders together. Decided by Claude, pending review.
- **How long after its product does a division card come?** 30 products later (`DIVISION_DELAY`), set through each note's new-card position: about 3 days at 20 new cards a day. Positions instead of sibling burying, because product and division are separate notes. Decided by Claude, pending review.
- **Where do factoring cards go?** Right after the last division card of that product, when every pair has been seen. Decided by Claude, pending review.
- **Cue on factoring cards?** The front says how many pairs there are ("4 pairs"), so the card is tractable and you know when you're done (FLASHCARD_GUIDE rule 7: a set needs its size). Decided by Claude, pending review.
- **Timer on the back?** Shows the time the card took, to a tenth of a second; the front counts whole seconds. Decided by Claude, pending review.
- **Note types?** Two custom ones, "Mathematics (typed, timed)" (Question, Answer) for products and divisions, and "Mathematics (factor pairs)" (Product, Pairs, Count), each with one template so Anki's default "card type, then order gathered" sort keeps the built order. Decided by Claude.
