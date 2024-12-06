# SPDX-License-Identifier: MIT


import sys  # noqa E401
from pprint import pprint  # noqa E401
import re
from talkgooder import plural
from rich.console import Console
from rich.table import Table
from string import Template
from html import escape

regex = r"\s\[\]{}\(\)<>,.:;!\?'\"`\\/\|\-_\+=%\*"


def compare(
    base: str,
    revision: str,
    base_name="",
    revision_name="",
    results="stats",
) -> dict | str | list:
    """Compare a base text against a revision to create a score and report

    Args:
        base (str):
            The base text.
        revision (str):
            The revision text.
        base_name (str):
            Optional, the name of the base text.
        revision_name (str):
            Optional, the name of the revision text.
        results (str):
            Optional, alternate formats for results:

                "stats": Raw stats without formatting, default (dict)
                "formatted_stats": Stats with descriptions (dict)
                "bbcode": Formatted stats with bbcode decorations (dict)
                "table": Formatted stats in a Rich table (str)
                "raw_table": A Rich table object (table)
                "html": A block of HTML and corresponding CSS (dict)
                "html_inline": A block of HTML with inline styles (dict)
                "html_page": A full page of HTMl with corresponding CSS (dict)
                "html_page_internal": A full page of HTML with styles in the head (dict)
                "html_page_inline": A full page of HTML with inline styles (dict)
                "raw": The raw analysis of the match (list)

    Returns:
        (dict | str | list)

    Raises:
        ValueError: Not a valid format: `results`
    """

    base_split = _split_text(
        text=base,
        regex=regex,
    )

    revision_split = _split_text(
        text=revision,
        regex=regex,
    )

    comparison_split = _base_revision_comparison(
        base_split=base_split,
        revision_split=revision_split,
    )

    # pprint(comparison_split)

    if results.lower() == "stats":
        return _stats(comparison_split)

    elif results.lower() == "formatted_stats":
        return _format_stats(_stats(comparison_split))

    elif results.lower() == "bbcode":
        return _format_bbcode(comparison_split)

    elif results.lower() == "table":
        console = Console()
        with console.capture() as capture:
            console.print(
                _format_table(
                    comparison_split=comparison_split,
                    base_name=base_name,
                    revision_name=revision_name,
                )
            )

        return capture.get()

    elif results.lower() == "raw_table":
        return _format_table(
            comparison_split=comparison_split,
            base_name=base_name,
            revision_name=revision_name,
        )

    elif results.lower() == "html":
        return _format_html(
            comparison_split=comparison_split,
            base_name=base_name,
            revision_name=revision_name,
        )

    elif results.lower() == "html_inline":
        return _format_html(
            comparison_split=comparison_split,
            inline=True,
            base_name=base_name,
            revision_name=revision_name,
        )

    elif results.lower() == "html_page":
        return _format_html(
            comparison_split=comparison_split,
            page=True,
            base_name=base_name,
            revision_name=revision_name,
        )

    elif results.lower() == "html_page_internal":
        return _format_html(
            comparison_split=comparison_split,
            page=True,
            internal=True,
            base_name=base_name,
            revision_name=revision_name,
        )

    elif results.lower() == "html_page_inline":
        return _format_html(
            comparison_split=comparison_split,
            page=True,
            inline=True,
            base_name=base_name,
            revision_name=revision_name,
        )

    elif results.lower() == "raw":
        return comparison_split

    else:
        raise ValueError("Not a valid format: %s" % results)


def _split_text(
    *,
    text: str | int | float,
    regex=regex,
) -> list:
    """Split text using the provided regex to identify separators between content.

    Args:
        text (string):
            The text to be split.
        regex (string):
            Optional, a replacement regex to identify separators between content.

    Returns:
        list ([{"value": string, "content": boolean}, ...]):
            Values from the text and whether they are content.

    Raises:
        TypeError: Text must be a string, int, or float.
    """

    # Check the type
    if not isinstance(text, (str, int, float)):
        raise TypeError("text must be a string, int, or float")

    # Return a content string if the text is an int or float
    if isinstance(text, (int, float)):
        return [
            {
                "value": str(text),
                "content": True,
            }
        ]

    # Return an empty list if there's no text
    if not len(text):
        return []

    separator_pattern = re.compile("^[%s]" % regex)
    content_pattern = re.compile("^[^%s]+" % regex)
    split_text = []

    # Nibble away at the text one chunk at a time
    while len(text):

        separator_found = separator_pattern.findall(text)
        content_found = content_pattern.findall(text)

        if len(separator_found):
            # A separator was found
            split_text.append(
                {
                    "value": separator_found[0],
                    "content": False,
                }
            )

            # Trim the separator from the start of text
            text = text[len(separator_found[0]) :]  # noqa E203

        elif len(content_found):
            # Content was found
            split_text.append(
                {
                    "value": content_found[0],
                    "content": True,
                }
            )

            # Trim the content from the start of text
            text = text[len(content_found[0]) :]  # noqa E203

    return split_text


