"""Lexicon baseline from a sentence to a point (V, A) (Section 2.2 of Harada (2026), rewritten).

For each sentence, the matched terms of a valence-arousal lexicon whose scores already lie in [-1, 1] (NRC VAD Lexicon
v2.1, Mohammad 2025, default form) are averaged component by component:

    V = (1/Z) sum_i V_i,  A = (1/Z) sum_i A_i,

where Z is the number of matched terms. The mean of values in [-1, 1] lies in [-1, 1], so no clipping is applied (the
clip of the preprint has no effect). If no term is matched (Z = 0) the sentence is given the neutral point (0, 0) and
is flagged as unmatched; such sentences are reported, not hidden.

Matching: the sentence is lower-cased, the typographic apostrophe is replaced by "'", and tokens are maximal runs of
letters, possibly joined by internal apostrophes or hyphens. Multiword entries of the lexicon are matched greedily
from the left, longest first (up to the longest entry); a token covered by a matched multiword entry is not matched
again on its own. Lexicon terms that the tokenizer cannot produce as written (in v2.1 only 'soda/pop') are
skipped and listed. No lemmatisation, no handling of negation, irony or context: the baseline is a transparent
average, not a sentence-level emotion detector.

The lexicon file is not part of this repository (its terms of use do not allow redistribution); its path and SHA-256
are recorded by each computation that uses it.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field
from pathlib import Path

TOKEN = re.compile(r"[a-z]+(?:['\-][a-z]+)*")
SENTENCE_END = re.compile(r"(?<=[.!?])\s+")


@dataclass(frozen=True)
class Lexicon:
    entries: dict[str, tuple[float, float]]
    max_len: int
    sha256: str = ""
    skipped: tuple[str, ...] = ()


@dataclass
class SentencePoint:
    text: str
    V: float
    A: float
    Z: int
    matched: list[str] = field(default_factory=list)

    @property
    def unmatched(self) -> bool:
        return self.Z == 0


def load_lexicon(path: Path) -> Lexicon:
    """Read the tab-separated default form (term, valence, arousal, dominance) with a header line."""
    raw = Path(path).read_bytes()
    entries: dict[str, tuple[float, float]] = {}
    skipped: list[str] = []
    lines = raw.decode("utf-8").splitlines()
    if lines[0].split("\t")[:3] != ["term", "valence", "arousal"]:
        raise ValueError(f"unexpected header in {path}: {lines[0]!r}")
    for ln in lines[1:]:
        if not ln.strip():
            continue
        term, v, a, *_ = ln.split("\t")
        v, a = float(v), float(a)
        if not (-1.0 <= v <= 1.0 and -1.0 <= a <= 1.0):
            raise ValueError(f"score outside [-1, 1] for {term!r}")
        key = " ".join(tokenize(term))
        if key != term.lower().replace("\u2019", "'"):
            # a term that the tokenizer cannot produce as written (e.g. 'soda/pop') can never match; it is skipped
            # and listed, so that it does not overwrite a plain entry with the same tokens
            skipped.append(term)
            continue
        if key in entries:
            raise ValueError(f"duplicate term {key!r}")
        entries[key] = (v, a)
    return Lexicon(entries, max(len(k.split(" ")) for k in entries), hashlib.sha256(raw).hexdigest(),
                   tuple(skipped))


def tokenize(text: str) -> list[str]:
    return TOKEN.findall(text.lower().replace("’", "'"))


def split_sentences(text: str) -> list[str]:
    return [s.strip() for s in SENTENCE_END.split(text.strip()) if s.strip()]


def match_terms(tokens: list[str], lex: Lexicon) -> list[str]:
    out, i = [], 0
    while i < len(tokens):
        for n in range(min(lex.max_len, len(tokens) - i), 0, -1):
            cand = " ".join(tokens[i : i + n])
            if cand in lex.entries:
                out.append(cand)
                i += n
                break
        else:
            i += 1
    return out


def sentence_point(text: str, lex: Lexicon) -> SentencePoint:
    terms = match_terms(tokenize(text), lex)
    if not terms:
        return SentencePoint(text, 0.0, 0.0, 0, [])
    z = len(terms)
    V = sum(lex.entries[t][0] for t in terms) / z
    A = sum(lex.entries[t][1] for t in terms) / z
    return SentencePoint(text, V, A, z, terms)


def text_path(text: str, lex: Lexicon) -> list[SentencePoint]:
    """The path of a text: one point per sentence, in order."""
    return [sentence_point(s, lex) for s in split_sentences(text)]
