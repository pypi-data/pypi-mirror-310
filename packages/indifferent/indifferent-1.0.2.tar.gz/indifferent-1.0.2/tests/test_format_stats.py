from indifferent.indifferent import _format_stats


def test_empty():
    assert _format_stats(
        stats={
            "inputs": {
                "base": {"length": {"content": 0, "total": 0}},
                "revision": {"length": {"content": 0, "total": 0}},
            },
            "results": {
                "added": {"length": {"content": 0, "total": 0}},
                "matched": {
                    "base_preserved": {"content": 0, "total": 0},
                    "length": {"content": 0, "total": 0},
                    "revision_matched": {"content": 0, "total": 0},
                },
                "removed": {"length": {"content": 0, "total": 0}},
            },
            "score": {"content": 0, "total": 0},
        }
    ) == {
        "base": [
            {"label": "Base length", "value": "0 words and 0 separators (0 total)"},
            {"label": "Words also in the revision", "value": "0 of 0 (0%)"},
            {"label": "Similarity", "value": "0% identical to the revision"},
        ],
        "matched": [
            {
                "label": "Identical in base and revision",
                "value": "0 words and 0 separators (0 total)",
            },
            {
                "label": "Removed from the base",
                "value": "0 words and 0 separators (0 total)",
            },
            {
                "label": "Added by the revision",
                "value": "0 words and 0 separators (0 total)",
            },
        ],
        "revision": [
            {"label": "Revision length", "value": "0 words and 0 separators (0 total)"},
            {"label": "Words also in the base", "value": "0 of 0 (0%)"},
            {"label": "Similarity", "value": "0% identical to the base"},
        ],
        "summary": "0% match",
    }


def test_single_match():
    assert _format_stats(
        {
            "inputs": {
                "base": {"length": {"content": 1, "total": 1}},
                "revision": {"length": {"content": 1, "total": 1}},
            },
            "results": {
                "added": {"length": {"content": 0, "total": 0}},
                "matched": {
                    "base_preserved": {"content": 1.0, "total": 1.0},
                    "length": {"content": 1, "total": 1},
                    "revision_matched": {"content": 1.0, "total": 1.0},
                },
                "removed": {"length": {"content": 0, "total": 0}},
            },
            "score": {"content": 1.0, "total": 1.0},
        }
    ) == {
        "base": [
            {"label": "Base length", "value": "1 word and 0 separators (1 total)"},
            {"label": "Words also in the revision", "value": "1 of 1 (100%)"},
            {"label": "Similarity", "value": "100% identical to the revision"},
        ],
        "matched": [
            {
                "label": "Identical in base and revision",
                "value": "1 word and 0 separators (1 total)",
            },
            {
                "label": "Removed from the base",
                "value": "0 words and 0 separators (0 total)",
            },
            {
                "label": "Added by the revision",
                "value": "0 words and 0 separators (0 total)",
            },
        ],
        "revision": [
            {"label": "Revision length", "value": "1 word and 0 separators (1 total)"},
            {"label": "Words also in the base", "value": "1 of 1 (100%)"},
            {"label": "Similarity", "value": "100% identical to the base"},
        ],
        "summary": "100% match",
    }


def test_no_match():
    assert _format_stats(
        {
            "inputs": {
                "base": {"length": {"content": 1, "total": 1}},
                "revision": {"length": {"content": 1, "total": 1}},
            },
            "results": {
                "added": {"length": {"content": 1, "total": 1}},
                "matched": {
                    "base_preserved": {"content": 0, "total": 0},
                    "length": {"content": 0, "total": 0},
                    "revision_matched": {"content": 0, "total": 0},
                },
                "removed": {"length": {"content": 1, "total": 1}},
            },
            "score": {"content": 0, "total": 0},
        }
    ) == {
        "base": [
            {"label": "Base length", "value": "1 word and 0 separators (1 total)"},
            {"label": "Words also in the revision", "value": "0 of 1 (0%)"},
            {"label": "Similarity", "value": "0% identical to the revision"},
        ],
        "matched": [
            {
                "label": "Identical in base and revision",
                "value": "0 words and 0 separators (0 total)",
            },
            {
                "label": "Removed from the base",
                "value": "1 word and 0 separators (1 total)",
            },
            {
                "label": "Added by the revision",
                "value": "1 word and 0 separators (1 total)",
            },
        ],
        "revision": [
            {"label": "Revision length", "value": "1 word and 0 separators (1 total)"},
            {"label": "Words also in the base", "value": "0 of 1 (0%)"},
            {"label": "Similarity", "value": "0% identical to the base"},
        ],
        "summary": "0% match",
    }