def _get_match(
    *,
    base_item: str,
    revision_split: str,
    revision_index: int,
) -> dict:
    """Find the index of the next content match, if any.

    Args:
        base_item (str):
            A string containing a base item value.
        revision_split (list):
            A list containing the split revision string.
        revision_index (int):
            Index of revision list to begin search.

    Returns:
        return (int | None):
            Index of next match, if it exists.

    Raises:
        ValueError: Revision index is out of range.
    """
    # If there's no revision, there's nothing to match
    if not len(revision_split):
        return None

    if revision_index >= len(revision_split) or revision_index < 0:
        raise ValueError(
            "Revision index is out of range (index: %s, length: %s)"
            % (revision_index, len(revision_split)),
        )

    # Find the next matching instance, if there is one
    next_match = next(
        (
            i
            for i, item in enumerate(revision_split[revision_index:])
            if item["value"] == base_item
        ),
        None,
    )

    if next_match:
        # If a match was found, return the absolute index of the revision item
        return next_match + revision_index

    else:
        return next_match


def _backfill(
    *,
    base_split: list,
    revision_split: list,
    base_last_match: int | None,
    base_index: int,
    revision_last_match: int | None,
    revision_index: int,
) -> list:
    """Backfill any unmatched base and revision items.

    Args:
        base_split (list):
            A list containing the split base string.
        revision_split (list):
            A list containing the split revision string.
        base_last_match (int):
            The index of the last matching content in the base, if it exists.
        base_index (int):
            The index of the current matching content in the base.
        revision_last_match (int | None):
            The index of the last matching content in the revision, if it exists.
        revision_index (int):
            The index of the current matching content in the revision.

    Returns:
        list [{"base": int, "content": boolean, "revision": int, "value": str,} ...]
    """  # noqa E501

    backfill = []
    backfill_index = 0

    if base_last_match is None:
        base_start = 0
    elif base_last_match == 0:
        base_start = 1
    else:
        base_start = base_last_match + 1

    if revision_last_match is None:
        revision_start = 0
    elif revision_last_match == 0:
        revision_start = 1
    else:
        revision_start = revision_last_match + 1

    # Extract the backfill lists
    backfill_base = base_split[base_start:base_index]
    backfill_revision = revision_split[revision_start:revision_index]

    if not len(backfill_base) and not len(backfill_revision):
        # If this is the first item in both lists there's nothing to backfill
        return backfill

    elif not len(backfill_base):

        # If there's no base to backfill, add all of the revision backfill items
        for item in backfill_revision:
            backfill.append(
                {
                    "value": item["value"],
                    "content": item["content"],
                    "base": None,
                    "revision": revision_start + backfill_index,
                },
            )
            backfill_index += 1
        return backfill

    elif not len(backfill_revision):
        # If there's no revision to backfill, add all of the base backfill items

        for item in backfill_base:
            backfill.append(
                {
                    "value": item["value"],
                    "content": item["content"],
                    "base": base_start + backfill_index,
                    "revision": None,
                },
            )

            backfill_index += 1
        return backfill

    else:
        # If there's something in both, look for common separators at the start, then look at the
        # end, then handle anything left over as an addition or removal.

        # First, count any separators that match at the start
        matches_start = 0
        for index in range(0, min(len(backfill_base), len(backfill_revision))):

            if backfill_base[index] == backfill_revision[index]:

                # Add the matching item to the backfill
                backfill.append(
                    {
                        "value": backfill_base[index]["value"],
                        "content": backfill_base[index]["content"],
                        "base": base_start + index,
                        "revision": revision_start + index,
                    },
                )

                # Record how many start items match
                matches_start += 1

            else:
                # Stop checking if there's no match
                break

        # Check if anything was uncounted after matching the start
        possible_matches_end_base = len(backfill_base) - matches_start
        possible_matches_end_revision = len(backfill_revision) - matches_start

        backfill_end = []

        # If uncounted items remain in both, count any separators that match at the end
        matches_end = 0
        if possible_matches_end_base and possible_matches_end_revision:

            # Check if there are any common
            for index in range(
                0, min(possible_matches_end_base, possible_matches_end_revision)
            ):

                # Walk backwards from the end of each list of backfills
                if (
                    backfill_base[len(backfill_base) - index - 1]
                    == backfill_revision[len(backfill_revision) - index - 1]
                ):

                    # Stash the ending items separately
                    backfill_end.insert(
                        0,
                        {
                            "value": backfill_base[len(backfill_base) - 1 - index][
                                "value"
                            ],
                            "content": backfill_base[len(backfill_base) - 1 - index][
                                "content"
                            ],
                            "base": base_start + len(backfill_base) - 1 - index,
                            "revision": revision_start
                            + len(backfill_revision)
                            - 1
                            - index,
                        },
                    )

                    # Record how many end items match
                    matches_end += 1

                else:
                    # Stop checking if there's no match
                    break

        # Assemble the backfill, starting with removed items
        backfill_base_index = 0

        for item in backfill_base[matches_start : len(backfill_base) - matches_end]:
            backfill.append(
                {
                    "value": item["value"],
                    "content": item["content"],
                    "base": base_start + matches_start + backfill_base_index,
                    "revision": None,
                },
            )

            backfill_base_index += 1

        # Next the added items
        backfill_revision_index = 0

        for item in backfill_revision[
            matches_start : len(backfill_revision) - matches_end
        ]:

            backfill.append(
                {
                    "value": item["value"],
                    "content": item["content"],
                    "base": None,
                    "revision": revision_start
                    + matches_start
                    + backfill_revision_index,
                },
            )

            backfill_revision_index += 1

        # Finally combine it all together
        return backfill + backfill_end


