from indifferent.indifferent import _backfill


# Nothing to backfill
def test_empty():
    assert (
        _backfill(
            base_split=[],
            revision_split=[],
            base_last_match=None,
            base_index=0,
            revision_last_match=None,
            revision_index=0,
        )
        == []
    )


# Nothing in the base to backfill, first match
def test_no_base_backfill(a, space, cat):
    assert _backfill(
        base_split=[cat],
        revision_split=[a, space, cat],
        base_last_match=None,
        base_index=0,
        revision_last_match=None,
        revision_index=2,
    ) == [
        {
            "base": None,
            "content": True,
            "revision": 0,
            "value": "a",
        },
        {
            "base": None,
            "content": False,
            "revision": 1,
            "value": " ",
        },
    ]


# Nothing in the revision to backfill, first match
def test_no_revision_backfill(a, space, cat):
    assert _backfill(
        base_split=[a, space, cat],
        revision_split=[cat],
        base_last_match=None,
        base_index=2,
        revision_last_match=None,
        revision_index=0,
    ) == [
        {
            "base": 0,
            "content": True,
            "revision": None,
            "value": "a",
        },
        {
            "base": 1,
            "content": False,
            "revision": None,
            "value": " ",
        },
    ]


# Separator at the start, no revision backfill, first match
def test_start_separator_match_backfill_base(a, space, cat):
    assert _backfill(
        base_split=[space, a, space, cat],
        revision_split=[space, cat],
        base_last_match=None,
        base_index=3,
        revision_last_match=None,
        revision_index=1,
    ) == [
        {
            "base": 0,
            "content": False,
            "revision": 0,
            "value": " ",
        },
        {
            "base": 1,
            "content": True,
            "revision": None,
            "value": "a",
        },
        {
            "base": 2,
            "content": False,
            "revision": None,
            "value": " ",
        },
    ]


# Separator at the start, no base backfill, first match
def test_start_separator_match_backfill_revision(a, space, cat):
    assert _backfill(
        base_split=[space, cat],
        revision_split=[space, a, space, cat],
        base_last_match=None,
        base_index=1,
        revision_last_match=None,
        revision_index=3,
    ) == [
        {
            "base": 0,
            "content": False,
            "revision": 0,
            "value": " ",
        },
        {
            "base": None,
            "content": True,
            "revision": 1,
            "value": "a",
        },
        {
            "base": None,
            "content": False,
            "revision": 2,
            "value": " ",
        },
    ]


# Separator at the start, both backfill, first match
def test_start_separator_match_backfill_both(a, space, tab, tabby, cat):
    assert _backfill(
        base_split=[space, a, space, cat],
        revision_split=[space, tabby, tab, cat],
        base_last_match=None,
        base_index=3,
        revision_last_match=None,
        revision_index=3,
    ) == [
        {
            "base": 0,
            "content": False,
            "revision": 0,
            "value": " ",
        },
        {
            "base": 1,
            "content": True,
            "revision": None,
            "value": "a",
        },
        {
            "base": 2,
            "content": False,
            "revision": None,
            "value": " ",
        },
        {
            "base": None,
            "content": True,
            "revision": 1,
            "value": "tabby",
        },
        {
            "base": None,
            "content": False,
            "revision": 2,
            "value": "\t",
        },
    ]


# Separator at start and end, backfill base, first match
def test_start_end_separator_match_backfill_base(a, space, cat, tab):
    assert _backfill(
        base_split=[space, a, space, tab, cat],
        revision_split=[space, tab, cat],
        base_last_match=None,
        base_index=4,
        revision_last_match=None,
        revision_index=2,
    ) == [
        {
            "base": 0,
            "content": False,
            "revision": 0,
            "value": " ",
        },
        {
            "base": 1,
            "content": True,
            "revision": None,
            "value": "a",
        },
        {
            "base": 2,
            "content": False,
            "revision": None,
            "value": " ",
        },
        {
            "base": 3,
            "content": False,
            "revision": 1,
            "value": "\t",
        },
    ]