def test_partial_match():
    assert _format_stats(
        {
            "inputs": {
                "base": {"length": {"content": 1, "total": 1}},
                "revision": {"length": {"content": 2, "total": 3}},
            },
            "results": {
                "added": {"length": {"content": 1, "total": 2}},
                "matched": {
                    "base_preserved": {"content": 1.0, "total": 1.0},
                    "length": {"content": 1, "total": 1},
                    "revision_matched": {"content": 0.5, "total": 0.3333333333333333},
                },
                "removed": {"length": {"content": 0, "total": 0}},
            },
            "score": {"content": 0.5, "total": 0.3333333333333333},
        }
    ) == {
        "base": [
            {"label": "Base length", "value": "1 word and 0 separators (1 total)"},
            {"label": "Words also in the revision", "value": "1 of 1 (100%)"},
            {"label": "Similarity", "value": "100% identical to the revision"},
        ],
        "matched": [
            {
                "label": "Identical in base and revision",
                "value": "1 word and 0 separators (1 total)",
            },
            {
                "label": "Removed from the base",
                "value": "0 words and 0 separators (0 total)",
            },
            {
                "label": "Added by the revision",
                "value": "1 word and 1 separator (2 total)",
            },
        ],
        "revision": [
            {"label": "Revision length", "value": "2 words and 1 separator (3 total)"},
            {"label": "Words also in the base", "value": "1 of 2 (50%)"},
            {"label": "Similarity", "value": "33% identical to the base"},
        ],
        "summary": "50% match",
    }


def test_separator_match():
    assert _format_stats(
        {
            "inputs": {
                "base": {"length": {"content": 0, "total": 1}},
                "revision": {"length": {"content": 0, "total": 1}},
            },
            "results": {
                "added": {"length": {"content": 0, "total": 0}},
                "matched": {
                    "base_preserved": {"content": 0, "total": 1.0},
                    "length": {"content": 0, "total": 1},
                    "revision_matched": {"content": 0, "total": 1.0},
                },
                "removed": {"length": {"content": 0, "total": 0}},
            },
            "score": {"content": 0, "total": 1.0},
        }
    ) == {
        "base": [
            {"label": "Base length", "value": "0 words and 1 separator (1 total)"},
            {"label": "Words also in the revision", "value": "0 of 0 (0%)"},
            {"label": "Similarity", "value": "100% identical to the revision"},
        ],
        "matched": [
            {
                "label": "Identical in base and revision",
                "value": "0 words and 1 separator (1 total)",
            },
            {
                "label": "Removed from the base",
                "value": "0 words and 0 separators (0 total)",
            },
            {
                "label": "Added by the revision",
                "value": "0 words and 0 separators (0 total)",
            },
        ],
        "revision": [
            {"label": "Revision length", "value": "0 words and 1 separator (1 total)"},
            {"label": "Words also in the base", "value": "0 of 0 (0%)"},
            {"label": "Similarity", "value": "100% identical to the base"},
        ],
        "summary": "0% match",
    }


def test_separator_no_match():
    assert _format_stats(
        {
            "inputs": {
                "base": {"length": {"content": 0, "total": 1}},
                "revision": {"length": {"content": 0, "total": 1}},
            },
            "results": {
                "added": {"length": {"content": 0, "total": 1}},
                "matched": {
                    "base_preserved": {"content": 0, "total": 0},
                    "length": {"content": 0, "total": 0},
                    "revision_matched": {"content": 0, "total": 0},
                },
                "removed": {"length": {"content": 0, "total": 1}},
            },
            "score": {"content": 0, "total": 0},
        }
    ) == {
        "base": [
            {"label": "Base length", "value": "0 words and 1 separator (1 total)"},
            {"label": "Words also in the revision", "value": "0 of 0 (0%)"},
            {"label": "Similarity", "value": "0% identical to the revision"},
        ],
        "matched": [
            {
                "label": "Identical in base and revision",
                "value": "0 words and 0 separators (0 total)",
            },
            {
                "label": "Removed from the base",
                "value": "0 words and 1 separator (1 total)",
            },
            {
                "label": "Added by the revision",
                "value": "0 words and 1 separator (1 total)",
            },
        ],
        "revision": [
            {"label": "Revision length", "value": "0 words and 1 separator (1 total)"},
            {"label": "Words also in the base", "value": "0 of 0 (0%)"},
            {"label": "Similarity", "value": "0% identical to the base"},
        ],
        "summary": "0% match",
    }
