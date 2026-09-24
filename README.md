# The Unofficial Guide

     Name: Rohith Ambarish
     Corpus: city_guides

---

# Unit 1

## What This Does

<!-- Three or four sentences. Which corpus you picked, and the kinds of
     questions your system answers. Write it for someone who has never seen
     this repo.

     Milestone 5. -->
     This is a retrieval-augmented question-answering system built on a corpus of
     14 UK seaside town guides (`city_guides`). Each guide covers one town across
     a consistent set of sections — getting there, getting around, eating and
     drinking, sightseeing, accommodation, timing a visit, and practical notes.
     The system answers questions like "where should I stay in Pellew Sands?" or
     "how do I get around without a car?" by retrieving the relevant section(s)
     and generating an answer grounded in them, with the source guide named.

## Chunking Strategy

**Chunk size:** 
     Not a fixed size — chunks follow the document's own markdown section headers, so length varies naturally (in practice: 178–549 characters, 317 on average across 88 chunks from 14 documents).

**Overlap:** None.

     The starter's fixed 800-character window barely touched this corpus (docs
     average ~2,068 characters, so it produced only 51 chunks) but where it did
     cut, it sliced straight through the middle of a section — pairing the tail
     of "Eat and drink" with the head of "What to see" in the same chunk.

     When I read the actual documents in Milestone 1, I noticed each guide is
     already organized into clearly labeled, single-topic sections (`## Getting
     there`, `## Where to stay`, etc.), each running roughly 150–500 characters —
     short enough to stay focused, long enough to stand alone. That structure is
     a better chunk boundary than any character count I could have picked, so I
     split on the markdown headers instead: one section becomes one chunk, with
     the document title folded into the first section rather than becoming an
     orphan chunk of its own.

     I didn't add overlap because each section is already self-contained — a
     question about "getting around" doesn't need trailing context from "getting
     there" to be answered, so overlap would only add noise rather than missing
     context.

     I didn't need a fallback for oversized or undersized sections in practice:
     the longest chunk (549 characters) is still one topic, not several, and the
     shortest (178 characters) is a complete section, not a fragment.

<!-- What about YOUR documents made you pick these numbers? Short posts and
     long sectioned guides don't want the same chunking, and "800 seemed
     reasonable" earns nothing. Point at something you noticed when you read
     the documents in Milestone 1.

     If you changed your mind partway through, say so and say why. That's worth
     more than pretending you got it right first time.

     Milestone 3. -->

## Sample Chunks

<!-- Five chunks, pasted as text. Label each one and name the file it came from
     AND the function that produced it — the grader checks your code against
     what you claim here.

     `python app.py chunks -n 5` prints all three for you. Copy them straight
     across.

     Milestone 3. -->
```
======================================================================
Chunk 1  |  source: guide_accessibility.md#0  |  produced by: chunker.py::split_documents
======================================================================
# Getting around the region with limited mobility

An honest assessment rather than a promotional one. Some of these places are
difficult and it is better to know in advance.

## Straightforward

**Thornby Wells** is the easiest town in the region. It is flat, compact, and
everything is within three minutes of everything else. Parking is free for two
hours anywhere in town and the station is central. The pump room and gardens
are level throughout.

**Marchwood** has a modern tram network with level boarding on all four lines,
running every 8 minutes on weekdays. The city museum and covered market are both
step-free. The distances between districts are the main consideration.

**Brightwater** is level along the river and through the centre. The mill museum
is step-free. The station is a 15-minute walk from campus on flat ground, or the
shuttle meets the four busiest arrivals.

======================================================================
Chunk 2  |  source: guide_corry_vale.md#5  |  produced by: chunker.py::split_documents
======================================================================
## When to go

May to September. Outside those months the pub in the third village closes, the farm shop reduces its hours, and several footpaths becomegenuinely boggy rather than merely wet. The road is not gritted above the second village and is impassable in snow.

======================================================================
Chunk 3  |  source: guide_givens_mill.md#2  |  produced by: chunker.py::split_documents
======================================================================
## Eat and drink

A tearoom attached to the mill, open 10 to 4 daily except Tuesdays, which sells bread made from the flour ground twenty metres away and is the reason most people come. One pub, food served lunchtimes and Thursday to Saturday evenings.

======================================================================
Chunk 4  |  source: guide_kestrelford.md#4  |  produced by: chunker.py::split_documents
======================================================================
## Where to stay

Two inns on the square and a handful of rooms above the pubs. Booking ahead matters between May and September and not at all otherwise. There is no accommodation of any kind within four miles of the town in either direction.

======================================================================
Chunk 5  |  source: guide_pellew_sands.md#6  |  produced by: chunker.py::split_documents
======================================================================
## Practical notes

Cash is still useful at the market and in smaller places, though cards are
accepted almost everywhere now. Mobile coverage is good in the centre and
patchy on the outskirts. The nearest full hospital is in Brightwater; there is
a minor injuries unit locally with limited hours.
```

