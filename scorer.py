"""
scorer.py

Automated pass/fail judgment for run_eval.py, per the contract:

    judge(question, expects, answer, results) -> bool

`results` is the list of retrieved Result objects (see store.py) for this
question -- used here to also sanity-check that the expected phrase was
actually retrievable, not just present in the final answer by coincidence.

This implements a single criterion: does the generated answer contain the
expected phrase? Matching is case-insensitive and also accepts the phrase
in "underscored filename" form (e.g. "Pellew Sands" matches "pellew_sands"
in a cited filename), since this system's grounding instruction has the
model cite sources by filename rather than always spelling out the subject
in prose -- see the README's Milestone 2 revision for why that's a deliberate
choice, not a loophole.
"""

import re


def _normalize(text: str) -> str:
    """Lowercase and collapse whitespace/underscores for loose comparison."""
    text = text.lower()
    text = text.replace("_", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def judge(question: str, expects: str, answer: str, results) -> bool:
    """
    Return True if `answer` satisfies the expected phrase for `question`.

    Primary check: expects, normalized, appears as a substring of answer,
    normalized. This catches "Pellew Sands" appearing as prose, and also
    "guide_pellew_sands.md" appearing as a citation, without needing two
    separate code paths.
    """
    norm_answer = _normalize(answer)
    norm_expects = _normalize(expects)

    if norm_expects in norm_answer:
        return True

    return False