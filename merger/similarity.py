from .score_vars import (
    WORD_MISMATCH_PENALTY,
    NO_MATCH_PENALTY,
    EXTRA_WORD_PENALTY,
    MAX_CONFIDENCE,
    SINGLE_SOURCE_CONFIDENCE
)


def similarity(a: str | None, b: str | None):
    if not a and not b:
        return None

    if not a or not b:
        return SINGLE_SOURCE_CONFIDENCE

    
    a = a.lower().strip()
    b = b.lower().strip()

    if a == b:
        return 1.0

    
    a_words = a.split()
    b_words = set(b.split())

    confidence_loss = 0.0

    if len(a_words) != len(b_words):
        confidence_loss += WORD_MISMATCH_PENALTY

    unmatched_words = 0

    for word in a_words:
        if word in b_words:
            b_words.remove(word)
        else:
            unmatched_words += 1

   
    if unmatched_words == len(a_words):
        confidence_loss += NO_MATCH_PENALTY
    elif unmatched_words > 0:
        confidence_loss += unmatched_words * EXTRA_WORD_PENALTY

   
    return max(
        0.0,
        round(MAX_CONFIDENCE - confidence_loss, 2)
    )