## Sample Answer

<!-- One complete question and answer, pasted as text, with the source line
     visible. Milestone 4. -->

**Question:**
    "What is mill building turned into?" 

**Answer:**
     Based on the provided documents, the mill building in Brightwater is now a museum (source: `guide_brightwater.md`).

     Sources retrieved: guide_brightwater.md, guide_givens_mill.md

**My relevance cutoff:**

<!-- The number you set in config.py, and how you got there.

     You ran five questions your corpus covers and the five in OUT_OF_SCOPE
     that it clearly doesn't, and wrote down the best distance for each. What
     did those two groups look like? Where was the gap? Put the actual numbers
     here — the table below wants all ten rows.

     Milestone 4. -->
     I ran my five in-corpus test questions and the five OUT_OF_SCOPE questions and recorded the best distance for each. The in-corpus questions all landed between 0.370 and 0.586, and the out-of-scope questions all landed between 0.813 and 0.975 — a clean gap with no overlap. I set the cutoff at 0.6 (the starter default), which sits comfortably in that gap: high enough that none of my real questions get refused, low enough that none of the out-of-scope questions get answered.

| Question | In corpus? | Best distance |
|---|---|---|
| What is mill building turned into? | Yes | 0.484 |
| What time of the year is Givens Mill closed? | Yes | 0.370 |
| Where is Marine Terrace located? | Yes | 0.452 |
| When and what time of the day is hard to find a meal? | Yes | 0.474 |
| Which place is cycling not recommended? | Yes | 0.586 |
| What is the capital of Mongolia? | No | 0.827 |
| How do I change the oil in a diesel engine? | No | 0.903 |
| Who won the 1994 World Cup? | No | 0.975 |
| What is the recommended dosage of ibuprofen for a headache? | No | 0.846 |
| How do I write a for loop in Rust? | No | 0.813 |

## How I Used AI

<!-- Two specific moments. For each: what you asked for, what came back, and
     what you changed about it.

     "I asked Claude to write the chunking function from my notes. It ignored
     the overlap, so I added that myself" is the level of detail we're after.
     "I used AI to help me code" is not.

     Milestone 5. -->

**1.**
     **Chunking function.** I shared a sample document (Pellew Sands)
     with Claude and asked for a chunking function to replace the fixed-800-char
     starter. It first suggested a header-plus-paragraph-fallback approach with a
     MIN_CHUNK/MAX_CHUNK size check, but that was more complex than my documents
     actually needed — my guides are short, clean markdown with headers and no
     oversized sections. Once I showed it a real document, it simplified to a pure
     header-split function. I ran it and hit a `TypeError` because `Chunk` needed
     `index` and `produced_by` fields the draft hadn't included — I had to paste
     the actual error back before the function would run at all.


**2.**
     **Setting the relevance cutoff.** I ran my 5 in-corpus and 5
     out-of-scope test questions myself and pasted the raw terminal output (with
     distances) to Claude. Rather than picking a number for me outright, it read
     the two groups (0.370–0.586 vs. 0.813–0.975), pointed out the gap between
     them, and confirmed the starter's default of 0.6 already sat safely inside
     it — so I kept the default instead of guessing at a new number. I also
     initially flagged one question ("Where is Marine Terrace located?") as a
     possible failure because the answer only cited a filename, not the town
     name in prose — Claude helped me see that was a wording issue in my own
     question/expected-answer check, not a retrieval or grounding problem.

<!-- ── Stretch features ─────────────────────────────────────────────────────
     Doing one? Say so here BEFORE you start. A feature this README never
     claims earns nothing.
     ───────────────────────────────────────────────────────────────────────── -->

---

# Unit 2

<!-- These sections get ADDED to what's already above. Don't delete or rewrite
     unit 1 — the point is that someone can see what you said before you knew
     how it went. -->

## Run Log — Before

