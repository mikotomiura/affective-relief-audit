"""Checks of the lexicon baseline (atact.lexicon) on a small artificial lexicon (the real lexicon is not in the repo)."""

from __future__ import annotations

from pathlib import Path

import pytest

from atact.lexicon import Lexicon, load_lexicon, match_terms, sentence_point, split_sentences, text_path, tokenize

REAL = Path(__file__).resolve().parents[1] / "external" / "nrc-vad-v2.1-20261026" / "NRC-VAD-Lexicon-v2.1" / \
    "NRC-VAD-Lexicon-v2.1.txt"


@pytest.fixture
def lex(tmp_path) -> Lexicon:
    p = tmp_path / "lex.txt"
    p.write_text("term\tvalence\tarousal\tdominance\n"
                 "calm\t0.8\t-0.9\t0.1\n"
                 "storm\t-0.6\t0.9\t0.2\n"
                 "sea\t0.3\t0.1\t0.0\n"
                 "calm sea\t0.9\t-1.0\t0.3\n"
                 "don't\t-0.2\t0.0\t0.0\n"
                 "well-being\t0.9\t-0.1\t0.4\n"
                 "sea/storm\t0.0\t0.0\t0.0\n")
    return load_lexicon(p)


def test_tokenize_keeps_apostrophes_and_hyphens():
    assert tokenize("Don’t lose your Well-being!") == ["don't", "lose", "your", "well-being"]


def test_longest_multiword_first(lex):
    assert match_terms(tokenize("A calm sea, then a storm at sea."), lex) == ["calm sea", "storm", "sea"]
    assert lex.max_len == 2
    assert lex.skipped == ("sea/storm",)


def test_mean_without_clip(lex):
    p = sentence_point("Calm, calm storm.", lex)
    assert p.Z == 3
    assert p.V == pytest.approx((0.8 + 0.8 - 0.6) / 3)
    assert p.A == pytest.approx((-0.9 - 0.9 + 0.9) / 3)
    # the mean of the extreme entries stays inside the square, so nothing would be clipped
    q = sentence_point("calm sea calm sea", lex)
    assert (q.V, q.A) == pytest.approx((0.9, -1.0))


def test_no_match_gives_neutral_point_and_flag(lex):
    p = sentence_point("Nothing here matches.", lex)
    assert (p.V, p.A, p.Z, p.unmatched) == (0.0, 0.0, 0, True)


def test_text_path_one_point_per_sentence(lex):
    pts = text_path("A calm sea. A storm! Nothing?", lex)
    assert [p.Z for p in pts] == [1, 1, 0]
    assert split_sentences("One. Two!  Three?") == ["One.", "Two!", "Three?"]


def test_scores_outside_the_square_are_refused(tmp_path):
    p = tmp_path / "bad.txt"
    p.write_text("term\tvalence\tarousal\tdominance\nx\t1.5\t0\t0\n")
    with pytest.raises(ValueError):
        load_lexicon(p)


@pytest.mark.skipif(not REAL.exists(), reason="the NRC VAD lexicon is not redistributed with the repository")
def test_real_lexicon_loads():
    lx = load_lexicon(REAL)
    assert len(lx.entries) > 50000
    assert lx.max_len >= 2
    assert lx.skipped == ("soda/pop",)
    assert all(-1 <= v <= 1 and -1 <= a <= 1 for v, a in lx.entries.values())