def _forward_fill(
    *,
    base_split,
    revision_split,
    base_last_match,
    revision_last_match,
):
    """Fill any unmatched separators after the last match

    Args:
        base_split (list):
            A list containing the split base string.
        revision_split (list):
            A list containing the split revision string.
        base_last_match (int):
            The index of the last matching content in the base, if it exists.
        revision_last_match (int | None):
            The index of the last matching content in the revision, if it exists.

    Returns:
        list [{"base": int, "content": boolean, "revision": int, "value": str,} ...]
    """  # noqa E501

    leader = []
    fill = []
    terminator = []

    # Determine if any base items remain
    if base_last_match is None:
        base_fill_start = 0
    else:
        base_fill_start = base_last_match + 1

    base_terminal_index = len(base_split)

    # Determine if any revision items remain
    if revision_last_match is None:
        revision_fill_start = 0
    else:
        revision_fill_start = revision_last_match + 1

    revision_terminal_index = len(revision_split)

    # Walk forward from the beginning looking for separator matches
    for terminal_index in range(
        0,
        min(
            base_terminal_index - base_fill_start,
            revision_terminal_index - revision_fill_start,
        ),
    ):

        if (
            base_split[base_fill_start + terminal_index]
            == revision_split[revision_fill_start + terminal_index]
        ):

            leader.append(
                {
                    "value": base_split[base_fill_start + terminal_index]["value"],
                    "content": base_split[base_fill_start + terminal_index]["content"],
                    "base": base_fill_start + terminal_index,
                    "revision": revision_fill_start + terminal_index,
                },
            )

        else:
            break

    # Offset starts by amount of leading matches found
    base_fill_start += len(leader)
    revision_fill_start += len(leader)

    # Walk backwards from the end looking for separator matches
    for terminal_index in range(
        0,
        min(
            base_terminal_index - base_fill_start,
            revision_terminal_index - revision_fill_start,
        ),
    ):
        if (
            base_split[len(base_split) - 1 - terminal_index]
            == revision_split[len(revision_split) - 1 - terminal_index]
        ):

            terminator.insert(
                0,
                {
                    "value": base_split[len(base_split) - 1 - terminal_index]["value"],
                    "content": base_split[len(base_split) - 1 - terminal_index][
                        "content"
                    ],
                    "base": len(base_split) - 1 - terminal_index,
                    "revision": len(revision_split) - 1 - terminal_index,
                },
            )

            base_terminal_index -= 1
            revision_terminal_index -= 1

    # Any remaining bases are removals
    for base_fill_index in range(base_fill_start, base_terminal_index):

        fill.append(
            {
                "value": base_split[base_fill_index]["value"],
                "content": base_split[base_fill_index]["content"],
                "base": base_fill_index,
                "revision": None,
            },
        )

    # Any remaining revisions are additions
    for revision_fill_index in range(revision_fill_start, revision_terminal_index):
        fill.append(
            {
                "value": revision_split[revision_fill_index]["value"],
                "content": revision_split[revision_fill_index]["content"],
                "base": None,
                "revision": revision_fill_index,
            },
        )

    return leader + fill + terminator


