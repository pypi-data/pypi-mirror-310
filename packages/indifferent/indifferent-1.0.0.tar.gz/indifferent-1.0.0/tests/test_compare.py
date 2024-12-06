from indifferent.indifferent import compare


def test_empty():
    assert compare(base="", revision="") == {
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


def test_base_empty():
    assert compare(base="", revision="a tabby cat") == {
        "inputs": {
            "base": {"length": {"content": 0, "total": 0}},
            "revision": {"length": {"content": 3, "total": 5}},
        },
        "results": {
            "added": {"length": {"content": 3, "total": 5}},
            "matched": {
                "base_preserved": {"content": 0, "total": 0},
                "length": {"content": 0, "total": 0},
                "revision_matched": {"content": 0, "total": 0},
            },
            "removed": {"length": {"content": 0, "total": 0}},
        },
        "score": {"content": 0, "total": 0},
    }


def test_revision_empty():
    assert compare(
        base="a tabby cat",
        revision="",
    ) == {
        "inputs": {
            "base": {"length": {"content": 3, "total": 5}},
            "revision": {"length": {"content": 0, "total": 0}},
        },
        "results": {
            "added": {"length": {"content": 0, "total": 0}},
            "matched": {
                "base_preserved": {"content": 0, "total": 0},
                "length": {"content": 0, "total": 0},
                "revision_matched": {"content": 0, "total": 0},
            },
            "removed": {"length": {"content": 3, "total": 5}},
        },
        "score": {"content": 0, "total": 0},
    }


def test_match():
    assert compare(
        base="a tabby cat",
        revision="a tabby cat",
    ) == {
        "inputs": {
            "base": {"length": {"content": 3, "total": 5}},
            "revision": {"length": {"content": 3, "total": 5}},
        },
        "results": {
            "added": {"length": {"content": 0, "total": 0}},
            "matched": {
                "base_preserved": {"content": 1.0, "total": 1.0},
                "length": {"content": 3, "total": 5},
                "revision_matched": {"content": 1.0, "total": 1.0},
            },
            "removed": {"length": {"content": 0, "total": 0}},
        },
        "score": {"content": 1.0, "total": 1.0},
    }


def test_content_match():
    assert compare(
        base="cat",
        revision="cat",
    ) == {
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


def test_content_no_match():
    assert compare(
        base="cat",
        revision="tabby",
    ) == {
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


def test_content_partial_match_base_removal():
    assert compare(
        base="a tabby cat",
        revision="a cat",
    ) == {
        "inputs": {
            "base": {"length": {"content": 3, "total": 5}},
            "revision": {"length": {"content": 2, "total": 3}},
        },
        "results": {
            "added": {"length": {"content": 0, "total": 0}},
            "matched": {
                "base_preserved": {"content": 0.6666666666666666, "total": 0.6},
                "length": {"content": 2, "total": 3},
                "revision_matched": {"content": 1.0, "total": 1.0},
            },
            "removed": {"length": {"content": 1, "total": 2}},
        },
        "score": {"content": 0.6666666666666666, "total": 0.6},
    }


def test_content_partial_match_revision_removal():
    assert compare(
        base="a cat",
        revision="a tabby cat",
    ) == {
        "inputs": {
            "base": {"length": {"content": 2, "total": 3}},
            "revision": {"length": {"content": 3, "total": 5}},
        },
        "results": {
            "added": {"length": {"content": 1, "total": 2}},
            "matched": {
                "base_preserved": {"content": 1.0, "total": 1.0},
                "length": {"content": 2, "total": 3},
                "revision_matched": {"content": 0.6666666666666666, "total": 0.6},
            },
            "removed": {"length": {"content": 0, "total": 0}},
        },
        "score": {"content": 0.6666666666666666, "total": 0.6},
    }


def test_separator_match():
    assert compare(base=" ", revision=" ") == {
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


def test_separator_no_match():
    assert compare(base=" ", revision="\t") == {
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


def test_separator_partial_match_base_removal():
    assert compare(base=" ", revision="  ") == {
        "inputs": {
            "base": {"length": {"content": 0, "total": 1}},
            "revision": {"length": {"content": 0, "total": 2}},
        },
        "results": {
            "added": {"length": {"content": 0, "total": 1}},
            "matched": {
                "base_preserved": {"content": 0, "total": 1.0},
                "length": {"content": 0, "total": 1},
                "revision_matched": {"content": 0, "total": 0.5},
            },
            "removed": {"length": {"content": 0, "total": 0}},
        },
        "score": {"content": 0, "total": 0.5},
    }


def test_separator_partial_match_revision_removal():
    assert compare(base="  ", revision=" ") == {
        "inputs": {
            "base": {"length": {"content": 0, "total": 2}},
            "revision": {"length": {"content": 0, "total": 1}},
        },
        "results": {
            "added": {"length": {"content": 0, "total": 0}},
            "matched": {
                "base_preserved": {"content": 0, "total": 0.5},
                "length": {"content": 0, "total": 1},
                "revision_matched": {"content": 0, "total": 1.0},
            },
            "removed": {"length": {"content": 0, "total": 1}},
        },
        "score": {"content": 0, "total": 0.5},
    }


def test_base_content_revision_separator():
    assert compare(base="cat", revision=" ") == {
        "inputs": {
            "base": {"length": {"content": 1, "total": 1}},
            "revision": {"length": {"content": 0, "total": 1}},
        },
        "results": {
            "added": {"length": {"content": 0, "total": 1}},
            "matched": {
                "base_preserved": {"content": 0, "total": 0},
                "length": {"content": 0, "total": 0},
                "revision_matched": {"content": 0, "total": 0},
            },
            "removed": {"length": {"content": 1, "total": 1}},
        },
        "score": {"content": 0, "total": 0},
    }


def test_base_separator_revision_content():
    assert compare(base=" ", revision="cat") == {
        "inputs": {
            "base": {"length": {"content": 0, "total": 1}},
            "revision": {"length": {"content": 1, "total": 1}},
        },
        "results": {
            "added": {"length": {"content": 1, "total": 1}},
            "matched": {
                "base_preserved": {"content": 0, "total": 0},
                "length": {"content": 0, "total": 0},
                "revision_matched": {"content": 0, "total": 0},
            },
            "removed": {"length": {"content": 0, "total": 1}},
        },
        "score": {"content": 0, "total": 0},
    }


def test_output_stats():
    assert compare(
        base="a big cat",
        revision="a big orange tabby cat with stripes",
        results="stats",
    ) == {
        "inputs": {
            "base": {"length": {"content": 3, "total": 5}},
            "revision": {"length": {"content": 7, "total": 13}},
        },
        "results": {
            "added": {"length": {"content": 4, "total": 8}},
            "matched": {
                "base_preserved": {"content": 1.0, "total": 1.0},
                "length": {"content": 3, "total": 5},
                "revision_matched": {
                    "content": 0.42857142857142855,
                    "total": 0.38461538461538464,
                },
            },
            "removed": {"length": {"content": 0, "total": 0}},
        },
        "score": {"content": 0.42857142857142855, "total": 0.38461538461538464},
    }


def test_output_formatted_stats():
    assert compare(
        base="a big cat",
        revision="a big orange tabby cat with stripes",
        results="formatted_stats",
    ) == {
        "base": [
            {"label": "Base length", "value": "3 words and 2 separators (5 total)"},
            {"label": "Words also in the revision", "value": "3 of 3 (100%)"},
            {"label": "Similarity", "value": "100% identical to the revision"},
        ],
        "matched": [
            {
                "label": "Identical in base and revision",
                "value": "3 words and 2 separators (5 total)",
            },
            {
                "label": "Removed from the base",
                "value": "0 words and 0 separators (0 total)",
            },
            {
                "label": "Added by the revision",
                "value": "4 words and 4 separators (8 total)",
            },
        ],
        "revision": [
            {
                "label": "Revision length",
                "value": "7 words and 6 separators (13 total)",
            },
            {"label": "Words also in the base", "value": "3 of 7 (43%)"},
            {"label": "Similarity", "value": "38% identical to the base"},
        ],
        "summary": "43% match",
    }


def test_output_bbcode():
    assert compare(
        base="a big cat",
        revision="a big orange tabby cat with stripes",
        results="bbcode",
    ) == {
        "analysis": {
            "base": "[b]Base length:[/b]\n"
            "3 words and 2 separators (5 total)\n"
            "\n"
            "[b]Words also in the revision:[/b]\n"
            "3 of 3 (100%)\n"
            "\n"
            "[b]Similarity:[/b]\n"
            "100% identical to the revision",
            "matched": "[b]Identical in base and revision:[/b]\n"
            "3 words and 2 separators (5 total)\n"
            "\n"
            "[b]Removed from the base:[/b]\n"
            "0 words and 0 separators (0 total)\n"
            "\n"
            "[b]Added by the revision:[/b]\n"
            "4 words and 4 separators (8 total)",
            "revision": "[b]Revision length:[/b]\n"
            "7 words and 6 separators (13 total)\n"
            "\n"
            "[b]Words also in the base:[/b]\n"
            "3 of 7 (43%)\n"
            "\n"
            "[b]Similarity:[/b]\n"
            "38% identical to the base",
        },
        "matched": "a big [u green]orange[/u green][u green] [/u green][u "
        "green]tabby[/u green][u green] [/u green]cat[u green] [/u "
        "green][u green]with[/u green][u green] [/u green][u "
        "green]stripes[/u green]",
        "summary": "43% match",
    }


def test_output_table():

    assert compare(
        base="a big cat",
        revision="a big orange tabby cat with stripes",
        results="table",
    )[:4].startswith("┏━━━")


def test_output_raw_table():
    assert (
        compare(
            base="a big cat",
            revision="a big orange tabby cat with stripes",
            results="raw_table",
        ).__class__.__name__
        == "Table"
    )


def test_output_html():
    assert compare(
        base="a big cat",
        revision="a big orange tabby cat with stripes",
        results="html",
    ) == {
        "css": "    .indifferent {\n"
        "        max-width: 900px;\n"
        "        min-width: 800px;\n"
        "        margin: 0 auto;\n"
        "        background-color: #FFF;\n"
        "        padding: 30px 20px;\n"
        "        color: #333;\n"
        "    }\n"
        "\n"
        "    .indifferent h2.title {\n"
        "        text-align: center;\n"
        "    }\n"
        "\n"
        "    .indifferent h2.title .vs {\n"
        "        font-size: 70%;\n"
        "        color: #333;\n"
        "    }\n"
        "\n"
        "    .indifferent h3.subtitle {\n"
        "        border-bottom: none;\n"
        "        text-align: center;\n"
        "        color: #555;\n"
        "    }\n"
        "\n"
        "    .indifferent .nav-links table {\n"
        "        margin: 40px auto 0px;\n"
        "    }\n"
        "\n"
        "    .indifferent .nav-links td {\n"
        "        border-right: 1px #888 solid;\n"
        "    }\n"
        "\n"
        "    .indifferent .nav-links td.last {\n"
        "        border-right: 0px;\n"
        "    }\n"
        "\n"
        "    .indifferent .nav-links a {\n"
        "        color: #333;\n"
        "        padding: 5px 10px;\n"
        "        text-decoration: none;\n"
        "    }\n"
        "\n"
        "    .indifferent .section h3 {\n"
        "        padding-bottom: 10px;\n"
        "        margin: 20px 0px 0px;\n"
        "        border-bottom: 1px solid grey;\n"
        "    }\n"
        "\n"
        "    .indifferent .section {\n"
        "        padding: 20px 0px;\n"
        "    }\n"
        "\n"
        "    .indifferent .detail {\n"
        "        margin: 10px;\n"
        "        padding: 15px;\n"
        "        border: 1px solid #DDD;\n"
        "        font-family: monospace;\n"
        "    }\n"
        "\n"
        "    .indifferent .matched {\n"
        "        background-color: #DEDEDE;\n"
        "        margin: 0px 1px;\n"
        "    }\n"
        "\n"
        "    .indifferent .added {\n"
        "        color: green;\n"
        "        text-decoration: underline;\n"
        "        font-weight: bold;\n"
        "        margin: 0px 1px\n"
        "    }\n"
        "\n"
        "    .indifferent .deleted {\n"
        "        color: red;\n"
        "        text-decoration: line-through;\n"
        "        margin: 0px 1px;\n"
        "    }\n",
        "html": "<!-- Comparison generated by Indifferent: "
        "https://github.com/brianwarner/indifferent -->\n"
        '<div class="indifferent">\n'
        '    <h2 class="title">Base<br /><span class="vs">vs.</span><br '
        "/>Revision</h2>\n"
        '    <h3 class="subtitle">43% match</h3>\n'
        '    <div class="nav-links">\n'
        "        <table>\n"
        "            <tr>\n"
        '                <td><a href="#indifferent.base">Base</a></td>\n'
        "                <td><a "
        'href="#indifferent.revision">Revision</a></td>\n'
        '                <td class="last"><a '
        'href="#indifferent.match">Comparison</a></td>\n'
        "            </tr>\n"
        "        </table>\n"
        "    </div>\n"
        '    <div class="section base">\n'
        '        <a id="indifferent.base"></a>\n'
        "        <h3>Base</h3>\n"
        '        <div class="summary">\n'
        "            <ul>\n"
        "                <li><strong>Base length:</strong> 3 words and 2 "
        "separators (5 total)</li>\n"
        "                <li><strong>Words also in the revision:</strong> 3 "
        "of 3 (100%)</li>\n"
        "                <li><strong>Similarity:</strong> 100% identical to "
        "the revision</li>\n"
        "            </ul>\n"
        "        </div>\n"
        '        <div class="detail">\n'
        "            a big cat\n"
        "        </div>\n"
        "    </div>\n"
        '    <div class="section revision">\n'
        '        <a id="indifferent.revision"></a>\n'
        "        <h3>Revision</h3>\n"
        '        <div class="summary">\n'
        "            <ul>\n"
        "                <li><strong>Revision length:</strong> 7 words and 6 "
        "separators (13 total)</li>\n"
        "                <li><strong>Words also in the base:</strong> 3 of 7 "
        "(43%)</li>\n"
        "                <li><strong>Similarity:</strong> 38% identical to "
        "the base</li>\n"
        "            </ul>\n"
        "        </div>\n"
        '        <div class="detail">\n'
        "            a big orange tabby cat with stripes\n"
        "        </div>\n"
        "    </div>\n"
        '    <div class="section match">\n'
        '        <a id="indifferent.match"></a>\n'
        "        <h3>Comparison: 43% match</h3>\n"
        '        <div class="summary">\n'
        "            <ul>\n"
        "                <li><strong>Identical in base and revision:</strong> "
        "3 words and 2 separators (5 total)</li>\n"
        "                <li><strong>Removed from the base:</strong> 0 words "
        "and 0 separators (0 total)</li>\n"
        "                <li><strong>Added by the revision:</strong> 4 words "
        "and 4 separators (8 total)</li>\n"
        "        </div>\n"
        '        <div class="detail">\n'
        '            <span class="matched">a</span><span class="matched"> '
        '</span><span class="matched">big</span><span class="matched"> '
        '</span><span class="added">orange</span><span class="added"> '
        '</span><span class="added">tabby</span><span class="added"> '
        '</span><span class="matched">cat</span><span class="added"> '
        '</span><span class="added">with</span><span class="added"> '
        '</span><span class="added">stripes</span>\n'
        "        </div>\n"
        "    </div>\n"
        "</div>",
    }


def test_output_html_inline():
    assert compare(
        base="a big cat",
        revision="a big orange tabby cat with stripes",
        results="html_inline",
    ) == {
        "css": "",
        "html": "<!-- Comparison generated by Indifferent: "
        "https://github.com/brianwarner/indifferent -->\n"
        '<div class="indifferent" style="max-width: 900px; min-width: 800px; '
        "margin: 0 auto; background-color: #FFF; padding: 30px 20px; color: "
        '#333;">\n'
        '    <h2 style="text-align: center;" class="title">Base<br /><span '
        'class="vs" style="font-size: 70%; color: #333;">vs.</span><br '
        "/>Revision</h2>\n"
        '    <h3 style="border-bottom: none; text-align: center; color: '
        '#555;" class="subtitle">43% match</h3>\n'
        '    <div class="nav-links">\n'
        '        <table style="margin: 40px auto 0px;">\n'
        "            <tr>\n"
        '                <td style="border-right: 1px #888 solid;"><a '
        'href="#indifferent.base" style="color: #333; padding: 5px 10px; '
        'text-decoration: none;">Base</a></td>\n'
        '                <td style="border-right: 1px #888 solid;"><a '
        'href="#indifferent.revision" style="color: #333; padding: 5px 10px; '
        'text-decoration: none;">Revision</a></td>\n'
        '                <td style="border-right: 0px;" class="last"><a '
        'href="#indifferent.match" style="color: #333; padding: 5px 10px; '
        'text-decoration: none;">Comparison</a></td>\n'
        "            </tr>\n"
        "        </table>\n"
        "    </div>\n"
        '    <div class="section base" style="padding: 20px 0px;">\n'
        '        <a id="indifferent.base"></a>\n'
        '        <h3 style="padding-bottom: 10px; margin: 20px 0px 0px; '
        'border-bottom: 1px solid grey;">Base</h3>\n'
        '        <div class="summary">\n'
        "            <ul>\n"
        "                <li><strong>Base length:</strong> 3 words and 2 "
        "separators (5 total)</li>\n"
        "                <li><strong>Words also in the revision:</strong> 3 "
        "of 3 (100%)</li>\n"
        "                <li><strong>Similarity:</strong> 100% identical to "
        "the revision</li>\n"
        "            </ul>\n"
        "        </div>\n"
        '        <div class="detail" style="margin: 10px; padding: 15px; '
        'border: 1px solid #DDD; font-family: monospace;">\n'
        "            a big cat\n"
        "        </div>\n"
        "    </div>\n"
        '    <div class="section revision" style="padding: 20px 0px;">\n'
        '        <a id="indifferent.revision"></a>\n'
        '        <h3 style="padding-bottom: 10px; margin: 20px 0px 0px; '
        'border-bottom: 1px solid grey;">Revision</h3>\n'
        '        <div class="summary">\n'
        "            <ul>\n"
        "                <li><strong>Revision length:</strong> 7 words and 6 "
        "separators (13 total)</li>\n"
        "                <li><strong>Words also in the base:</strong> 3 of 7 "
        "(43%)</li>\n"
        "                <li><strong>Similarity:</strong> 38% identical to "
        "the base</li>\n"
        "            </ul>\n"
        "        </div>\n"
        '        <div class="detail" style="margin: 10px; padding: 15px; '
        'border: 1px solid #DDD; font-family: monospace;">\n'
        "            a big orange tabby cat with stripes\n"
        "        </div>\n"
        "    </div>\n"
        '    <div class="section match" style="padding: 20px 0px;">\n'
        '        <a id="indifferent.match"></a>\n'
        '        <h3 style="padding-bottom: 10px; margin: 20px 0px 0px; '
        'border-bottom: 1px solid grey;">Comparison: 43% match</h3>\n'
        '        <div class="summary">\n'
        "            <ul>\n"
        "                <li><strong>Identical in base and revision:</strong> "
        "3 words and 2 separators (5 total)</li>\n"
        "                <li><strong>Removed from the base:</strong> 0 words "
        "and 0 separators (0 total)</li>\n"
        "                <li><strong>Added by the revision:</strong> 4 words "
        "and 4 separators (8 total)</li>\n"
        "        </div>\n"
        '        <div class="detail" style="margin: 10px; padding: 15px; '
        'border: 1px solid #DDD; font-family: monospace;">\n'
        '            <span class="matched" style="background-color: #DEDEDE; '
        'margin: 0px 1px;">a</span><span class="matched" '
        'style="background-color: #DEDEDE; margin: 0px 1px;"> </span><span '
        'class="matched" style="background-color: #DEDEDE; margin: 0px '
        '1px;">big</span><span class="matched" style="background-color: '
        '#DEDEDE; margin: 0px 1px;"> </span><span class="added" style="color: '
        "green; text-decoration: underline; font-weight: bold; margin: 0px "
        '1px">orange</span><span class="added" style="color: green; '
        'text-decoration: underline; font-weight: bold; margin: 0px 1px"> '
        '</span><span class="added" style="color: green; text-decoration: '
        'underline; font-weight: bold; margin: 0px 1px">tabby</span><span '
        'class="added" style="color: green; text-decoration: underline; '
        'font-weight: bold; margin: 0px 1px"> </span><span class="matched" '
        'style="background-color: #DEDEDE; margin: 0px 1px;">cat</span><span '
        'class="added" style="color: green; text-decoration: underline; '
        'font-weight: bold; margin: 0px 1px"> </span><span class="added" '
        'style="color: green; text-decoration: underline; font-weight: bold; '
        'margin: 0px 1px">with</span><span class="added" style="color: green; '
        'text-decoration: underline; font-weight: bold; margin: 0px 1px"> '
        '</span><span class="added" style="color: green; text-decoration: '
        'underline; font-weight: bold; margin: 0px 1px">stripes</span>\n'
        "        </div>\n"
        "    </div>\n"
        "</div>",
    }


def test_output_html_page():
    assert compare(
        base="a big cat",
        revision="a big orange tabby cat with stripes",
        results="html_page",
    ) == {
        "css": "   .page {\n"
        "        background-color: #DDD;\n"
        "        font-family: sans-serif;\n"
        "    }\n"
        "\n"
        "    .indifferent {\n"
        "        max-width: 900px;\n"
        "        min-width: 800px;\n"
        "        margin: 0 auto;\n"
        "        background-color: #FFF;\n"
        "        padding: 30px 20px;\n"
        "        color: #333;\n"
        "    }\n"
        "\n"
        "    .indifferent h1.title {\n"
        "        text-align: center;\n"
        "    }\n"
        "\n"
        "    .indifferent h1.title .vs {\n"
        "        font-size: 70%;\n"
        "        color: #333;\n"
        "    }\n"
        "\n"
        "    .indifferent h2.subtitle {\n"
        "        border-bottom: none;\n"
        "        text-align: center;\n"
        "        color: #555;\n"
        "    }\n"
        "\n"
        "    .indifferent .nav-links table {\n"
        "        margin: 40px auto 0px;\n"
        "    }\n"
        "\n"
        "    .indifferent .nav-links td {\n"
        "        border-right: 1px #888 solid;\n"
        "    }\n"
        "\n"
        "    .indifferent .nav-links td.last {\n"
        "        border-right: 0px;\n"
        "    }\n"
        "\n"
        "    .indifferent .nav-links a {\n"
        "        color: #333;\n"
        "        padding: 5px 10px;\n"
        "        text-decoration: none;\n"
        "    }\n"
        "\n"
        "    .indifferent .section h2 {\n"
        "        padding-bottom: 10px;\n"
        "        margin: 20px 0px 0px;\n"
        "        border-bottom: 1px solid grey;\n"
        "    }\n"
        "\n"
        "    .indifferent .section {\n"
        "        padding: 20px 0px;\n"
        "    }\n"
        "\n"
        "    .indifferent .detail {\n"
        "        margin: 10px;\n"
        "        padding: 15px;\n"
        "        border: 1px solid #DDD;\n"
        "        font-family: monospace;\n"
        "    }\n"
        "\n"
        "    .indifferent .matched {\n"
        "        background-color: #DEDEDE;\n"
        "        margin: 0px 1px;\n"
        "    }\n"
        "\n"
        "    .indifferent .added {\n"
        "        color: green;\n"
        "        text-decoration: underline;\n"
        "        font-weight: bold;\n"
        "        margin: 0px 1px\n"
        "    }\n"
        "\n"
        "    .indifferent .deleted {\n"
        "        color: red;\n"
        "        text-decoration: line-through;\n"
        "        margin: 0px 1px;\n"
        "    }\n",
        "html": "<!doctype html>\n"
        '<html lang="en-US">\n'
        "<head>\n"
        '<meta charset="utf-8" />\n'
        "<title>Comparison of Base and Revision</title>\n"
        '<link rel="stylesheet" href="indifferent.css">\n'
        "</head>\n"
        '<body class="page">\n'
        "<!-- Comparison generated by Indifferent: "
        "https://github.com/brianwarner/indifferent -->\n"
        '<div class="indifferent">\n'
        '    <h1 class="title">Base<br /><span class="vs">vs.</span><br '
        "/>Revision</h1>\n"
        '    <h2 class="subtitle">43% match</h2>\n'
        '    <div class="nav-links">\n'
        "        <table>\n"
        "            <tr>\n"
        '                <td><a href="#indifferent.base">Base</a></td>\n'
        "                <td><a "
        'href="#indifferent.revision">Revision</a></td>\n'
        '                <td class="last"><a '
        'href="#indifferent.match">Comparison</a></td>\n'
        "            </tr>\n"
        "        </table>\n"
        "    </div>\n"
        '    <div class="section base">\n'
        '        <a id="indifferent.base"></a>\n'
        "        <h2>Base</h2>\n"
        '        <div class="summary">\n'
        "            <ul>\n"
        "                <li><strong>Base length:</strong> 3 words and 2 "
        "separators (5 total)</li>\n"
        "                <li><strong>Words also in the revision:</strong> 3 "
        "of 3 (100%)</li>\n"
        "                <li><strong>Similarity:</strong> 100% identical to "
        "the revision</li>\n"
        "            </ul>\n"
        "        </div>\n"
        '        <div class="detail">\n'
        "            a big cat\n"
        "        </div>\n"
        "    </div>\n"
        '    <div class="section revision">\n'
        '        <a id="indifferent.revision"></a>\n'
        "        <h2>Revision</h2>\n"
        '        <div class="summary">\n'
        "            <ul>\n"
        "                <li><strong>Revision length:</strong> 7 words and 6 "
        "separators (13 total)</li>\n"
        "                <li><strong>Words also in the base:</strong> 3 of 7 "
        "(43%)</li>\n"
        "                <li><strong>Similarity:</strong> 38% identical to "
        "the base</li>\n"
        "            </ul>\n"
        "        </div>\n"
        '        <div class="detail">\n'
        "            a big orange tabby cat with stripes\n"
        "        </div>\n"
        "    </div>\n"
        '    <div class="section match">\n'
        '        <a id="indifferent.match"></a>\n'
        "        <h2>Comparison: 43% match</h2>\n"
        '        <div class="summary">\n'
        "            <ul>\n"
        "                <li><strong>Identical in base and revision:</strong> "
        "3 words and 2 separators (5 total)</li>\n"
        "                <li><strong>Removed from the base:</strong> 0 words "
        "and 0 separators (0 total)</li>\n"
        "                <li><strong>Added by the revision:</strong> 4 words "
        "and 4 separators (8 total)</li>\n"
        "        </div>\n"
        '        <div class="detail">\n'
        '            <span class="matched">a</span><span class="matched"> '
        '</span><span class="matched">big</span><span class="matched"> '
        '</span><span class="added">orange</span><span class="added"> '
        '</span><span class="added">tabby</span><span class="added"> '
        '</span><span class="matched">cat</span><span class="added"> '
        '</span><span class="added">with</span><span class="added"> '
        '</span><span class="added">stripes</span>\n'
        "        </div>\n"
        "    </div>\n"
        "</div>\n"
        "</body>\n"
        "</html>",
    }


def test_output_html_page_internal():
    assert compare(
        base="a big cat",
        revision="a big orange tabby cat with stripes",
        results="html_page_internal",
    ) == {
        "css": "",
        "html": "<!doctype html>\n"
        '<html lang="en-US">\n'
        "<head>\n"
        '<meta charset="utf-8" />\n'
        "<title>Comparison of Base and Revision</title>\n"
        "<style>\n"
        "   .page {\n"
        "        background-color: #DDD;\n"
        "        font-family: sans-serif;\n"
        "    }\n"
        "\n"
        "    .indifferent {\n"
        "        max-width: 900px;\n"
        "        min-width: 800px;\n"
        "        margin: 0 auto;\n"
        "        background-color: #FFF;\n"
        "        padding: 30px 20px;\n"
        "        color: #333;\n"
        "    }\n"
        "\n"
        "    .indifferent h1.title {\n"
        "        text-align: center;\n"
        "    }\n"
        "\n"
        "    .indifferent h1.title .vs {\n"
        "        font-size: 70%;\n"
        "        color: #333;\n"
        "    }\n"
        "\n"
        "    .indifferent h2.subtitle {\n"
        "        border-bottom: none;\n"
        "        text-align: center;\n"
        "        color: #555;\n"
        "    }\n"
        "\n"
        "    .indifferent .nav-links table {\n"
        "        margin: 40px auto 0px;\n"
        "    }\n"
        "\n"
        "    .indifferent .nav-links td {\n"
        "        border-right: 1px #888 solid;\n"
        "    }\n"
        "\n"
        "    .indifferent .nav-links td.last {\n"
        "        border-right: 0px;\n"
        "    }\n"
        "\n"
        "    .indifferent .nav-links a {\n"
        "        color: #333;\n"
        "        padding: 5px 10px;\n"
        "        text-decoration: none;\n"
        "    }\n"
        "\n"
        "    .indifferent .section h2 {\n"
        "        padding-bottom: 10px;\n"
        "        margin: 20px 0px 0px;\n"
        "        border-bottom: 1px solid grey;\n"
        "    }\n"
        "\n"
        "    .indifferent .section {\n"
        "        padding: 20px 0px;\n"
        "    }\n"
        "\n"
        "    .indifferent .detail {\n"
        "        margin: 10px;\n"
        "        padding: 15px;\n"
        "        border: 1px solid #DDD;\n"
        "        font-family: monospace;\n"
        "    }\n"
        "\n"
        "    .indifferent .matched {\n"
        "        background-color: #DEDEDE;\n"
        "        margin: 0px 1px;\n"
        "    }\n"
        "\n"
        "    .indifferent .added {\n"
        "        color: green;\n"
        "        text-decoration: underline;\n"
        "        font-weight: bold;\n"
        "        margin: 0px 1px\n"
        "    }\n"
        "\n"
        "    .indifferent .deleted {\n"
        "        color: red;\n"
        "        text-decoration: line-through;\n"
        "        margin: 0px 1px;\n"
        "    }\n"
        "</style>\n"
        "</head>\n"
        '<body class="page">\n'
        "<!-- Comparison generated by Indifferent: "
        "https://github.com/brianwarner/indifferent -->\n"
        '<div class="indifferent">\n'
        '    <h1 class="title">Base<br /><span class="vs">vs.</span><br '
        "/>Revision</h1>\n"
        '    <h2 class="subtitle">43% match</h2>\n'
        '    <div class="nav-links">\n'
        "        <table>\n"
        "            <tr>\n"
        '                <td><a href="#indifferent.base">Base</a></td>\n'
        "                <td><a "
        'href="#indifferent.revision">Revision</a></td>\n'
        '                <td class="last"><a '
        'href="#indifferent.match">Comparison</a></td>\n'
        "            </tr>\n"
        "        </table>\n"
        "    </div>\n"
        '    <div class="section base">\n'
        '        <a id="indifferent.base"></a>\n'
        "        <h2>Base</h2>\n"
        '        <div class="summary">\n'
        "            <ul>\n"
        "                <li><strong>Base length:</strong> 3 words and 2 "
        "separators (5 total)</li>\n"
        "                <li><strong>Words also in the revision:</strong> 3 "
        "of 3 (100%)</li>\n"
        "                <li><strong>Similarity:</strong> 100% identical to "
        "the revision</li>\n"
        "            </ul>\n"
        "        </div>\n"
        '        <div class="detail">\n'
        "            a big cat\n"
        "        </div>\n"
        "    </div>\n"
        '    <div class="section revision">\n'
        '        <a id="indifferent.revision"></a>\n'
        "        <h2>Revision</h2>\n"
        '        <div class="summary">\n'
        "            <ul>\n"
        "                <li><strong>Revision length:</strong> 7 words and 6 "
        "separators (13 total)</li>\n"
        "                <li><strong>Words also in the base:</strong> 3 of 7 "
        "(43%)</li>\n"
        "                <li><strong>Similarity:</strong> 38% identical to "
        "the base</li>\n"
        "            </ul>\n"
        "        </div>\n"
        '        <div class="detail">\n'
        "            a big orange tabby cat with stripes\n"
        "        </div>\n"
        "    </div>\n"
        '    <div class="section match">\n'
        '        <a id="indifferent.match"></a>\n'
        "        <h2>Comparison: 43% match</h2>\n"
        '        <div class="summary">\n'
        "            <ul>\n"
        "                <li><strong>Identical in base and revision:</strong> "
        "3 words and 2 separators (5 total)</li>\n"
        "                <li><strong>Removed from the base:</strong> 0 words "
        "and 0 separators (0 total)</li>\n"
        "                <li><strong>Added by the revision:</strong> 4 words "
        "and 4 separators (8 total)</li>\n"
        "        </div>\n"
        '        <div class="detail">\n'
        '            <span class="matched">a</span><span class="matched"> '
        '</span><span class="matched">big</span><span class="matched"> '
        '</span><span class="added">orange</span><span class="added"> '
        '</span><span class="added">tabby</span><span class="added"> '
        '</span><span class="matched">cat</span><span class="added"> '
        '</span><span class="added">with</span><span class="added"> '
        '</span><span class="added">stripes</span>\n'
        "        </div>\n"
        "    </div>\n"
        "</div>\n"
        "</body>\n"
        "</html>",
    }


def test_output_html_page_inline():
    assert compare(
        base="a big cat",
        revision="a big orange tabby cat with stripes",
        results="html_page_inline",
    ) == {
        "css": "",
        "html": "<!doctype html>\n"
        '<html lang="en-US">\n'
        "<head>\n"
        '<meta charset="utf-8" />\n'
        "<title>Comparison of Base and Revision</title>\n"
        "</head>\n"
        '<body class="page" style="background-color: #DDD; font-family: '
        'sans-serif;">\n'
        "<!-- Comparison generated by Indifferent: "
        "https://github.com/brianwarner/indifferent -->\n"
        '<div class="indifferent" style="max-width: 900px; min-width: 800px; '
        "margin: 0 auto; background-color: #FFF; padding: 30px 20px; color: "
        '#333;">\n'
        '    <h1 style="text-align: center;" class="title">Base<br /><span '
        'class="vs" style="font-size: 70%; color: #333;">vs.</span><br '
        "/>Revision</h1>\n"
        '    <h2 style="border-bottom: none; text-align: center; color: '
        '#555;" class="subtitle">43% match</h2>\n'
        '    <div class="nav-links">\n'
        '        <table style="margin: 40px auto 0px;">\n'
        "            <tr>\n"
        '                <td style="border-right: 1px #888 solid;"><a '
        'href="#indifferent.base" style="color: #333; padding: 5px 10px; '
        'text-decoration: none;">Base</a></td>\n'
        '                <td style="border-right: 1px #888 solid;"><a '
        'href="#indifferent.revision" style="color: #333; padding: 5px 10px; '
        'text-decoration: none;">Revision</a></td>\n'
        '                <td style="border-right: 0px;" class="last"><a '
        'href="#indifferent.match" style="color: #333; padding: 5px 10px; '
        'text-decoration: none;">Comparison</a></td>\n'
        "            </tr>\n"
        "        </table>\n"
        "    </div>\n"
        '    <div class="section base" style="padding: 20px 0px;">\n'
        '        <a id="indifferent.base"></a>\n'
        '        <h2 style="padding-bottom: 10px; margin: 20px 0px 0px; '
        'border-bottom: 1px solid grey;">Base</h2>\n'
        '        <div class="summary">\n'
        "            <ul>\n"
        "                <li><strong>Base length:</strong> 3 words and 2 "
        "separators (5 total)</li>\n"
        "                <li><strong>Words also in the revision:</strong> 3 "
        "of 3 (100%)</li>\n"
        "                <li><strong>Similarity:</strong> 100% identical to "
        "the revision</li>\n"
        "            </ul>\n"
        "        </div>\n"
        '        <div class="detail" style="margin: 10px; padding: 15px; '
        'border: 1px solid #DDD; font-family: monospace;">\n'
        "            a big cat\n"
        "        </div>\n"
        "    </div>\n"
        '    <div class="section revision" style="padding: 20px 0px;">\n'
        '        <a id="indifferent.revision"></a>\n'
        '        <h2 style="padding-bottom: 10px; margin: 20px 0px 0px; '
        'border-bottom: 1px solid grey;">Revision</h2>\n'
        '        <div class="summary">\n'
        "            <ul>\n"
        "                <li><strong>Revision length:</strong> 7 words and 6 "
        "separators (13 total)</li>\n"
        "                <li><strong>Words also in the base:</strong> 3 of 7 "
        "(43%)</li>\n"
        "                <li><strong>Similarity:</strong> 38% identical to "
        "the base</li>\n"
        "            </ul>\n"
        "        </div>\n"
        '        <div class="detail" style="margin: 10px; padding: 15px; '
        'border: 1px solid #DDD; font-family: monospace;">\n'
        "            a big orange tabby cat with stripes\n"
        "        </div>\n"
        "    </div>\n"
        '    <div class="section match" style="padding: 20px 0px;">\n'
        '        <a id="indifferent.match"></a>\n'
        '        <h2 style="padding-bottom: 10px; margin: 20px 0px 0px; '
        'border-bottom: 1px solid grey;">Comparison: 43% match</h2>\n'
        '        <div class="summary">\n'
        "            <ul>\n"
        "                <li><strong>Identical in base and revision:</strong> "
        "3 words and 2 separators (5 total)</li>\n"
        "                <li><strong>Removed from the base:</strong> 0 words "
        "and 0 separators (0 total)</li>\n"
        "                <li><strong>Added by the revision:</strong> 4 words "
        "and 4 separators (8 total)</li>\n"
        "        </div>\n"
        '        <div class="detail" style="margin: 10px; padding: 15px; '
        'border: 1px solid #DDD; font-family: monospace;">\n'
        '            <span class="matched" style="background-color: #DEDEDE; '
        'margin: 0px 1px;">a</span><span class="matched" '
        'style="background-color: #DEDEDE; margin: 0px 1px;"> </span><span '
        'class="matched" style="background-color: #DEDEDE; margin: 0px '
        '1px;">big</span><span class="matched" style="background-color: '
        '#DEDEDE; margin: 0px 1px;"> </span><span class="added" style="color: '
        "green; text-decoration: underline; font-weight: bold; margin: 0px "
        '1px">orange</span><span class="added" style="color: green; '
        'text-decoration: underline; font-weight: bold; margin: 0px 1px"> '
        '</span><span class="added" style="color: green; text-decoration: '
        'underline; font-weight: bold; margin: 0px 1px">tabby</span><span '
        'class="added" style="color: green; text-decoration: underline; '
        'font-weight: bold; margin: 0px 1px"> </span><span class="matched" '
        'style="background-color: #DEDEDE; margin: 0px 1px;">cat</span><span '
        'class="added" style="color: green; text-decoration: underline; '
        'font-weight: bold; margin: 0px 1px"> </span><span class="added" '
        'style="color: green; text-decoration: underline; font-weight: bold; '
        'margin: 0px 1px">with</span><span class="added" style="color: green; '
        'text-decoration: underline; font-weight: bold; margin: 0px 1px"> '
        '</span><span class="added" style="color: green; text-decoration: '
        'underline; font-weight: bold; margin: 0px 1px">stripes</span>\n'
        "        </div>\n"
        "    </div>\n"
        "</div>\n"
        "</body>\n"
        "</html>",
    }


def test_output_raw():
    assert compare(
        base="a big cat",
        revision="a big orange tabby cat with stripes",
        results="raw",
    ) == [
        {"base": 0, "content": True, "revision": 0, "value": "a"},
        {"base": 1, "content": False, "revision": 1, "value": " "},
        {"base": 2, "content": True, "revision": 2, "value": "big"},
        {"base": 3, "content": False, "revision": 3, "value": " "},
        {"base": None, "content": True, "revision": 4, "value": "orange"},
        {"base": None, "content": False, "revision": 5, "value": " "},
        {"base": None, "content": True, "revision": 6, "value": "tabby"},
        {"base": None, "content": False, "revision": 7, "value": " "},
        {"base": 4, "content": True, "revision": 8, "value": "cat"},
        {"base": None, "content": False, "revision": 9, "value": " "},
        {"base": None, "content": True, "revision": 10, "value": "with"},
        {"base": None, "content": False, "revision": 11, "value": " "},
        {"base": None, "content": True, "revision": 12, "value": "stripes"},
    ]


def test_titles():
    assert compare(
        base="a big cat",
        revision="a big orange tabby cat with stripes",
        base_name="What is that?",
        revision_name="More details please",
        results="html",
    ) == {
        "css": "    .indifferent {\n"
        "        max-width: 900px;\n"
        "        min-width: 800px;\n"
        "        margin: 0 auto;\n"
        "        background-color: #FFF;\n"
        "        padding: 30px 20px;\n"
        "        color: #333;\n"
        "    }\n"
        "\n"
        "    .indifferent h2.title {\n"
        "        text-align: center;\n"
        "    }\n"
        "\n"
        "    .indifferent h2.title .vs {\n"
        "        font-size: 70%;\n"
        "        color: #333;\n"
        "    }\n"
        "\n"
        "    .indifferent h3.subtitle {\n"
        "        border-bottom: none;\n"
        "        text-align: center;\n"
        "        color: #555;\n"
        "    }\n"
        "\n"
        "    .indifferent .nav-links table {\n"
        "        margin: 40px auto 0px;\n"
        "    }\n"
        "\n"
        "    .indifferent .nav-links td {\n"
        "        border-right: 1px #888 solid;\n"
        "    }\n"
        "\n"
        "    .indifferent .nav-links td.last {\n"
        "        border-right: 0px;\n"
        "    }\n"
        "\n"
        "    .indifferent .nav-links a {\n"
        "        color: #333;\n"
        "        padding: 5px 10px;\n"
        "        text-decoration: none;\n"
        "    }\n"
        "\n"
        "    .indifferent .section h3 {\n"
        "        padding-bottom: 10px;\n"
        "        margin: 20px 0px 0px;\n"
        "        border-bottom: 1px solid grey;\n"
        "    }\n"
        "\n"
        "    .indifferent .section {\n"
        "        padding: 20px 0px;\n"
        "    }\n"
        "\n"
        "    .indifferent .detail {\n"
        "        margin: 10px;\n"
        "        padding: 15px;\n"
        "        border: 1px solid #DDD;\n"
        "        font-family: monospace;\n"
        "    }\n"
        "\n"
        "    .indifferent .matched {\n"
        "        background-color: #DEDEDE;\n"
        "        margin: 0px 1px;\n"
        "    }\n"
        "\n"
        "    .indifferent .added {\n"
        "        color: green;\n"
        "        text-decoration: underline;\n"
        "        font-weight: bold;\n"
        "        margin: 0px 1px\n"
        "    }\n"
        "\n"
        "    .indifferent .deleted {\n"
        "        color: red;\n"
        "        text-decoration: line-through;\n"
        "        margin: 0px 1px;\n"
        "    }\n",
        "html": "<!-- Comparison generated by Indifferent: "
        "https://github.com/brianwarner/indifferent -->\n"
        '<div class="indifferent">\n'
        '    <h2 class="title">What is that?<br /><span '
        'class="vs">vs.</span><br />More details please</h2>\n'
        '    <h3 class="subtitle">43% match</h3>\n'
        '    <div class="nav-links">\n'
        "        <table>\n"
        "            <tr>\n"
        '                <td><a href="#indifferent.base">Base</a></td>\n'
        "                <td><a "
        'href="#indifferent.revision">Revision</a></td>\n'
        '                <td class="last"><a '
        'href="#indifferent.match">Comparison</a></td>\n'
        "            </tr>\n"
        "        </table>\n"
        "    </div>\n"
        '    <div class="section base">\n'
        '        <a id="indifferent.base"></a>\n'
        "        <h3>Base: What is that?</h3>\n"
        '        <div class="summary">\n'
        "            <ul>\n"
        "                <li><strong>Base length:</strong> 3 words and 2 "
        "separators (5 total)</li>\n"
        "                <li><strong>Words also in the revision:</strong> 3 "
        "of 3 (100%)</li>\n"
        "                <li><strong>Similarity:</strong> 100% identical to "
        "the revision</li>\n"
        "            </ul>\n"
        "        </div>\n"
        '        <div class="detail">\n'
        "            a big cat\n"
        "        </div>\n"
        "    </div>\n"
        '    <div class="section revision">\n'
        '        <a id="indifferent.revision"></a>\n'
        "        <h3>Revision: More details please</h3>\n"
        '        <div class="summary">\n'
        "            <ul>\n"
        "                <li><strong>Revision length:</strong> 7 words and 6 "
        "separators (13 total)</li>\n"
        "                <li><strong>Words also in the base:</strong> 3 of 7 "
        "(43%)</li>\n"
        "                <li><strong>Similarity:</strong> 38% identical to "
        "the base</li>\n"
        "            </ul>\n"
        "        </div>\n"
        '        <div class="detail">\n'
        "            a big orange tabby cat with stripes\n"
        "        </div>\n"
        "    </div>\n"
        '    <div class="section match">\n'
        '        <a id="indifferent.match"></a>\n'
        "        <h3>Comparison: 43% match</h3>\n"
        '        <div class="summary">\n'
        "            <ul>\n"
        "                <li><strong>Identical in base and revision:</strong> "
        "3 words and 2 separators (5 total)</li>\n"
        "                <li><strong>Removed from the base:</strong> 0 words "
        "and 0 separators (0 total)</li>\n"
        "                <li><strong>Added by the revision:</strong> 4 words "
        "and 4 separators (8 total)</li>\n"
        "        </div>\n"
        '        <div class="detail">\n'
        '            <span class="matched">a</span><span class="matched"> '
        '</span><span class="matched">big</span><span class="matched"> '
        '</span><span class="added">orange</span><span class="added"> '
        '</span><span class="added">tabby</span><span class="added"> '
        '</span><span class="matched">cat</span><span class="added"> '
        '</span><span class="added">with</span><span class="added"> '
        '</span><span class="added">stripes</span>\n'
        "        </div>\n"
        "    </div>\n"
        "</div>",
    }
