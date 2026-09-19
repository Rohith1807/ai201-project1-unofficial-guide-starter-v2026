# Acceptance criteria — The Unofficial Guide

Five criteria that say what "working" means for this system, written in unit 1
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"Retrieval works"* is an opinion. *"For at
least 4 of my 5 test questions, the top results include a chunk containing the
answer"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter or looser one. A reason that says something about your corpus or your
pipeline earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## 1. Retrieved chunks contain the answer

For at least 4 of my 5 test questions, the retrieved chunks include one that
contains the answer.

**Why this target:** My city_guides documents are short and section-based
(150-500 characters per section), so most single-fact questions map cleanly
onto one section. I expect 4 of 5 to be easy. The one I'd flag as harder is
anything that spans two sections (e.g. comparing "getting around" and "where
to stay" for the same town) — a single-chunk retrieval might miss half of
that answer, which is why I'm not claiming 5 of 5.

---

## 2. Every answer names a source

Every answer the system produces names at least one source document.

**Why this target:** This one is achievable at 100% because it's enforced in
the code, not left to chance. The `GROUNDING_INSTRUCTION` system prompt
explicitly requires the model to name the source filename in every answer,
and every retrieved chunk is already tagged with its source before it reaches
the prompt. The only way this fails is if the model ignores an explicit
instruction it's given every single time, which is a much narrower failure
mode than "did retrieval happen to find the right chunk."

---

## 3. The relevance gate stops out-of-corpus questions

When I ask a question my documents clearly don't cover, the relevance gate
stops it and the system returns "I don't have enough information about that" —
in at least 4 of 5 tries.

**Why this target:** When I ran my 5 in-corpus and 5 out-of-scope questions in
Milestone 4, the best distances split into two clean, non-overlapping groups:
0.370-0.586 for in-corpus questions and 0.813-0.975 for out-of-scope ones. With
a gap that wide (roughly 0.23 between the closest pair), a cutoff of 0.6 sitting
in the middle should catch all 5 out-of-scope questions reliably, not just 4 —
but I'm keeping the target at 4/5 rather than 5/5 in case a future off-topic
question happens to share more vocabulary with my corpus than these five did.

---

## 4. Something about your chunks

At least 80% of retrieved chunks are between 100 and 300 words long.

**Why this target:**

I chose 100 to 300 words because shorter chunks may not provide enough context, while longer chunks may include unnecessary information. The 80% threshold allows for some variation in document structure.

---

## 5. Your choice

For at least 4 of my 5 test questions, the generated answer contains the expected phrase defined in questions.py.

**Why this target:** I chose 4 out of 5 because retrieval systems are not
perfect, but the system should successfully answer most questions and include
the key information expected from the source documents. The one place I'd
expect this to slip is phrasing mismatches rather than retrieval failures —
for example, my own "Marine Terrace" question expected the literal string
"Pellew Sands" in the answer, but the model correctly cited the source as
`guide_pellew_sands.md` instead of writing the town name in prose. That's a
wording gap in my expected-phrase check, not a grounding or retrieval failure,
which is exactly the kind of near-miss I'd want this criterion to surface.

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 2 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 1. Retrieved chunks contain the answer

         For at least 4 of my 5 test questions, the retrieved chunks include
         one that contains the answer.

         **Why this target:** ...

         > **Revised in unit 2:** For at least 4 of 5 questions, the top three
         > results contain the answer.
         >
         > **Why revised:** I couldn't judge "the chunks include one that
         > contains the answer" the same way twice — I scored two questions
         > differently on Monday than on Wednesday. The new version is
         > something I can actually check.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said 4 of 5 but got 2 of 5, so 2 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.

     The whole reason the originals stay visible is so someone can see what you
     said before you knew the answer.
     ───────────────────────────────────────────────────────────────────────── -->
