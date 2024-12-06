from indifferent.indifferent import _base_revision_comparison


def test_empty():
    assert (
        _base_revision_comparison(
            base_split=[],
            revision_split=[],
        )
        == []
    )


def test_single_content_match(cat):
    assert _base_revision_comparison(
        base_split=[cat],
        revision_split=[cat],
    ) == [
        {
            "base": 0,
            "revision": 0,
            "content": True,
            "value": "cat",
        }
    ]


def test_single_separator_match(space):
    assert _base_revision_comparison(
        base_split=[space],
        revision_split=[space],
    ) == [
        {
            "base": 0,
            "revision": 0,
            "content": False,
            "value": " ",
        }
    ]


def test_single_content_no_match(tabby, cat):
    assert _base_revision_comparison(
        base_split=[tabby],
        revision_split=[cat],
    ) == [
        {
            "base": 0,
            "revision": None,
            "content": True,
            "value": "tabby",
        },
        {
            "base": None,
            "revision": 0,
            "content": True,
            "value": "cat",
        },
    ]


def test_single_separator_no_match(space, tab):
    assert _base_revision_comparison(
        base_split=[space],
        revision_split=[tab],
    ) == [
        {
            "base": 0,
            "revision": None,
            "content": False,
            "value": " ",
        },
        {
            "base": None,
            "revision": 0,
            "content": False,
            "value": "\t",
        },
    ]


def test_single_base_content(cat):
    assert _base_revision_comparison(
        base_split=[cat],
        revision_split=[],
    ) == [
        {
            "base": 0,
            "revision": None,
            "content": True,
            "value": "cat",
        }
    ]


def test_single_revision_content(cat):
    assert _base_revision_comparison(
        base_split=[],
        revision_split=[cat],
    ) == [
        {
            "base": None,
            "revision": 0,
            "content": True,
            "value": "cat",
        }
    ]


def test_single_base_separator(space):
    assert _base_revision_comparison(
        base_split=[space],
        revision_split=[],
    ) == [
        {
            "base": 0,
            "revision": None,
            "content": False,
            "value": " ",
        }
    ]


def test_single_revision_separator(space):
    assert _base_revision_comparison(
        base_split=[],
        revision_split=[space],
    ) == [
        {
            "base": None,
            "revision": 0,
            "content": False,
            "value": " ",
        }
    ]


def test_single_base_separator_revision_content(space, cat):
    assert _base_revision_comparison(
        base_split=[space],
        revision_split=[cat],
    ) == [
        {
            "base": 0,
            "revision": None,
            "content": False,
            "value": " ",
        },
        {
            "base": None,
            "revision": 0,
            "content": True,
            "value": "cat",
        },
    ]


def test_single_base_content_revision_separator(space, cat):
    assert _base_revision_comparison(
        base_split=[cat],
        revision_split=[space],
    ) == [
        {
            "base": 0,
            "revision": None,
            "content": True,
            "value": "cat",
        },
        {
            "base": None,
            "revision": 0,
            "content": False,
            "value": " ",
        },
    ]


def test_content_match(a, tabby, cat, space):
    assert _base_revision_comparison(
        base_split=[a, space, tabby, space, cat],
        revision_split=[a, space, tabby, space, cat],
    ) == [
        {
            "base": 0,
            "revision": 0,
            "content": True,
            "value": "a",
        },
        {
            "base": 1,
            "revision": 1,
            "content": False,
            "value": " ",
        },
        {
            "base": 2,
            "revision": 2,
            "content": True,
            "value": "tabby",
        },
        {
            "base": 3,
            "revision": 3,
            "content": False,
            "value": " ",
        },
        {
            "base": 4,
            "revision": 4,
            "content": True,
            "value": "cat",
        },
    ]


def test_content_match_start_separator(a, tabby, cat, space):
    assert _base_revision_comparison(
        base_split=[space, a, space, tabby, space, cat],
        revision_split=[space, a, space, tabby, space, cat],
    ) == [
        {
            "base": 0,
            "revision": 0,
            "content": False,
            "value": " ",
        },
        {
            "base": 1,
            "revision": 1,
            "content": True,
            "value": "a",
        },
        {
            "base": 2,
            "revision": 2,
            "content": False,
            "value": " ",
        },
        {
            "base": 3,
            "revision": 3,
            "content": True,
            "value": "tabby",
        },
        {
            "base": 4,
            "revision": 4,
            "content": False,
            "value": " ",
        },
        {
            "base": 5,
            "revision": 5,
            "content": True,
            "value": "cat",
        },
    ]


