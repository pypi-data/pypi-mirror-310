from indifferent.indifferent import _forward_fill


def test_empty():
    assert (
        _forward_fill(
            base_split=[],
            revision_split=[],
            base_last_match=None,
            revision_last_match=None,
        )
        == []
    )


def test_no_forward_fill(a, space, cat):
    assert (
        _forward_fill(
            base_split=[a, space, cat],
            revision_split=[a, space, cat],
            base_last_match=2,
            revision_last_match=2,
        )
        == []
    )


def test_base_forward_fill(a, space, tabby, cat):
    assert _forward_fill(
        base_split=[a, space, tabby, space, cat],
        revision_split=[a, space, tabby],
        base_last_match=2,
        revision_last_match=2,
    ) == [
        {"base": 3, "content": False, "revision": None, "value": " "},
        {"base": 4, "content": True, "revision": None, "value": "cat"},
    ]


def test_space_match_base_forward_fill(a, space, tabby, cat):
    assert _forward_fill(
        base_split=[a, space, tabby, space, cat],
        revision_split=[a, space, tabby, space],
        base_last_match=2,
        revision_last_match=2,
    ) == [
        {"base": 3, "content": False, "revision": 3, "value": " "},
        {"base": 4, "content": True, "revision": None, "value": "cat"},
    ]


def test_base_forward_fill_space_match(a, space, tabby, cat):
    assert _forward_fill(
        base_split=[a, space, tabby, space, cat, space],
        revision_split=[a, space, tabby, space],
        base_last_match=2,
        revision_last_match=2,
    ) == [
        {"base": 3, "content": False, "revision": 3, "value": " "},
        {"base": 4, "content": True, "revision": None, "value": "cat"},
        {"base": 5, "content": False, "revision": None, "value": " "},
    ]


def test_revision_forward_fill(a, space, tabby, cat):
    assert _forward_fill(
        base_split=[a, space, tabby],
        revision_split=[a, space, tabby, space, cat],
        base_last_match=2,
        revision_last_match=2,
    ) == [
        {"base": None, "content": False, "revision": 3, "value": " "},
        {"base": None, "content": True, "revision": 4, "value": "cat"},
    ]


def test_space_match_revision_forward_fill(a, space, tabby, cat):
    assert _forward_fill(
        base_split=[a, space, tabby, space],
        revision_split=[a, space, tabby, space, cat],
        base_last_match=2,
        revision_last_match=2,
    ) == [
        {"base": 3, "content": False, "revision": 3, "value": " "},
        {"base": None, "content": True, "revision": 4, "value": "cat"},
    ]


def test_revision_forward_fill_space_match(a, space, tabby, cat):
    assert _forward_fill(
        base_split=[a, space, tabby, space],
        revision_split=[a, space, tabby, space, cat, space],
        base_last_match=2,
        revision_last_match=2,
    ) == [
        {"base": 3, "content": False, "revision": 3, "value": " "},
        {"base": None, "content": True, "revision": 4, "value": "cat"},
        {"base": None, "content": False, "revision": 5, "value": " "},
    ]
