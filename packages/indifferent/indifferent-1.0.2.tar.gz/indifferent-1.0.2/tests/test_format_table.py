from indifferent.indifferent import _format_table


def test_header_base():
    assert (
        _format_table(
            comparison_split=[
                {"base": 0, "content": True, "revision": 0, "value": "a"},
                {"base": 1, "content": False, "revision": 1, "value": " "},
                {"base": 2, "content": True, "revision": None, "value": "big"},
                {"base": None, "content": True, "revision": 2, "value": "tabby"},
                {"base": 3, "content": False, "revision": 3, "value": " "},
                {"base": 4, "content": True, "revision": 4, "value": "cat"},
            ]
        )
        .columns[0]
        .header
    ) == "Base"


def test_header_base_name():
    assert (
        _format_table(
            comparison_split=[
                {"base": 0, "content": True, "revision": 0, "value": "a"},
                {"base": 1, "content": False, "revision": 1, "value": " "},
                {"base": 2, "content": True, "revision": None, "value": "big"},
                {"base": None, "content": True, "revision": 2, "value": "tabby"},
                {"base": 3, "content": False, "revision": 3, "value": " "},
                {"base": 4, "content": True, "revision": 4, "value": "cat"},
            ],
            base_name="The base name",
        )
        .columns[0]
        .header
    ) == "Base: The base name"


def test_header_revision():
    assert (
        _format_table(
            comparison_split=[
                {"base": 0, "content": True, "revision": 0, "value": "a"},
                {"base": 1, "content": False, "revision": 1, "value": " "},
                {"base": 2, "content": True, "revision": None, "value": "big"},
                {"base": None, "content": True, "revision": 2, "value": "tabby"},
                {"base": 3, "content": False, "revision": 3, "value": " "},
                {"base": 4, "content": True, "revision": 4, "value": "cat"},
            ]
        )
        .columns[1]
        .header
    ) == "Revision"


def test_header_revision_name():
    assert (
        _format_table(
            comparison_split=[
                {"base": 0, "content": True, "revision": 0, "value": "a"},
                {"base": 1, "content": False, "revision": 1, "value": " "},
                {"base": 2, "content": True, "revision": None, "value": "big"},
                {"base": None, "content": True, "revision": 2, "value": "tabby"},
                {"base": 3, "content": False, "revision": 3, "value": " "},
                {"base": 4, "content": True, "revision": 4, "value": "cat"},
            ],
            revision_name="The revision name",
        )
        .columns[1]
        .header
    ) == "Revision: The revision name"


def test_header_comparison():
    assert (
        _format_table(
            comparison_split=[
                {"base": 0, "content": True, "revision": 0, "value": "a"},
                {"base": 1, "content": False, "revision": 1, "value": " "},
                {"base": 2, "content": True, "revision": None, "value": "big"},
                {"base": None, "content": True, "revision": 2, "value": "tabby"},
                {"base": 3, "content": False, "revision": 3, "value": " "},
                {"base": 4, "content": True, "revision": 4, "value": "cat"},
            ]
        )
        .columns[2]
        .header
    ) == "Comparison: 50% match"


def test_0_0():
    assert (
        _format_table(
            comparison_split=[
                {"base": 0, "content": True, "revision": 0, "value": "a"},
                {"base": 1, "content": False, "revision": 1, "value": " "},
                {"base": 2, "content": True, "revision": None, "value": "big"},
                {"base": None, "content": True, "revision": 2, "value": "tabby"},
                {"base": 3, "content": False, "revision": 3, "value": " "},
                {"base": 4, "content": True, "revision": 4, "value": "cat"},
            ]
        )
        .columns[0]
        ._cells[0]
    ) == "a big cat"


def test_1_0():
    assert (
        _format_table(
            comparison_split=[
                {"base": 0, "content": True, "revision": 0, "value": "a"},
                {"base": 1, "content": False, "revision": 1, "value": " "},
                {"base": 2, "content": True, "revision": None, "value": "big"},
                {"base": None, "content": True, "revision": 2, "value": "tabby"},
                {"base": 3, "content": False, "revision": 3, "value": " "},
                {"base": 4, "content": True, "revision": 4, "value": "cat"},
            ]
        )
        .columns[1]
        ._cells[0]
    ) == "a tabby cat"


def test_2_0():
    assert (
        _format_table(
            comparison_split=[
                {"base": 0, "content": True, "revision": 0, "value": "a"},
                {"base": 1, "content": False, "revision": 1, "value": " "},
                {"base": 2, "content": True, "revision": None, "value": "big"},
                {"base": None, "content": True, "revision": 2, "value": "tabby"},
                {"base": 3, "content": False, "revision": 3, "value": " "},
                {"base": 4, "content": True, "revision": 4, "value": "cat"},
            ]
        )
        .columns[2]
        ._cells[0]
    ) == "a [s red]big[/s red][u green]tabby[/u green] cat"


def test_0_1():
    assert (
        _format_table(
            comparison_split=[
                {"base": 0, "content": True, "revision": 0, "value": "a"},
                {"base": 1, "content": False, "revision": 1, "value": " "},
                {"base": 2, "content": True, "revision": None, "value": "big"},
                {"base": None, "content": True, "revision": 2, "value": "tabby"},
                {"base": 3, "content": False, "revision": 3, "value": " "},
                {"base": 4, "content": True, "revision": 4, "value": "cat"},
            ]
        )
        .columns[0]
        ._cells[1]
    ) == (
        "[b]Base length:[/b]\n"
        "3 words and 2 separators (5 total)\n"
        "\n"
        "[b]Words also in the revision:[/b]\n"
        "2 of 3 (67%)\n"
        "\n"
        "[b]Similarity:[/b]\n"
        "80% identical to the revision"
    )


def test_1_1():
    assert (
        _format_table(
            comparison_split=[
                {"base": 0, "content": True, "revision": 0, "value": "a"},
                {"base": 1, "content": False, "revision": 1, "value": " "},
                {"base": 2, "content": True, "revision": None, "value": "big"},
                {"base": None, "content": True, "revision": 2, "value": "tabby"},
                {"base": 3, "content": False, "revision": 3, "value": " "},
                {"base": 4, "content": True, "revision": 4, "value": "cat"},
            ]
        )
        .columns[1]
        ._cells[1]
    ) == (
        "[b]Revision length:[/b]\n"
        "3 words and 2 separators (5 total)\n"
        "\n"
        "[b]Words also in the base:[/b]\n"
        "2 of 3 (67%)\n"
        "\n"
        "[b]Similarity:[/b]\n"
        "80% identical to the base"
    )


def test_2_1():
    assert (
        _format_table(
            comparison_split=[
                {"base": 0, "content": True, "revision": 0, "value": "a"},
                {"base": 1, "content": False, "revision": 1, "value": " "},
                {"base": 2, "content": True, "revision": None, "value": "big"},
                {"base": None, "content": True, "revision": 2, "value": "tabby"},
                {"base": 3, "content": False, "revision": 3, "value": " "},
                {"base": 4, "content": True, "revision": 4, "value": "cat"},
            ]
        )
        .columns[2]
        ._cells[1]
    ) == (
        "[b]Identical in base and revision:[/b]\n"
        "2 words and 2 separators (4 total)\n"
        "\n"
        "[b]Removed from the base:[/b]\n"
        "1 word and 0 separators (1 total)\n"
        "\n"
        "[b]Added by the revision:[/b]\n"
        "1 word and 0 separators (1 total)"
    )