def test_content_match_start_base_separator(a, tabby, cat, space):
    assert _base_revision_comparison(
        base_split=[space, a, space, tabby, space, cat],
        revision_split=[a, space, tabby, space, cat],
    ) == [
        {
            "base": 0,
            "revision": None,
            "content": False,
            "value": " ",
        },
        {
            "base": 1,
            "revision": 0,
            "content": True,
            "value": "a",
        },
        {
            "base": 2,
            "revision": 1,
            "content": False,
            "value": " ",
        },
        {
            "base": 3,
            "revision": 2,
            "content": True,
            "value": "tabby",
        },
        {
            "base": 4,
            "revision": 3,
            "content": False,
            "value": " ",
        },
        {
            "base": 5,
            "revision": 4,
            "content": True,
            "value": "cat",
        },
    ]


def test_content_match_start_revision_separator(a, tabby, cat, space):
    assert _base_revision_comparison(
        base_split=[a, space, tabby, space, cat],
        revision_split=[space, a, space, tabby, space, cat],
    ) == [
        {
            "base": None,
            "revision": 0,
            "content": False,
            "value": " ",
        },
        {
            "base": 0,
            "revision": 1,
            "content": True,
            "value": "a",
        },
        {
            "base": 1,
            "revision": 2,
            "content": False,
            "value": " ",
        },
        {
            "base": 2,
            "revision": 3,
            "content": True,
            "value": "tabby",
        },
        {
            "base": 3,
            "revision": 4,
            "content": False,
            "value": " ",
        },
        {
            "base": 4,
            "revision": 5,
            "content": True,
            "value": "cat",
        },
    ]


def test_content_match_end_separator(a, tabby, cat, space):
    assert _base_revision_comparison(
        base_split=[a, space, tabby, space, cat, space],
        revision_split=[a, space, tabby, space, cat, space],
    ) == [
        {
            "base": 0,
            "revision": 0,
            "content": True,
            "value": "a",
        },
        {
            "base": 1,
            "revision": 1,
            "content": False,
            "value": " ",
        },
        {
            "base": 2,
            "revision": 2,
            "content": True,
            "value": "tabby",
        },
        {
            "base": 3,
            "revision": 3,
            "content": False,
            "value": " ",
        },
        {
            "base": 4,
            "revision": 4,
            "content": True,
            "value": "cat",
        },
        {
            "base": 5,
            "revision": 5,
            "content": False,
            "value": " ",
        },
    ]


def test_content_match_end_base_separator(a, tabby, cat, space):
    assert _base_revision_comparison(
        base_split=[a, space, tabby, space, cat, space],
        revision_split=[a, space, tabby, space, cat],
    ) == [
        {
            "base": 0,
            "revision": 0,
            "content": True,
            "value": "a",
        },
        {
            "base": 1,
            "revision": 1,
            "content": False,
            "value": " ",
        },
        {
            "base": 2,
            "revision": 2,
            "content": True,
            "value": "tabby",
        },
        {
            "base": 3,
            "revision": 3,
            "content": False,
            "value": " ",
        },
        {
            "base": 4,
            "revision": 4,
            "content": True,
            "value": "cat",
        },
        {
            "base": 5,
            "revision": None,
            "content": False,
            "value": " ",
        },
    ]


def test_content_match_end_revision_separator(a, tabby, cat, space):
    assert _base_revision_comparison(
        base_split=[a, space, tabby, space, cat],
        revision_split=[a, space, tabby, space, cat, space],
    ) == [
        {
            "base": 0,
            "revision": 0,
            "content": True,
            "value": "a",
        },
        {
            "base": 1,
            "revision": 1,
            "content": False,
            "value": " ",
        },
        {
            "base": 2,
            "revision": 2,
            "content": True,
            "value": "tabby",
        },
        {
            "base": 3,
            "revision": 3,
            "content": False,
            "value": " ",
        },
        {
            "base": 4,
            "revision": 4,
            "content": True,
            "value": "cat",
        },
        {
            "base": None,
            "revision": 5,
            "content": False,
            "value": " ",
        },
    ]


