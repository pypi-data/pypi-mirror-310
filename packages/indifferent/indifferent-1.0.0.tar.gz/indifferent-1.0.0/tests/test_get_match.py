from indifferent.indifferent import _get_match


def test_no_match(cat):

    assert (
        _get_match(
            base_item="tabby",
            revision_split=[cat],
            revision_index=0,
        )
        is None
    )


def test_content_match(a):

    assert (
        _get_match(
            base_item="a",
            revision_split=[a],
            revision_index=0,
        )
        == 0
    )


def test_separator_match(space):

    assert (
        _get_match(
            base_item=" ",
            revision_split=[space],
            revision_index=0,
        )
        == 0
    )


def test_first_base_later_revision_match(space, a, cat):

    assert (
        _get_match(
            base_item="cat",
            revision_split=[
                a,
                space,
                cat,
            ],
            revision_index=0,
        )
        == 2
    )


def test_first_base_later_revision_match_skip_first(space, a, cat):

    assert (
        _get_match(
            base_item="cat",
            revision_split=[
                cat,
                space,
                a,
                space,
                cat,
            ],
            revision_index=1,
        )
        == 4
    )
