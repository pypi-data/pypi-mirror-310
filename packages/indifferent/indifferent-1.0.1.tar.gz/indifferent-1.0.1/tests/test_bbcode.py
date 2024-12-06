from indifferent.indifferent import _format_bbcode


def test_empty():
    assert _format_bbcode([]) == {
        "analysis": {
            "base": "[b]Base length:[/b]\n"
            "0 words and 0 separators (0 total)\n"
            "\n"
            "[b]Words also in the revision:[/b]\n"
            "0 of 0 (0%)\n"
            "\n"
            "[b]Similarity:[/b]\n"
            "0% identical to the revision",
            "matched": "[b]Identical in base and revision:[/b]\n"
            "0 words and 0 separators (0 total)\n"
            "\n"
            "[b]Removed from the base:[/b]\n"
            "0 words and 0 separators (0 total)\n"
            "\n"
            "[b]Added by the revision:[/b]\n"
            "0 words and 0 separators (0 total)",
            "revision": "[b]Revision length:[/b]\n"
            "0 words and 0 separators (0 total)\n"
            "\n"
            "[b]Words also in the base:[/b]\n"
            "0 of 0 (0%)\n"
            "\n"
            "[b]Similarity:[/b]\n"
            "0% identical to the base",
        },
        "matched": "",
        "summary": "0% match",
    }


def test_match():

    assert _format_bbcode(
        [{"base": 0, "content": True, "revision": 0, "value": "cat"}]
    ) == {
        "analysis": {
            "base": "[b]Base length:[/b]\n"
            "1 word and 0 separators (1 total)\n"
            "\n"
            "[b]Words also in the revision:[/b]\n"
            "1 of 1 (100%)\n"
            "\n"
            "[b]Similarity:[/b]\n"
            "100% identical to the revision",
            "matched": "[b]Identical in base and revision:[/b]\n"
            "1 word and 0 separators (1 total)\n"
            "\n"
            "[b]Removed from the base:[/b]\n"
            "0 words and 0 separators (0 total)\n"
            "\n"
            "[b]Added by the revision:[/b]\n"
            "0 words and 0 separators (0 total)",
            "revision": "[b]Revision length:[/b]\n"
            "1 word and 0 separators (1 total)\n"
            "\n"
            "[b]Words also in the base:[/b]\n"
            "1 of 1 (100%)\n"
            "\n"
            "[b]Similarity:[/b]\n"
            "100% identical to the base",
        },
        "matched": "cat",
        "summary": "100% match",
    }


def test_no_match():
    assert _format_bbcode(
        [
            {"base": 0, "content": True, "revision": None, "value": "tabby"},
            {"base": None, "content": True, "revision": 0, "value": "cat"},
        ]
    ) == {
        "analysis": {
            "base": "[b]Base length:[/b]\n"
            "1 word and 0 separators (1 total)\n"
            "\n"
            "[b]Words also in the revision:[/b]\n"
            "0 of 1 (0%)\n"
            "\n"
            "[b]Similarity:[/b]\n"
            "0% identical to the revision",
            "matched": "[b]Identical in base and revision:[/b]\n"
            "0 words and 0 separators (0 total)\n"
            "\n"
            "[b]Removed from the base:[/b]\n"
            "1 word and 0 separators (1 total)\n"
            "\n"
            "[b]Added by the revision:[/b]\n"
            "1 word and 0 separators (1 total)",
            "revision": "[b]Revision length:[/b]\n"
            "1 word and 0 separators (1 total)\n"
            "\n"
            "[b]Words also in the base:[/b]\n"
            "0 of 1 (0%)\n"
            "\n"
            "[b]Similarity:[/b]\n"
            "0% identical to the base",
        },
        "matched": "[s red]tabby[/s red][u green]cat[/u green]",
        "summary": "0% match",
    }