def test_base_content_backfill_start(a, tabby, cat, space):
    assert _base_revision_comparison(
        base_split=[a, space, tabby, space, cat],
        revision_split=[tabby, space, cat],
    ) == [
        {
            "base": 0,
            "revision": None,
            "content": True,
            "value": "a",
        },
        {
            "base": 1,
            "revision": None,
            "content": False,
            "value": " ",
        },
        {
            "base": 2,
            "revision": 0,
            "content": True,
            "value": "tabby",
        },
        {
            "base": 3,
            "revision": 1,
            "content": False,
            "value": " ",
        },
        {
            "base": 4,
            "revision": 2,
            "content": True,
            "value": "cat",
        },
    ]


def test_revision_content_backfill_start(a, tabby, cat, space):
    assert _base_revision_comparison(
        base_split=[tabby, space, cat],
        revision_split=[a, space, tabby, space, cat],
    ) == [
        {
            "base": None,
            "revision": 0,
            "content": True,
            "value": "a",
        },
        {
            "base": None,
            "revision": 1,
            "content": False,
            "value": " ",
        },
        {
            "base": 0,
            "revision": 2,
            "content": True,
            "value": "tabby",
        },
        {
            "base": 1,
            "revision": 3,
            "content": False,
            "value": " ",
        },
        {
            "base": 2,
            "revision": 4,
            "content": True,
            "value": "cat",
        },
    ]


def test_base_content_backfill_middle(a, tabby, cat, space):
    assert _base_revision_comparison(
        base_split=[a, space, tabby, space, cat],
        revision_split=[a, space, cat],
    ) == [
        {
            "base": 0,
            "revision": 0,
            "content": True,
            "value": "a",
        },
        {
            "base": 1,
            "revision": 1,
            "content": False,
            "value": " ",
        },
        {
            "base": 2,
            "revision": None,
            "content": True,
            "value": "tabby",
        },
        {
            "base": 3,
            "revision": None,
            "content": False,
            "value": " ",
        },
        {
            "base": 4,
            "revision": 2,
            "content": True,
            "value": "cat",
        },
    ]


def test_revision_content_backfill_middle(a, tabby, cat, space):
    assert _base_revision_comparison(
        base_split=[a, space, cat],
        revision_split=[a, space, tabby, space, cat],
    ) == [
        {
            "base": 0,
            "revision": 0,
            "content": True,
            "value": "a",
        },
        {
            "base": 1,
            "revision": 1,
            "content": False,
            "value": " ",
        },
        {
            "base": None,
            "revision": 2,
            "content": True,
            "value": "tabby",
        },
        {
            "base": None,
            "revision": 3,
            "content": False,
            "value": " ",
        },
        {
            "base": 2,
            "revision": 4,
            "content": True,
            "value": "cat",
        },
    ]


def test_base_content_forward_fill_end(a, tabby, cat, space):
    assert _base_revision_comparison(
        base_split=[a, space, tabby, space, cat],
        revision_split=[a, space, tabby],
    ) == [
        {
            "base": 0,
            "revision": 0,
            "content": True,
            "value": "a",
        },
        {
            "base": 1,
            "revision": 1,
            "content": False,
            "value": " ",
        },
        {
            "base": 2,
            "revision": 2,
            "content": True,
            "value": "tabby",
        },
        {
            "base": 3,
            "revision": None,
            "content": False,
            "value": " ",
        },
        {
            "base": 4,
            "revision": None,
            "content": True,
            "value": "cat",
        },
    ]


def test_single_base_revision_content_forward_fill_end(a, tabby, cat, space):
    assert _base_revision_comparison(
        base_split=[a],
        revision_split=[a, space, tabby, space, cat],
    ) == [
        {
            "base": 0,
            "revision": 0,
            "content": True,
            "value": "a",
        },
        {
            "base": None,
            "revision": 1,
            "content": False,
            "value": " ",
        },
        {
            "base": None,
            "revision": 2,
            "content": True,
            "value": "tabby",
        },
        {
            "base": None,
            "revision": 3,
            "content": False,
            "value": " ",
        },
        {
            "base": None,
            "revision": 4,
            "content": True,
            "value": "cat",
        },
    ]


