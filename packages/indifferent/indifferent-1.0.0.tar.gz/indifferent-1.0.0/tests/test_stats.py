from indifferent.indifferent import _stats


def test_empty():

    assert _stats(comparison_split=[]) == {
        "inputs": {
            "base": {"length": {"content": 0, "total": 0}},
            "revision": {"length": {"content": 0, "total": 0}},
        },
        "results": {
            "added": {
                "length": {"content": 0, "total": 0},
            },
            "matched": {
                "base_preserved": {"content": 0, "total": 0},
                "length": {"content": 0, "total": 0},
                "revision_matched": {"content": 0, "total": 0},
            },
            "removed": {
                "length": {"content": 0, "total": 0},
            },
        },
        "score": {"content": 0, "total": 0},
    }


def test_match_single_content():
    assert _stats(
        comparison_split=[{"base": 0, "content": True, "revision": 0, "value": "cat"}]
    ) == {
        "inputs": {
            "base": {"length": {"content": 1, "total": 1}},
            "revision": {"length": {"content": 1, "total": 1}},
        },
        "results": {
            "added": {
                "length": {"content": 0, "total": 0},
            },
            "matched": {
                "base_preserved": {"content": 1.0, "total": 1.0},
                "length": {"content": 1, "total": 1},
                "revision_matched": {"content": 1.0, "total": 1.0},
            },
            "removed": {
                "length": {"content": 0, "total": 0},
            },
        },
        "score": {"content": 1.0, "total": 1.0},
    }


def test_match_single_separator():
    assert _stats(
        comparison_split=[{"base": 0, "content": False, "revision": 0, "value": " "}]
    ) == {
        "inputs": {
            "base": {"length": {"content": 0, "total": 1}},
            "revision": {"length": {"content": 0, "total": 1}},
        },
        "results": {
            "added": {
                "length": {"content": 0, "total": 0},
            },
            "matched": {
                "base_preserved": {"content": 0, "total": 1.0},
                "length": {"content": 0, "total": 1},
                "revision_matched": {"content": 0, "total": 1.0},
            },
            "removed": {
                "length": {"content": 0, "total": 0},
            },
        },
        "score": {"content": 0, "total": 1.0},
    }


def test_match():
    assert _stats(
        comparison_split=[
            {"base": 0, "content": True, "revision": 0, "value": "a"},
            {"base": 1, "content": False, "revision": 1, "value": " "},
            {"base": 2, "content": True, "revision": 2, "value": "cat"},
        ]
    ) == {
        "inputs": {
            "base": {"length": {"content": 2, "total": 3}},
            "revision": {"length": {"content": 2, "total": 3}},
        },
        "results": {
            "added": {
                "length": {"content": 0, "total": 0},
            },
            "matched": {
                "base_preserved": {"content": 1.0, "total": 1.0},
                "length": {"content": 2, "total": 3},
                "revision_matched": {"content": 1.0, "total": 1.0},
            },
            "removed": {
                "length": {"content": 0, "total": 0},
            },
        },
        "score": {"content": 1.0, "total": 1.0},
    }


def test_no_match_content():
    assert _stats(
        comparison_split=[
            {"base": 0, "content": True, "revision": None, "value": "a"},
            {"base": None, "content": True, "revision": 0, "value": "cat"},
        ]
    ) == {
        "inputs": {
            "base": {"length": {"content": 1, "total": 1}},
            "revision": {"length": {"content": 1, "total": 1}},
        },
        "results": {
            "added": {
                "length": {"content": 1, "total": 1},
            },
            "matched": {
                "base_preserved": {"content": 0, "total": 0},
                "length": {"content": 0, "total": 0},
                "revision_matched": {"content": 0, "total": 0},
            },
            "removed": {
                "length": {"content": 1, "total": 1},
            },
        },
        "score": {"content": 0, "total": 0},
    }


def test_no_match_separator():
    assert _stats(
        comparison_split=[
            {"base": 0, "content": False, "revision": None, "value": " "},
            {"base": None, "content": False, "revision": 0, "value": "\t"},
        ]
    ) == {
        "inputs": {
            "base": {"length": {"content": 0, "total": 1}},
            "revision": {"length": {"content": 0, "total": 1}},
        },
        "results": {
            "added": {
                "length": {"content": 0, "total": 1},
            },
            "matched": {
                "base_preserved": {"content": 0, "total": 0},
                "length": {"content": 0, "total": 0},
                "revision_matched": {"content": 0, "total": 0},
            },
            "removed": {
                "length": {"content": 0, "total": 1},
            },
        },
        "score": {"content": 0, "total": 0},
    }


def test_leading_base_separator():
    assert _stats(
        comparison_split=[
            {"base": 0, "content": False, "revision": None, "value": " "},
            {"base": 1, "content": True, "revision": 0, "value": "a"},
            {"base": 2, "content": False, "revision": 1, "value": " "},
            {"base": 3, "content": True, "revision": 2, "value": "cat"},
        ]
    ) == {
        "inputs": {
            "base": {"length": {"content": 2, "total": 4}},
            "revision": {"length": {"content": 2, "total": 3}},
        },
        "results": {
            "added": {
                "length": {"content": 0, "total": 0},
            },
            "matched": {
                "base_preserved": {"content": 1.0, "total": 0.75},
                "length": {"content": 2, "total": 3},
                "revision_matched": {"content": 1.0, "total": 1.0},
            },
            "removed": {
                "length": {"content": 0, "total": 1},
            },
        },
        "score": {"content": 1.0, "total": 0.75},
    }