def _base_revision_comparison(
    *,
    base_split: list,
    revision_split: list,
) -> list:
    """Compare the base against the revision.

    Args:
        base_split (list):
            A list containing the split base string.
        revision_split (list):
            A list containing the split revision string.

    Returns:
        list [{"base": int, "revision": int, "content": bool, "value": "str"}, ...]
    """  # noqa E501

    match = []
    base_index = 0
    base_last_match = None
    revision_index = 0
    revision_last_match = None

    for base_item in base_split:

        # If there's nothing in the revision, skip any comparisons
        if not len(revision_split):
            break

        # If there's base content only compare content, separators will be backfilled
        if (
            True in [item["content"] for item in base_split]
            and not base_item["content"]
        ):
            base_index += 1
            continue

        # Set an addressable value for last match, if it hasn't been matched yet
        if revision_last_match is None:
            revision_index_start = 0
        else:
            # Check if any revision items remain
            if revision_last_match + 1 < len(revision_split):
                # Start at the next revision index
                revision_index_start = revision_last_match + 1

            else:
                # No revision items remain, move to the end
                base_index += 1
                break

        # Find the next item in the revision that matches the base
        revision_index = _get_match(
            base_item=base_item["value"],
            revision_split=revision_split,
            revision_index=revision_index_start,
        )

        # If there's no match, continue
        if revision_index is None:
            base_index += 1
            continue

        # Check if anything needs to be backfilled
        match += _backfill(
            base_split=base_split,
            revision_split=revision_split,
            base_index=base_index,
            base_last_match=base_last_match,
            revision_index=revision_index,
            revision_last_match=revision_last_match,
        )

        match.append(
            {
                "value": base_split[base_index]["value"],
                "content": base_split[base_index]["content"],
                "base": base_index,
                "revision": revision_index,
            }
        )

        base_last_match = base_index
        revision_last_match = revision_index

        base_index += 1

    # Forward fill any remaining items
    fill = _forward_fill(
        base_split=base_split,
        revision_split=revision_split,
        base_last_match=base_last_match,
        revision_last_match=revision_last_match,
    )

    return match + fill


def _stats(
    comparison_split: list,
) -> dict:
    """Calculate statistics of the match

    Args:
        comparison (list):
            A list of dicts with the analysis results

    returns:
        dict:
            Stats in raw form
    """

    added_length_content = len(
        [
            item
            for item in comparison_split
            if item["base"] is None and item["revision"] is not None and item["content"]
        ]
    )

    added_length_total = len(
        [
            item
            for item in comparison_split
            if item["base"] is None and item["revision"] is not None
        ]
    )

    removed_length_content = len(
        [
            item
            for item in comparison_split
            if item["base"] is not None and item["revision"] is None and item["content"]
        ]
    )

    removed_length_total = len(
        [
            item
            for item in comparison_split
            if item["base"] is not None and item["revision"] is None
        ]
    )

    base_length_content = len(
        [
            item
            for item in comparison_split
            if item["base"] is not None and item["content"]
        ]
    )

    base_length_total = len(
        [item for item in comparison_split if item["base"] is not None]
    )

    revision_length_content = len(
        [
            item
            for item in comparison_split
            if item["revision"] is not None and item["content"]
        ]
    )

    revision_length_total = len(
        [item for item in comparison_split if item["revision"] is not None]
    )

    match_length_content = len(
        [
            item
            for item in comparison_split
            if item["base"] is not None
            and item["revision"] is not None
            and item["content"]
        ]
    )

    match_length_total = len(
        [
            item
            for item in comparison_split
            if item["base"] is not None and item["revision"] is not None
        ]
    )

    return {
        "inputs": {
            "base": {
                "length": {
                    "content": base_length_content,
                    "total": base_length_total,
                },
            },
            "revision": {
                "length": {
                    "content": revision_length_content,
                    "total": revision_length_total,
                },
            },
        },
        "results": {
            "added": {
                "length": {
                    "content": added_length_content,
                    "total": added_length_total,
                },
            },
            "removed": {
                "length": {
                    "content": removed_length_content,
                    "total": removed_length_total,
                },
            },
            "matched": {
                "length": {
                    "content": match_length_content,
                    "total": match_length_total,
                },
                "base_preserved": {
                    "total": (base_length_total)
                    and ((match_length_total) / (base_length_total))
                    or 0,
                    "content": base_length_content
                    and (match_length_content / base_length_content)
                    or 0,
                },
                "revision_matched": {
                    "total": (revision_length_total)
                    and ((match_length_total) / (revision_length_total))
                    or 0,
                    "content": revision_length_content
                    and (match_length_content / revision_length_content)
                    or 0,
                },
            },
        },
        "score": {  # Score is (match) / (match + difference)
            "total": (
                (match_length_total + removed_length_total + added_length_total)
                and (match_length_total)
                / (match_length_total + removed_length_total + added_length_total)
                or 0
            ),
            "content": (
                (match_length_content + removed_length_content + added_length_content)
                and match_length_content
                / (match_length_content + removed_length_content + added_length_content)
                or 0
            ),
        },
    }