# Separator at start and end, backfill revision, first match
def test_start_end_separator_match_backfill_revision(a, space, cat, tab):
    assert _backfill(
        base_split=[space, tab, cat],
        revision_split=[space, a, space, tab, cat],
        base_last_match=None,
        base_index=2,
        revision_last_match=None,
        revision_index=4,
    ) == [
        {
            "base": 0,
            "content": False,
            "revision": 0,
            "value": " ",
        },
        {
            "base": None,
            "content": True,
            "revision": 1,
            "value": "a",
        },
        {
            "base": None,
            "content": False,
            "revision": 2,
            "value": " ",
        },
        {
            "base": 1,
            "content": False,
            "revision": 3,
            "value": "\t",
        },
    ]


# Separator at start and end, backfill both, first match
def test_start_end_separator_match_backfill_both(a, space, tab, tabby, cat):
    assert _backfill(
        base_split=[space, a, tab, cat],
        revision_split=[space, tabby, tab, cat],
        base_last_match=None,
        base_index=3,
        revision_last_match=None,
        revision_index=3,
    ) == [
        {
            "base": 0,
            "content": False,
            "revision": 0,
            "value": " ",
        },
        {
            "base": 1,
            "content": True,
            "revision": None,
            "value": "a",
        },
        {
            "base": None,
            "content": True,
            "revision": 1,
            "value": "tabby",
        },
        {
            "base": 2,
            "content": False,
            "revision": 2,
            "value": "\t",
        },
    ]


# Multiple separators at start, backfill base, first match
def test_start_multiple_separator_match_backfill_base(a, space, tab, cat):
    assert _backfill(
        base_split=[space, tab, a, space, cat],
        revision_split=[space, tab, cat],
        base_last_match=None,
        base_index=4,
        revision_last_match=None,
        revision_index=2,
    ) == [
        {
            "base": 0,
            "content": False,
            "revision": 0,
            "value": " ",
        },
        {
            "base": 1,
            "content": False,
            "revision": 1,
            "value": "\t",
        },
        {
            "base": 2,
            "content": True,
            "revision": None,
            "value": "a",
        },
        {
            "base": 3,
            "content": False,
            "revision": None,
            "value": " ",
        },
    ]


# Multiple separators at start, backfill revision, first match
def test_start_multiple_separator_match_backfill_revision(a, tab, space, cat):
    assert _backfill(
        base_split=[space, tab, cat],
        revision_split=[space, tab, a, space, cat],
        base_last_match=None,
        base_index=2,
        revision_last_match=None,
        revision_index=4,
    ) == [
        {
            "base": 0,
            "content": False,
            "revision": 0,
            "value": " ",
        },
        {
            "base": 1,
            "content": False,
            "revision": 1,
            "value": "\t",
        },
        {
            "base": None,
            "content": True,
            "revision": 2,
            "value": "a",
        },
        {
            "base": None,
            "content": False,
            "revision": 3,
            "value": " ",
        },
    ]


# Multiple separators at start, backfill both, first match
def test_start_multiple_separator_match_backfill_both(a, space, tab, tabby, cat):
    assert _backfill(
        base_split=[space, tab, a, space, cat],
        revision_split=[space, tab, tabby, tab, cat],
        base_last_match=None,
        base_index=4,
        revision_last_match=None,
        revision_index=4,
    ) == [
        {
            "base": 0,
            "content": False,
            "revision": 0,
            "value": " ",
        },
        {
            "base": 1,
            "content": False,
            "revision": 1,
            "value": "\t",
        },
        {
            "base": 2,
            "content": True,
            "revision": None,
            "value": "a",
        },
        {
            "base": 3,
            "content": False,
            "revision": None,
            "value": " ",
        },
        {
            "base": None,
            "content": True,
            "revision": 2,
            "value": "tabby",
        },
        {
            "base": None,
            "content": False,
            "revision": 3,
            "value": "\t",
        },
    ]


# Multiple separators at end, backfill base, first match
def test_start_end_multiple_separator_match_backfill_base(a, space, cat, tab):
    assert _backfill(
        base_split=[a, space, tab, cat],
        revision_split=[space, tab, cat],
        base_last_match=None,
        base_index=3,
        revision_last_match=None,
        revision_index=2,
    ) == [
        {
            "base": 0,
            "content": True,
            "revision": None,
            "value": "a",
        },
        {
            "base": 1,
            "content": False,
            "revision": 0,
            "value": " ",
        },
        {
            "base": 2,
            "content": False,
            "revision": 1,
            "value": "\t",
        },
    ]