def test_leading_revision_separator():
    assert _stats(
        comparison_split=[
            {"base": None, "content": False, "revision": 0, "value": " "},
            {"base": 0, "content": True, "revision": 1, "value": "a"},
            {"base": 1, "content": False, "revision": 2, "value": " "},
            {"base": 2, "content": True, "revision": 3, "value": "cat"},
        ]
    ) == {
        "inputs": {
            "base": {"length": {"content": 2, "total": 3}},
            "revision": {"length": {"content": 2, "total": 4}},
        },
        "results": {
            "added": {
                "length": {"content": 0, "total": 1},
            },
            "matched": {
                "base_preserved": {"content": 1.0, "total": 1.0},
                "length": {"content": 2, "total": 3},
                "revision_matched": {"content": 1.0, "total": 0.75},
            },
            "removed": {
                "length": {"content": 0, "total": 0},
            },
        },
        "score": {"content": 1.0, "total": 0.75},
    }


def test_trailing_base_separator():
    assert _stats(
        comparison_split=[
            {"base": 0, "content": True, "revision": 0, "value": "a"},
            {"base": 1, "content": False, "revision": 1, "value": " "},
            {"base": 2, "content": True, "revision": 2, "value": "cat"},
            {"base": 3, "content": False, "revision": None, "value": " "},
        ]
    ) == {
        "inputs": {
            "base": {"length": {"content": 2, "total": 4}},
            "revision": {"length": {"content": 2, "total": 3}},
        },
        "results": {
            "added": {
                "length": {"content": 0, "total": 0},
            },
            "matched": {
                "base_preserved": {"content": 1.0, "total": 0.75},
                "length": {"content": 2, "total": 3},
                "revision_matched": {"content": 1.0, "total": 1.0},
            },
            "removed": {
                "length": {"content": 0, "total": 1},
            },
        },
        "score": {"content": 1.0, "total": 0.75},
    }


def test_trailing_revision_separator():
    assert _stats(
        comparison_split=[
            {"base": 0, "content": True, "revision": 0, "value": "a"},
            {"base": 1, "content": False, "revision": 1, "value": " "},
            {"base": 2, "content": True, "revision": 2, "value": "cat"},
            {"base": None, "content": False, "revision": 3, "value": " "},
        ]
    ) == {
        "inputs": {
            "base": {"length": {"content": 2, "total": 3}},
            "revision": {"length": {"content": 2, "total": 4}},
        },
        "results": {
            "added": {
                "length": {"content": 0, "total": 1},
            },
            "matched": {
                "base_preserved": {"content": 1.0, "total": 1.0},
                "length": {"content": 2, "total": 3},
                "revision_matched": {"content": 1.0, "total": 0.75},
            },
            "removed": {
                "length": {"content": 0, "total": 0},
            },
        },
        "score": {"content": 1.0, "total": 0.75},
    }


def test_leading_trailing_base_separator():
    assert _stats(
        comparison_split=[
            {"base": 0, "content": False, "revision": None, "value": " "},
            {"base": 1, "content": True, "revision": 0, "value": "a"},
            {"base": 2, "content": False, "revision": 1, "value": " "},
            {"base": 3, "content": True, "revision": 2, "value": "cat"},
            {"base": 4, "content": False, "revision": None, "value": " "},
        ]
    ) == {
        "inputs": {
            "base": {"length": {"content": 2, "total": 5}},
            "revision": {"length": {"content": 2, "total": 3}},
        },
        "results": {
            "added": {
                "length": {"content": 0, "total": 0},
            },
            "matched": {
                "base_preserved": {"content": 1.0, "total": 0.6},
                "length": {"content": 2, "total": 3},
                "revision_matched": {"content": 1.0, "total": 1.0},
            },
            "removed": {
                "length": {"content": 0, "total": 2},
            },
        },
        "score": {"content": 1.0, "total": 0.6},
    }


def test_leading_trailing_revision_separator():
    assert _stats(
        comparison_split=[
            {"base": None, "content": False, "revision": 0, "value": " "},
            {"base": 0, "content": True, "revision": 1, "value": "a"},
            {"base": 1, "content": False, "revision": 2, "value": " "},
            {"base": 2, "content": True, "revision": 3, "value": "cat"},
            {"base": None, "content": False, "revision": 4, "value": " "},
        ]
    ) == {
        "inputs": {
            "base": {"length": {"content": 2, "total": 3}},
            "revision": {"length": {"content": 2, "total": 5}},
        },
        "results": {
            "added": {
                "length": {"content": 0, "total": 2},
            },
            "matched": {
                "base_preserved": {"content": 1.0, "total": 1.0},
                "length": {"content": 2, "total": 3},
                "revision_matched": {"content": 1.0, "total": 0.6},
            },
            "removed": {
                "length": {"content": 0, "total": 0},
            },
        },
        "score": {"content": 1.0, "total": 0.6},
    }


def test_leading_trailing_both_separator():
    assert _stats(
        comparison_split=[
            {"base": 0, "content": False, "revision": 0, "value": " "},
            {"base": 1, "content": True, "revision": 1, "value": "a"},
            {"base": 2, "content": False, "revision": 2, "value": " "},
            {"base": 3, "content": True, "revision": 3, "value": "cat"},
            {"base": 4, "content": False, "revision": 4, "value": " "},
        ]
    ) == {
        "inputs": {
            "base": {"length": {"content": 2, "total": 5}},
            "revision": {"length": {"content": 2, "total": 5}},
        },
        "results": {
            "added": {
                "length": {"content": 0, "total": 0},
            },
            "matched": {
                "base_preserved": {"content": 1.0, "total": 1.0},
                "length": {"content": 2, "total": 5},
                "revision_matched": {"content": 1.0, "total": 1.0},
            },
            "removed": {
                "length": {"content": 0, "total": 0},
            },
        },
        "score": {"content": 1.0, "total": 1.0},  # ????
    }