def _format_stats(
    stats: dict,
) -> dict:
    """Explain the results in a format more conducive to humans

    Args:
        stats (dict):
            A dict with the output of the _stats function.

    Returns:
        dict:
            Stats in human-readable formats, with explanations
    """

    return {
        "summary": "%s%% match" % round(stats["score"]["content"] * 100),
        "base": [
            {
                "label": "Base length",
                "value": "%s %s and %s %s (%s total)"
                % (
                    stats["inputs"]["base"]["length"]["content"],
                    plural("word", stats["inputs"]["base"]["length"]["content"]),
                    stats["inputs"]["base"]["length"]["total"]
                    - stats["inputs"]["base"]["length"]["content"],
                    plural(
                        "separator",
                        stats["inputs"]["base"]["length"]["total"]
                        - stats["inputs"]["base"]["length"]["content"],
                    ),
                    stats["inputs"]["base"]["length"]["total"],
                ),
            },
            {
                "label": "Words also in the revision",
                "value": "%s of %s (%s%%)"
                % (
                    stats["results"]["matched"]["length"]["content"],
                    stats["inputs"]["base"]["length"]["content"],
                    round(
                        stats["results"]["matched"]["base_preserved"]["content"] * 100
                    ),
                ),
            },
            {
                "label": "Similarity",
                "value": "%s%% identical to the revision"
                % (
                    round(stats["results"]["matched"]["base_preserved"]["total"] * 100),
                ),
            },
        ],
        "revision": [
            {
                "label": "Revision length",
                "value": "%s %s and %s %s (%s total)"
                % (
                    stats["inputs"]["revision"]["length"]["content"],
                    plural("word", stats["inputs"]["revision"]["length"]["content"]),
                    stats["inputs"]["revision"]["length"]["total"]
                    - stats["inputs"]["revision"]["length"]["content"],
                    plural(
                        "separator",
                        stats["inputs"]["revision"]["length"]["total"]
                        - stats["inputs"]["revision"]["length"]["content"],
                    ),
                    stats["inputs"]["revision"]["length"]["total"],
                ),
            },
            {
                "label": "Words also in the base",
                "value": "%s of %s (%s%%)"
                % (
                    stats["results"]["matched"]["length"]["content"],
                    stats["inputs"]["revision"]["length"]["content"],
                    round(
                        stats["results"]["matched"]["revision_matched"]["content"] * 100
                    ),
                ),
            },
            {
                "label": "Similarity",
                "value": "%s%% identical to the base"
                % (
                    round(
                        stats["results"]["matched"]["revision_matched"]["total"] * 100
                    ),
                ),
            },
        ],
        "matched": [
            {
                "label": "Identical in base and revision",
                "value": "%s %s and %s %s (%s total)"
                % (
                    stats["results"]["matched"]["length"]["content"],
                    plural("word", stats["results"]["matched"]["length"]["content"]),
                    stats["results"]["matched"]["length"]["total"]
                    - stats["results"]["matched"]["length"]["content"],
                    plural(
                        "separator",
                        stats["results"]["matched"]["length"]["total"]
                        - stats["results"]["matched"]["length"]["content"],
                    ),
                    stats["results"]["matched"]["length"]["total"],
                ),
            },
            {
                "label": "Removed from the base",
                "value": "%s %s and %s %s (%s total)"
                % (
                    stats["results"]["removed"]["length"]["content"],
                    plural("word", stats["results"]["removed"]["length"]["content"]),
                    stats["results"]["removed"]["length"]["total"]
                    - stats["results"]["removed"]["length"]["content"],
                    plural(
                        "separator",
                        stats["results"]["removed"]["length"]["total"]
                        - stats["results"]["removed"]["length"]["content"],
                    ),
                    stats["results"]["removed"]["length"]["total"],
                ),
            },
            {
                "label": "Added by the revision",
                "value": "%s %s and %s %s (%s total)"
                % (
                    stats["results"]["added"]["length"]["content"],
                    plural("word", stats["results"]["added"]["length"]["content"]),
                    stats["results"]["added"]["length"]["total"]
                    - stats["results"]["added"]["length"]["content"],
                    plural(
                        "separator",
                        stats["results"]["added"]["length"]["total"]
                        - stats["results"]["added"]["length"]["content"],
                    ),
                    stats["results"]["added"]["length"]["total"],
                ),
            },
        ],
    }