# Multiple separators at end, backfill revision, first match
def test_start_end_multiple_separator_match_backfill_revision(a, space, cat, tab):
    assert _backfill(
        base_split=[space, tab, cat],
        revision_split=[a, space, tab, cat],
        base_last_match=None,
        base_index=2,
        revision_last_match=None,
        revision_index=3,
    ) == [
        {
            "base": None,
            "content": True,
            "revision": 0,
            "value": "a",
        },
        {
            "base": 0,
            "content": False,
            "revision": 1,
            "value": " ",
        },
        {
            "base": 1,
            "content": False,
            "revision": 2,
            "value": "\t",
        },
    ]


# Multiple separators at end, backfill both, first match
def test_start_end_multiple_separator_match_backfill_both(a, space, tab, tabby, cat):
    assert _backfill(
        base_split=[tab, a, tab, space, cat],
        revision_split=[space, tabby, tab, space, cat],
        base_last_match=None,
        base_index=4,
        revision_last_match=None,
        revision_index=4,
    ) == [
        {
            "base": 0,
            "content": False,
            "revision": None,
            "value": "\t",
        },
        {
            "base": 1,
            "content": True,
            "revision": None,
            "value": "a",
        },
        {
            "base": None,
            "content": False,
            "revision": 0,
            "value": " ",
        },
        {
            "base": None,
            "content": True,
            "revision": 1,
            "value": "tabby",
        },
        {
            "base": 2,
            "content": False,
            "revision": 2,
            "value": "\t",
        },
        {
            "base": 3,
            "content": False,
            "revision": 3,
            "value": " ",
        },
    ]


# Multiple separators at beginning and end, backfill base, first match
def test_start_multiple_end_multiple_separator_match_backfill_base(a, space, cat, tab):
    assert _backfill(
        base_split=[tab, space, a, space, tab, cat],
        revision_split=[tab, space, space, tab, cat],
        base_last_match=None,
        base_index=5,
        revision_last_match=None,
        revision_index=4,
    ) == [
        {
            "base": 0,
            "content": False,
            "revision": 0,
            "value": "\t",
        },
        {
            "base": 1,
            "content": False,
            "revision": 1,
            "value": " ",
        },
        {
            "base": 2,
            "content": True,
            "revision": None,
            "value": "a",
        },
        {
            "base": 3,
            "content": False,
            "revision": 2,
            "value": " ",
        },
        {
            "base": 4,
            "content": False,
            "revision": 3,
            "value": "\t",
        },
    ]


# Multiple separators at start and end, backfill revision, first match
def test_start_multiple_end_multiple_separator_match_backfill_revision(
    a, space, cat, tab
):
    assert _backfill(
        base_split=[tab, space, space, tab, cat],
        revision_split=[tab, space, a, space, tab, cat],
        base_last_match=None,
        base_index=4,
        revision_last_match=None,
        revision_index=5,
    ) == [
        {
            "base": 0,
            "content": False,
            "revision": 0,
            "value": "\t",
        },
        {
            "base": 1,
            "content": False,
            "revision": 1,
            "value": " ",
        },
        {
            "base": None,
            "content": True,
            "revision": 2,
            "value": "a",
        },
        {
            "base": 2,
            "content": False,
            "revision": 3,
            "value": " ",
        },
        {
            "base": 3,
            "content": False,
            "revision": 4,
            "value": "\t",
        },
    ]


# Multiple separators at end, backfill both, first match
def test_start_multiple_end_multiple_separator_match_backfill_both(
    a, space, tab, tabby, cat
):
    assert _backfill(
        base_split=[space, tab, a, tab, space, cat],
        revision_split=[space, tab, tabby, tab, space, cat],
        base_last_match=None,
        base_index=5,
        revision_last_match=None,
        revision_index=5,
    ) == [
        {
            "base": 0,
            "content": False,
            "revision": 0,
            "value": " ",
        },
        {
            "base": 1,
            "content": False,
            "revision": 1,
            "value": "\t",
        },
        {
            "base": 2,
            "content": True,
            "revision": None,
            "value": "a",
        },
        {
            "base": None,
            "content": True,
            "revision": 2,
            "value": "tabby",
        },
        {
            "base": 3,
            "content": False,
            "revision": 3,
            "value": "\t",
        },
        {
            "base": 4,
            "content": False,
            "revision": 4,
            "value": " ",
        },
    ]