<!-- Your five criteria, three runs each. `python run_eval.py --label before`
     runs the questions, puts the OUT_OF_SCOPE ones through the gate, and
     writes it all into results/ for you. Targets come from criteria.md; the
     verdict column is your call.

     Criterion 3 is measured in one deterministic pass rather than three, so
     the same number goes in all three run columns. That's correct, not lazy.

     Milestone 1. -->

     | Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
     |---|---|---|---|---|---|
     | 1. Retrieved chunk contains the answer | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
     | 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
     | 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
     | 4. 80% of chunks between 30-150 words | 80% | 100% | 100% | 100% | MET |
     | 5. Answer contains expected phrase | 4 of 5 | 4/5 | 4/5 | 4/5 | MET |

     ## Real Output

### Criterion 1 — Retrieved chunk contains the answer
Produced by `store.py::search` (chunks from `chunker.py::split_documents`)

Question: "What is mill building turned into?"
Best distance: 0.4654
Sources retrieved: guide_accessibility.md, guide_brightwater.md, guide_givens_mill.md

Retrieved chunk (guide_brightwater.md):
"## What to see  The mill building itself is now a museum..."

### Criterion 2 — Every answer names a source
Produced by `generate.py::answer_from_chunks`

Question: "What is mill building turned into?"

"The mill building is now a museum (source: guide_brightwater.md)."

### Criterion 3 — Gate stops out-of-corpus questions
Produced by `run_eval.py::check_out_of_scope` (gate logic in `gate.py`)

Question: "What is the capital of Mongolia?"
Best distance: 0.827 (cutoff 0.6)

"I don't have enough information about that."

### Criterion 4 — Chunk word length
Produced by `check_chunk_lengths.py`, reading the `city_guides__default` collection via `store.py`

Collection: city_guides__default
Total chunks: 84
In range [30, 150] words: 84 (100.0%)
Shortest: 30 words
Longest: 146 words
Average: 60.3 words

### Criterion 5 — Answer contains expected phrase
Produced by `generate.py::answer_from_chunks`

Question: "Where is Marine Terrace located?"
Expected phrase: "Pellew Sands"

"Marine Terrace is located one street back from the seafront.
Source: guide_pellew_sands.md (also mentioned in guide_eating.md)"

This is the one question where the expected phrase never appears — the
model correctly cites the source file but never writes "Pellew Sands" as
a place name in prose, so this run fails the check even though retrieval
and grounding both worked correctly.

<!-- Underneath, paste the REAL output for each criterion from one of your
     runs — the actual text your system produced, not a description of it.
     Name the file and function that produced it. -->

## Verdicts

<!-- MET or MISSED for each of the five, against the target you wrote last
     unit — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 | Retrieved chunks contain the answer (4 of 5) | MET | All three runs scored 5/5 — every question's retrieved chunks contained the literal answer, not just related material, with no exceptions across runs. |
| 2 | Every answer names a source (5 of 5) | MET | All three runs scored 5/5, which is expected since GROUNDING_INSTRUCTION requires a source filename in every prompt, not left to chance. |
| 3 | Gate stops out-of-corpus questions (4 of 5) | MET | Refused 5/5 in a single deterministic pass; the best out-of-scope distance (0.813) sits well clear of the 0.6 cutoff, so it's not a borderline result. |
| 4 | 80% of chunks between 30-150 words | MET | 100% of my 84 stored chunks fell in range (measured via check_chunk_lengths.py), with shortest (30) and longest (146) both comfortably inside the bounds. |
| 5 | Answer contains expected phrase (4 of 5) | MET | All three runs scored exactly 4/5 — the "Marine Terrace" question failed every time because the model names the source as a filename rather than writing "Pellew Sands" in prose; see revision below. |

### Revision — Criterion 5

     **Original:** For at least 4 of my 5 test questions, the generated answer
     contains the expected phrase defined in questions.py.

     **Problem:** My expected phrase for "Where is Marine Terrace located?" was
     "Pellew Sands," but the system is instructed by GROUNDING_INSTRUCTION to
     name sources by filename, so it consistently answers with
     `guide_pellew_sands.md` instead of writing the town name in prose. This
     isn't the model failing to find the answer — it's my expected-phrase check
     not accounting for the system's own citation format.

     **Revised:** For at least 4 of 5 test questions, the generated answer
     contains the expected phrase, accepting the source filename as a valid
     match when the expected phrase is a place name that also appears in a
     guide's filename (e.g. "Pellew Sands" or "pellew_sands" both count).

     **Result under revision:** 5/5 in all three runs.