def test_separator_match():
    assert _format_bbcode(
        [{"base": 0, "content": False, "revision": 0, "value": " "}]
    ) == {
        "analysis": {
            "base": "[b]Base length:[/b]\n"
            "0 words and 1 separator (1 total)\n"
            "\n"
            "[b]Words also in the revision:[/b]\n"
            "0 of 0 (0%)\n"
            "\n"
            "[b]Similarity:[/b]\n"
            "100% identical to the revision",
            "matched": "[b]Identical in base and revision:[/b]\n"
            "0 words and 1 separator (1 total)\n"
            "\n"
            "[b]Removed from the base:[/b]\n"
            "0 words and 0 separators (0 total)\n"
            "\n"
            "[b]Added by the revision:[/b]\n"
            "0 words and 0 separators (0 total)",
            "revision": "[b]Revision length:[/b]\n"
            "0 words and 1 separator (1 total)\n"
            "\n"
            "[b]Words also in the base:[/b]\n"
            "0 of 0 (0%)\n"
            "\n"
            "[b]Similarity:[/b]\n"
            "100% identical to the base",
        },
        "matched": " ",
        "summary": "0% match",
    }


def test_separator_no_match():
    assert _format_bbcode(
        [
            {"base": 0, "content": False, "revision": None, "value": " "},
            {"base": None, "content": False, "revision": 0, "value": "\t"},
        ]
    ) == {
        "analysis": {
            "base": "[b]Base length:[/b]\n"
            "0 words and 1 separator (1 total)\n"
            "\n"
            "[b]Words also in the revision:[/b]\n"
            "0 of 0 (0%)\n"
            "\n"
            "[b]Similarity:[/b]\n"
            "0% identical to the revision",
            "matched": "[b]Identical in base and revision:[/b]\n"
            "0 words and 0 separators (0 total)\n"
            "\n"
            "[b]Removed from the base:[/b]\n"
            "0 words and 1 separator (1 total)\n"
            "\n"
            "[b]Added by the revision:[/b]\n"
            "0 words and 1 separator (1 total)",
            "revision": "[b]Revision length:[/b]\n"
            "0 words and 1 separator (1 total)\n"
            "\n"
            "[b]Words also in the base:[/b]\n"
            "0 of 0 (0%)\n"
            "\n"
            "[b]Similarity:[/b]\n"
            "0% identical to the base",
        },
        "matched": "[s red] [/s red][u green]   ⇥[/u green]",
        "summary": "0% match",
    }


def test_beginning_end_match_middle_different():
    assert _format_bbcode(
        [
            {"base": 0, "content": True, "revision": 0, "value": "a"},
            {"base": 1, "content": False, "revision": 1, "value": " "},
            {"base": 2, "content": True, "revision": None, "value": "big"},
            {"base": None, "content": True, "revision": 2, "value": "tabby"},
            {"base": 3, "content": False, "revision": 3, "value": " "},
            {"base": 4, "content": True, "revision": 4, "value": "cat"},
        ]
    ) == {
        "analysis": {
            "base": "[b]Base length:[/b]\n"
            "3 words and 2 separators (5 total)\n"
            "\n"
            "[b]Words also in the revision:[/b]\n"
            "2 of 3 (67%)\n"
            "\n"
            "[b]Similarity:[/b]\n"
            "80% identical to the revision",
            "matched": "[b]Identical in base and revision:[/b]\n"
            "2 words and 2 separators (4 total)\n"
            "\n"
            "[b]Removed from the base:[/b]\n"
            "1 word and 0 separators (1 total)\n"
            "\n"
            "[b]Added by the revision:[/b]\n"
            "1 word and 0 separators (1 total)",
            "revision": "[b]Revision length:[/b]\n"
            "3 words and 2 separators (5 total)\n"
            "\n"
            "[b]Words also in the base:[/b]\n"
            "2 of 3 (67%)\n"
            "\n"
            "[b]Similarity:[/b]\n"
            "80% identical to the base",
        },
        "matched": "a [s red]big[/s red][u green]tabby[/u green] cat",
        "summary": "50% match",
    }