# Multiple separators at end, backfill both, last match at 0
def test_start_multiple_end_multiple_separator_match_backfill_both_last_match_0(
    a, space, tab, tabby, cat
):
    assert _backfill(
        base_split=[cat, space, tab, a, tab, space, cat],
        revision_split=[cat, space, tab, tabby, tab, space, cat],
        base_last_match=0,
        base_index=6,
        revision_last_match=0,
        revision_index=6,
    ) == [
        {
            "base": 1,
            "content": False,
            "revision": 1,
            "value": " ",
        },
        {
            "base": 2,
            "content": False,
            "revision": 2,
            "value": "\t",
        },
        {
            "base": 3,
            "content": True,
            "revision": None,
            "value": "a",
        },
        {
            "base": None,
            "content": True,
            "revision": 3,
            "value": "tabby",
        },
        {
            "base": 4,
            "content": False,
            "revision": 4,
            "value": "\t",
        },
        {
            "base": 5,
            "content": False,
            "revision": 5,
            "value": " ",
        },
    ]


# Single separator at start, backfill base, last match at 1
def test_start_single_backfill_base_last_base_match_2_last_revision_match_0(
    a, space, tabby, cat
):
    assert _backfill(
        base_split=[a, space, a, space, tabby, space, cat],
        revision_split=[a, space, cat],
        base_last_match=2,
        base_index=6,
        revision_last_match=0,
        revision_index=2,
    ) == [
        {"base": 3, "content": False, "revision": 1, "value": " "},
        {"base": 4, "content": True, "revision": None, "value": "tabby"},
        {"base": 5, "content": False, "revision": None, "value": " "},
    ]


# Single separator at start, backfill revision, last match at 1
def test_start_single_backfill_revision_last_base_match_0_last_revision_match_2(
    a, space, tabby, cat
):
    assert _backfill(
        base_split=[a, space, cat],
        revision_split=[a, space, a, space, tabby, space, cat],
        base_last_match=0,
        base_index=2,
        revision_last_match=2,
        revision_index=6,
    ) == [
        {"base": 1, "content": False, "revision": 3, "value": " "},
        {"base": None, "content": True, "revision": 4, "value": "tabby"},
        {"base": None, "content": False, "revision": 5, "value": " "},
    ]


# Multiple separators at end, backfill both, last match at 1
def test_start_multiple_end_multiple_separator_match_backfill_both_last_match_1(
    a, space, tab, tabby, cat
):
    assert _backfill(
        base_split=[a, cat, space, tab, a, tab, space, cat],
        revision_split=[a, cat, space, tab, tabby, tab, space, cat],
        base_last_match=1,
        base_index=7,
        revision_last_match=1,
        revision_index=7,
    ) == [
        {
            "base": 2,
            "content": False,
            "revision": 2,
            "value": " ",
        },
        {
            "base": 3,
            "content": False,
            "revision": 3,
            "value": "\t",
        },
        {
            "base": 4,
            "content": True,
            "revision": None,
            "value": "a",
        },
        {
            "base": None,
            "content": True,
            "revision": 4,
            "value": "tabby",
        },
        {
            "base": 5,
            "content": False,
            "revision": 5,
            "value": "\t",
        },
        {
            "base": 6,
            "content": False,
            "revision": 6,
            "value": " ",
        },
    ]


# Multiple separators at end, backfill both, last match at 1, trailing words
def test_start_multiple_end_multiple_separator_match_backfill_both_last_match_1_trailing_words(
    a, space, tab, tabby, cat
):
    assert _backfill(
        base_split=[a, cat, space, tab, a, tab, space, cat, tab, tabby],
        revision_split=[a, cat, space, tab, tabby, tab, space, cat, space, cat],
        base_last_match=1,
        base_index=7,
        revision_last_match=1,
        revision_index=7,
    ) == [
        {
            "base": 2,
            "content": False,
            "revision": 2,
            "value": " ",
        },
        {
            "base": 3,
            "content": False,
            "revision": 3,
            "value": "\t",
        },
        {
            "base": 4,
            "content": True,
            "revision": None,
            "value": "a",
        },
        {
            "base": None,
            "content": True,
            "revision": 4,
            "value": "tabby",
        },
        {
            "base": 5,
            "content": False,
            "revision": 5,
            "value": "\t",
        },
        {
            "base": 6,
            "content": False,
            "revision": 6,
            "value": " ",
        },
    ]