def _format_bbcode(
    comparison_split: list,
) -> dict:
    """Format the matched results using BBCode

    Args:
        comparison_split (list):
            The results of the analysis

    Returns:
        dict:
            Analysis results reformatted as BBCode
    """

    formatted_stats = _format_stats(_stats(comparison_split))

    # Assemble the text of matching words and separators
    matched = ""
    for item in comparison_split:

        # Reveal invisible characters
        reveal = ""
        if item["value"] == "\t":
            reveal = "   ⇥"
        elif item["value"] == "\n":
            reveal = "↲\n"

        if item["base"] is not None and item["revision"] is None:

            if not reveal:
                reveal = item["value"]

            matched += "[s red]%s[/s red]" % reveal

        elif item["base"] is None and item["revision"] is not None:

            if not reveal:
                reveal = item["value"]

            matched += "[u green]%s[/u green]" % reveal
        else:
            matched += item["value"]

    return {
        "summary": formatted_stats["summary"],
        "matched": matched,
        "analysis": {
            "base": "\n\n".join(
                [
                    "[b]%s:[/b]\n%s" % (item["label"], item["value"])
                    for item in formatted_stats["base"]
                ]
            ),
            "matched": "\n\n".join(
                [
                    "[b]%s:[/b]\n%s" % (item["label"], item["value"])
                    for item in formatted_stats["matched"]
                ]
            ),
            "revision": "\n\n".join(
                [
                    "[b]%s:[/b]\n%s" % (item["label"], item["value"])
                    for item in formatted_stats["revision"]
                ]
            ),
        },
    }


def _format_table(
    *,
    comparison_split: list,
    base_name="",
    revision_name="",
):
    """Create summary tables that can be printed to the console

    Args:
        comparison_split (list):
            The results of the analysis
        base_name (str):
            Optional name for the base text
        revision_name (str):
            Optional name for the revision text

    return:
        table:
            rich.table.Table object with a formatted table
    """

    # Get BBCode-formatted results
    bbcode_results = _format_bbcode(comparison_split)

    # Create the diff table
    diff_table = Table(
        show_header=True,
        header_style="bold cyan",
        show_lines=True,
    )

    # Add titles to base and revision
    base_title = ""
    if base_name:
        base_title = ": %s" % base_name

    revision_title = ""
    if revision_name:
        revision_title = ": %s" % revision_name

    diff_table.add_column("Base%s" % base_title, ratio=1, min_width=10, vertical="top")
    diff_table.add_column(
        "Revision%s" % revision_title, ratio=1, min_width=10, vertical="top"
    )
    diff_table.add_column(
        "Comparison: %s" % bbcode_results["summary"],
        ratio=1,
        min_width=10,
        vertical="top",
    )

    diff_table.add_row(
        "".join(
            [item["value"] for item in comparison_split if item["base"] is not None]
        ),
        "".join(
            [item["value"] for item in comparison_split if item["revision"] is not None]
        ),
        bbcode_results["matched"],
    )

    diff_table.add_row(
        bbcode_results["analysis"]["base"],
        bbcode_results["analysis"]["revision"],
        bbcode_results["analysis"]["matched"],
    )

    return diff_table


def _safe_html(
    text: str,
) -> str:
    """Shake some of the gremlins out of text so it renders properly

    Args:
        text (str):
            Text to be escaped

    Returns:
        str:
            Escaped text that will render safely in HTML

    Raises:
        TypeError: Text must be a string.
    """

    # Check the type
    if not isinstance(text, str):
        raise TypeError("text must be a string")

    # Escape existing characters with special meaning in HTML
    text = escape(text)

    # Convert line breaks to HTML breaks
    text = text.replace("\n", "<br />")

    # Convert tabs to explicit spaces
    text = text.replace("\t", "&nbsp;&nbsp;&nbsp;&nbsp;")

    return text


