from indifferent.indifferent import _split_text


# Fundamental combinations
def test_empty():
    assert (
        _split_text(
            text="",
        )
        == []
    )


def test_single_content():
    assert _split_text(
        text="a",
    ) == [
        {
            "value": "a",
            "content": True,
        },
    ]


def test_single_separator():
    assert _split_text(
        text=" ",
    ) == [
        {
            "value": " ",
            "content": False,
        },
    ]


def test_multiple_content():
    assert _split_text(
        text="cat",
    ) == [
        {
            "value": "cat",
            "content": True,
        },
    ]


def test_multiple_separator():
    assert _split_text(
        text=" \t.",
    ) == [
        {
            "value": " ",
            "content": False,
        },
        {
            "value": "\t",
            "content": False,
        },
        {
            "value": ".",
            "content": False,
        },
    ]


def test_single_content_single_separator():
    assert _split_text(text="a ") == [
        {
            "value": "a",
            "content": True,
        },
        {
            "value": " ",
            "content": False,
        },
    ]


def test_single_content_multiple_separator():
    assert _split_text(text="a. ") == [
        {
            "value": "a",
            "content": True,
        },
        {
            "value": ".",
            "content": False,
        },
        {
            "value": " ",
            "content": False,
        },
    ]


def test_single_separator_single_content():
    assert _split_text(text=" a") == [
        {
            "value": " ",
            "content": False,
        },
        {
            "value": "a",
            "content": True,
        },
    ]


def test_multiple_separator_single_content():
    assert _split_text(text="* a") == [
        {
            "value": "*",
            "content": False,
        },
        {
            "value": " ",
            "content": False,
        },
        {
            "value": "a",
            "content": True,
        },
    ]


def test_multiple_content_single_separator():
    assert _split_text(text="cat ") == [
        {
            "value": "cat",
            "content": True,
        },
        {
            "value": " ",
            "content": False,
        },
    ]


def test_multiple_content_multiple_separator():
    assert _split_text(text="cat. ") == [
        {
            "value": "cat",
            "content": True,
        },
        {
            "value": ".",
            "content": False,
        },
        {
            "value": " ",
            "content": False,
        },
    ]


def test_single_separator_multiple_content():
    assert _split_text(text=" cat") == [
        {
            "value": " ",
            "content": False,
        },
        {
            "value": "cat",
            "content": True,
        },
    ]


def test_multiple_separator_multiple_content():
    assert _split_text(text="* cat") == [
        {
            "value": "*",
            "content": False,
        },
        {
            "value": " ",
            "content": False,
        },
        {
            "value": "cat",
            "content": True,
        },
    ]


# Complex combinations


def test_content_separator_content():
    assert _split_text(text="a cat") == [
        {
            "value": "a",
            "content": True,
        },
        {
            "value": " ",
            "content": False,
        },
        {
            "value": "cat",
            "content": True,
        },
    ]


def test_separator_content_separator():
    assert _split_text(text=" cat.") == [
        {
            "value": " ",
            "content": False,
        },
        {
            "value": "cat",
            "content": True,
        },
        {
            "value": ".",
            "content": False,
        },
    ]


def test_line_break_separator_content():
    assert (
        _split_text(
            text="""
    cat"""
        )
        == [
            {
                "value": "\n",
                "content": False,
            },
            {
                "value": " ",
                "content": False,
            },
            {
                "value": " ",
                "content": False,
            },
            {
                "value": " ",
                "content": False,
            },
            {
                "value": " ",
                "content": False,
            },
            {
                "value": "cat",
                "content": True,
            },
        ]
    )


def test_content_line_break_separator():
    assert (
        _split_text(
            text="""cat
    """
        )
        == [
            {
                "value": "cat",
                "content": True,
            },
            {
                "value": "\n",
                "content": False,
            },
            {
                "value": " ",
                "content": False,
            },
            {
                "value": " ",
                "content": False,
            },
            {
                "value": " ",
                "content": False,
            },
            {
                "value": " ",
                "content": False,
            },
        ]
    )


def test_content_line_break_content():
    assert (
        _split_text(
            text="""a
cat"""
        )
        == [
            {
                "value": "a",
                "content": True,
            },
            {
                "value": "\n",
                "content": False,
            },
            {
                "value": "cat",
                "content": True,
            },
        ]
    )


def test_content_multiple_line_breaks_content():
    assert (
        _split_text(
            text="""a


cat"""
        )
        == [
            {
                "value": "a",
                "content": True,
            },
            {
                "value": "\n",
                "content": False,
            },
            {
                "value": "\n",
                "content": False,
            },
            {
                "value": "\n",
                "content": False,
            },
            {
                "value": "cat",
                "content": True,
            },
        ]
    )


# Type conversions
def test_int():
    assert _split_text(
        text=1,
    ) == [
        {
            "value": "1",
            "content": True,
        }
    ]


def test_float():
    assert _split_text(
        text=1.111,
    ) == [
        {
            "value": "1.111",
            "content": True,
        }
    ]