## Diagnoses

<!-- For each miss: which stage caused it, and how. The stage alone isn't
     enough — you need the mechanism.

     Not a diagnosis: "Question 3 didn't work."
     A diagnosis:     "Question 3 asks about laundry costs. The answer is in
                       one sentence that got split across two chunks, so
                       neither chunk on its own contains it."

     The five stages: loading → chunking → embedding → retrieval → generation.

     Look for a pattern. If three misses all ask about numbers, that's one
     problem, not three.

     Missed nothing? Say so, then say honestly whether your targets were set
     low, and which one you'd tighten and to what.

     Milestone 3. -->

     I didn't miss any criterion — all five came out MET across all three runs
     (see Milestone 2 verdicts table). So there's no pipeline failure to trace
     through loading, chunking, embedding, retrieval, or generation.

     **Honest check on whether my targets were too easy:**

     Criteria 2, 3, and 4 were met with wide margin (100% or 5/5 against targets
     of 5/5, 4/5, and 80%), and each is either enforced by design (the grounding
     instruction requires a source in every prompt) or backed by a clean, wide
     numerical gap (out-of-scope distances 0.813-0.975 vs. a 0.6 cutoff; chunk
     lengths 30-146 words comfortably inside a 30-150 range). I don't think these
     three were set low — they're just genuinely well-suited to a small, clean,
     well-structured corpus like mine.

     Criterion 5 is the one I'd tighten. My original expected-phrase check turned
     out to be too forgiving of my own test design: the "Marine Terrace" question
     passed on a technicality (the source filename `guide_pellew_sands.md`
     contains "pellew_sands", which I allowed as a match after the fact) rather
     than the model demonstrating it actually surfaced the town name as a fact,
     not just a citation. A tighter version of this criterion would require the
     expected phrase to appear in the answer's prose sentence, separate from the
     source citation line — that would test whether the model synthesizes the
     answer, not just whether it names the right file. I suspect that stricter
     version would still pass, since the underlying retrieval and grounding are
     solid, but I haven't actually tested it that way, so I can't claim it as MET
     under the tighter definition.

## The Improvement

     **What I changed:** Added one line to `GROUNDING_INSTRUCTION` in
     `generate.py`, instructing the model to name the place or topic in plain
     language in the answer text, not just cite the source filename.

     **Why I picked it:** My Milestone 3 diagnosis found that criterion 5 passed
     "Where is Marine Terrace located?" only after I loosened my expected-phrase
     check to accept the source filename (`guide_pellew_sands.md`) as a match for
     "Pellew Sands" — the model itself never wrote the town name in prose, which
     meant the underlying gap (generation not surfacing the answer in readable
     form) was still there even though the loosened test passed.

     ### Run Log — After

     | Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
     |---|---|---|---|---|---|
     | 1. Retrieved chunk contains the answer | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
     | 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
     | 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
     | 4. 80% of chunks between 30-150 words | 80% | 100% | 100% | 100% | MET |
     | 5. Answer contains expected phrase | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |

     **Did it help?** Yes. Criterion 5 moved from a consistent 4/5 (all three
     before-runs) to a consistent 5/5 (all three after-runs), with criteria 1-4
     completely unchanged — expected, since the fix only touched the grounding
     prompt, not chunking, retrieval, or the relevance gate. All five best
     distances (0.465, 0.370, 0.442, 0.474, 0.586) are identical before and after,
     confirming retrieval itself never moved; only generation did.

     Importantly, this isn't just the scorer being more lenient. The actual
     answer text for "Where is Marine Terrace located?" changed from citing only
     `guide_pellew_sands.md` to explicitly stating "...located one street back
     from the seafront in Pellew Sands." That passes even the original, stricter
     phrase-match definition (looking for the literal text "Pellew Sands"), not
     just the loosened filename-matching version I'd built into scorer.py as a
     workaround. So the fix addressed the real gap identified in Milestone 3 —
     the model synthesizing the answer into readable prose — rather than the
     improvement being an artifact of a more forgiving test.

## What's Still Broken

<!-- For each criterion still missed after your fix: what you'd do about it,
     and why you stopped where you did.

     "I ran out of time" is fine if it's true. Pretending nothing is left is
     not.

     Milestone 5. -->

## What I'd Do Differently

<!-- Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. -->