def _format_html(
    *,
    comparison_split: list,
    page=False,
    inline=False,
    internal=False,
    heading_level=1,
    base_name="",
    revision_name="Revision",
) -> dict:
    """Create an HTML-formatted report

    Args:
        comparison_split (list):
            The result of the initial analysis.
        page (bool):
            If True, return a full page instead of a snippet.
        inline (bool):
            If True, render styles directly inline in the document.
        internal (bool):
            If True, render styles in the <head> of the document.
        heading_level (int):
            The highest heading level.
        base_name (str):
            Optional name for the base text
        revision_name (str):
            Optional name for the revision text

    Returns:
        dict:
            HTML and CSS
    """

    stats = _stats(comparison_split)
    formatted_stats = _format_stats(stats)

    # Add the base and revision and match reports
    html_output = {
        "summary": formatted_stats["summary"],
        "match_summary": "\n                ".join(
            [
                "<li><strong>%s:</strong> %s</li>" % (item["label"], item["value"])
                for item in formatted_stats["matched"]
            ]
        ),
        "base_summary": "\n                ".join(
            [
                "<li><strong>%s:</strong> %s</li>" % (item["label"], item["value"])
                for item in formatted_stats["base"]
            ]
        ),
        "base_detail": _safe_html(
            "".join(
                [item["value"] for item in comparison_split if item["base"] is not None]
            )
        ),
        "revision_summary": "\n                ".join(
            [
                "<li><strong>%s:</strong> %s</li>" % (item["label"], item["value"])
                for item in formatted_stats["revision"]
            ]
        ),
        "revision_detail": _safe_html(
            "".join(
                [
                    item["value"]
                    for item in comparison_split
                    if item["revision"] is not None
                ]
            )
        ),
    }

    # Set the heading levels
    if page or heading_level != 1:
        html_output["heading_level"] = heading_level
        html_output["subheading_level"] = heading_level + 1

    else:
        # If not a page, the title should not be H1
        html_output["heading_level"] = 2
        html_output["subheading_level"] = 3

    # Set base name and title, if they exist
    if base_name:
        html_output["base_name"] = base_name
        html_output["base_title"] = "Base: %s" % base_name

    else:
        html_output["base_name"] = html_output["base_title"] = "Base"

    # Set revision name and title, if they exist
    if revision_name:
        html_output["revision_name"] = revision_name
        html_output["revision_title"] = "Revision: %s" % revision_name

    else:
        html_output["revision_name"] = html_output["revision_title"] = "Revision"

    head_template = """<!doctype html>
<html lang="en-US">
<head>
<meta charset="utf-8" />
<title>Comparison of $base_name and $revision_name</title>
$head_css</head>
<body class="page"$style_page_inline>
"""

    body_template = """<!-- Comparison generated by Indifferent: https://github.com/brianwarner/indifferent -->
<div class="indifferent"$style_indifferent_inline>
    <h$heading_level$style_title_inline class="title">$base_name<br /><span class="vs"$style_vs_inline>vs.</span><br />$revision_name</h$heading_level>
    <h$subheading_level$style_subtitle_inline class="subtitle">$summary</h$subheading_level>
    <div class="nav-links">
        <table$style_nav_links_table_inline>
            <tr>
                <td$style_nav_links_td_inline><a href="#indifferent.base"$style_nav_links_a_inline>Base</a></td>
                <td$style_nav_links_td_inline><a href="#indifferent.revision"$style_nav_links_a_inline>Revision</a></td>
                <td$style_nav_links_td_last_inline class="last"><a href="#indifferent.match"$style_nav_links_a_inline>Comparison</a></td>
            </tr>
        </table>
    </div>
    <div class="section base"$style_section_inline>
        <a id="indifferent.base"></a>
        <h$subheading_level$style_subheading_inline>$base_title</h$subheading_level>
        <div class="summary">
            <ul>
                $base_summary
            </ul>
        </div>
        <div class="detail"$style_detail_inline>
            $base_detail
        </div>
    </div>
    <div class="section revision"$style_section_inline>
        <a id="indifferent.revision"></a>
        <h$subheading_level$style_subheading_inline>$revision_title</h$subheading_level>
        <div class="summary">
            <ul>
                $revision_summary
            </ul>
        </div>
        <div class="detail"$style_detail_inline>
            $revision_detail
        </div>
    </div>
    <div class="section match"$style_section_inline>
        <a id="indifferent.match"></a>
        <h$subheading_level$style_subheading_inline>Comparison: $summary</h$subheading_level>
        <div class="summary">
            <ul>
                $match_summary
        </div>
        <div class="detail"$style_detail_inline>
            $match_detail
        </div>
    </div>
</div>"""  # noqa E501

    tail_template = """
</body>
</html>"""

    # Only include .page if returning a page
    if page:
        css_template = """   .page {
        $style_page
    }

"""
    else:
        css_template = ""

    css_template += """    .indifferent {
        $style_indifferent
    }

    .indifferent h$heading_level.title {
        $style_title
    }

    .indifferent h$heading_level.title .vs {
        $style_vs
    }

    .indifferent h$subheading_level.subtitle {
        $style_subtitle
    }

    .indifferent .nav-links table {
        $style_nav_links_table
    }

    .indifferent .nav-links td {
        $style_nav_links_td
    }

    .indifferent .nav-links td.last {
        $style_nav_links_td_last
    }

    .indifferent .nav-links a {
        $style_nav_links_a
    }

    .indifferent .section h$subheading_level {
        $style_subheading
    }

    .indifferent .section {
        $style_section
    }

    .indifferent .detail {
        $style_detail
    }

    .indifferent .matched {
        $style_matched
    }

    .indifferent .added {
        $style_added
    }

    .indifferent .deleted {
        $style_deleted
    }
"""

    # Define the styles
    style_definitions = {
        "page": "background-color: #DDD; font-family: sans-serif;",
        "indifferent": "max-width: 900px; min-width: 800px; margin: 0 auto; background-color: #FFF; padding: 30px 20px; color: #333;",  # noqa E501
        "section": "padding: 20px 0px;",
        "title": "text-align: center;",
        "vs": "font-size: 70%; color: #333;",
        "subtitle": "border-bottom: none; text-align: center; color: #555;",
        "nav_links_table": "margin: 40px auto 0px;",
        "nav_links_td": "border-right: 1px #888 solid;",
        "nav_links_td_last": "border-right: 0px;",
        "nav_links_a": "color: #333; padding: 5px 10px; text-decoration: none;",
        "subheading": (
            "padding-bottom: 10px; margin: 20px 0px 0px; border-bottom: 1px solid grey;"
        ),
        "detail": (
            "margin: 10px; padding: 15px; border: 1px solid #DDD; font-family: monospace;"
        ),
        "matched": "background-color: #DEDEDE; margin: 0px 1px;",
        "added": (
            "color: green; text-decoration: underline; font-weight: bold; margin: 0px 1px"
        ),
        "deleted": "color: red; text-decoration: line-through; margin: 0px 1px;",
    }

    # Format styles for inline or internal/external
    for style in style_definitions.keys():
        if inline:
            # Inline styles are embedded directly into tags
            html_output["style_%s_inline" % style] = (
                ' style="%s"' % style_definitions[style]
            )
            html_output["style_%s" % style] = ""
        else:
            # Internal/external styles are more readable when separated by line breaks
            html_output["style_%s_inline" % style] = ""
            html_output["style_%s" % style] = style_definitions[style].replace(
                "; ", ";\n        "
            )

    # Assemble the match for display
    html_output["match_detail"] = ""
    for item in comparison_split:

        # Reveal specific invisible characters, otherwise escape the item
        if item["value"] == "\t":
            display = "&nbsp;&nbsp;&nbsp;&RightArrowBar;"

        elif item["value"] == "\n":
            display = "&ldsh;<br />"

        else:
            display = _safe_html(item["value"])

        if item["base"] is not None and item["revision"] is None:
            html_output["match_detail"] += '<span class="deleted"%s>%s</span>' % (
                html_output["style_deleted_inline"],
                display,
            )

        elif item["base"] is None and item["revision"] is not None:
            html_output["match_detail"] += '<span class="added"%s>%s</span>' % (
                html_output["style_added_inline"],
                display,
            )

        else:
            html_output["match_detail"] += '<span class="matched"%s>%s</span>' % (
                html_output["style_matched_inline"],
                display,
            )

    # Assemble CSS
    if inline:
        # Don't return CSS if using inline styles
        html_output["head_css"] = ""
        external_css = ""

    elif internal:
        # If using internal styles, add CSS to head
        html_output["head_css"] = "<style>\n%s</style>\n" % Template(
            css_template
        ).substitute(html_output)
        external_css = ""

    else:
        # If using external styles, return CSS
        html_output["head_css"] = '<link rel="stylesheet" href="indifferent.css">\n'
        external_css = Template(css_template).substitute(html_output)

    # Assemble templates and return
    if page:
        return {
            "html": Template(head_template).substitute(html_output)
            + Template(body_template).substitute(html_output)
            + tail_template,
            "css": external_css,
        }

    else:
        return {
            "html": Template(body_template).substitute(html_output),
            "css": external_css,
        }