def test_single_revision_base_content_forward_fill_end(a, tabby, cat, space):
    assert _base_revision_comparison(
        base_split=[a, space, tabby, space, cat],
        revision_split=[a],
    ) == [
        {
            "base": 0,
            "revision": 0,
            "content": True,
            "value": "a",
        },
        {
            "base": 1,
            "revision": None,
            "content": False,
            "value": " ",
        },
        {
            "base": 2,
            "revision": None,
            "content": True,
            "value": "tabby",
        },
        {
            "base": 3,
            "revision": None,
            "content": False,
            "value": " ",
        },
        {
            "base": 4,
            "revision": None,
            "content": True,
            "value": "cat",
        },
    ]


def test_revision_content_forward_fill_end(a, tabby, cat, space):
    assert _base_revision_comparison(
        base_split=[a, space, tabby],
        revision_split=[a, space, tabby, space, cat],
    ) == [
        {
            "base": 0,
            "revision": 0,
            "content": True,
            "value": "a",
        },
        {
            "base": 1,
            "revision": 1,
            "content": False,
            "value": " ",
        },
        {
            "base": 2,
            "revision": 2,
            "content": True,
            "value": "tabby",
        },
        {
            "base": None,
            "revision": 3,
            "content": False,
            "value": " ",
        },
        {
            "base": None,
            "revision": 4,
            "content": True,
            "value": "cat",
        },
    ]


def test_same_beginning_end_different_middle(a, tabby, big, cat, space):
    assert _base_revision_comparison(
        base_split=[a, space, tabby, space, cat],
        revision_split=[a, space, big, space, cat],
    ) == [
        {
            "base": 0,
            "revision": 0,
            "content": True,
            "value": "a",
        },
        {
            "base": 1,
            "revision": 1,
            "content": False,
            "value": " ",
        },
        {
            "base": 2,
            "revision": None,
            "content": True,
            "value": "tabby",
        },
        {
            "base": None,
            "revision": 2,
            "content": True,
            "value": "big",
        },
        {
            "base": 3,
            "revision": 3,
            "content": False,
            "value": " ",
        },
        {
            "base": 4,
            "revision": 4,
            "content": True,
            "value": "cat",
        },
    ]


def test_different_beginning_same_end(tabby, big, cat, space):
    assert _base_revision_comparison(
        base_split=[tabby, space, cat],
        revision_split=[big, space, cat],
    ) == [
        {
            "base": 0,
            "revision": None,
            "content": True,
            "value": "tabby",
        },
        {
            "base": None,
            "revision": 0,
            "content": True,
            "value": "big",
        },
        {
            "base": 1,
            "revision": 1,
            "content": False,
            "value": " ",
        },
        {
            "base": 2,
            "revision": 2,
            "content": True,
            "value": "cat",
        },
    ]


def test_same_beginning_different_end(a, tabby, cat, space):
    assert _base_revision_comparison(
        base_split=[a, space, tabby],
        revision_split=[a, space, cat],
    ) == [
        {
            "base": 0,
            "revision": 0,
            "content": True,
            "value": "a",
        },
        {
            "base": 1,
            "revision": 1,
            "content": False,
            "value": " ",
        },
        {
            "base": 2,
            "revision": None,
            "content": True,
            "value": "tabby",
        },
        {
            "base": None,
            "revision": 2,
            "content": True,
            "value": "cat",
        },
    ]


def test_same_middle_different_start_different_end(the, a, big, tabby, cat, space):
    assert _base_revision_comparison(
        base_split=[a, space, big, space, tabby],
        revision_split=[the, space, big, space, cat],
    ) == [
        {
            "base": 0,
            "revision": None,
            "content": True,
            "value": "a",
        },
        {
            "base": None,
            "revision": 0,
            "content": True,
            "value": "the",
        },
        {
            "base": 1,
            "revision": 1,
            "content": False,
            "value": " ",
        },
        {
            "base": 2,
            "revision": 2,
            "content": True,
            "value": "big",
        },
        {
            "base": 3,
            "revision": 3,
            "content": False,
            "value": " ",
        },
        {
            "base": 4,
            "revision": None,
            "content": True,
            "value": "tabby",
        },
        {
            "base": None,
            "revision": 4,
            "content": True,
            "value": "cat",
        },
    ]
