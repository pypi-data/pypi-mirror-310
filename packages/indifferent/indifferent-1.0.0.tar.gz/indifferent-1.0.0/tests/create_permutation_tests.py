import os

# Write test files to check permutations with a variety of phrases. The intent is not to check
# correctness, but rather uncover edge cases that lead to failures.
#
# Manually written tests are the correct way to test for correctness.

# Input values
test_components = [
    {"value": "", "description": "empty"},
    {"value": "cat", "description": "content"},
    {"value": "tabby", "description": "alternate content"},
    {"value": " ", "description": "separator"},
    {"value": "\t", "description": "alternate separator"},
    {"value": " cat", "description": "separator then content"},
    {"value": "cat ", "description": "content then separator"},
    {"value": " cat ", "description": "separator then content then separator"},
    {"value": " \t", "description": "consecutive separators"},
    {"value": "a tabby cat", "description": "phrase"},
    {"value": " a tabby cat", "description": "separator at start of phrase"},
    {"value": "a tabby cat ", "description": "separator at end of phrase"},
    {"value": " a tabby cat ", "description": "separators at start and end of phrase"},
    {"value": "  a tabby cat", "description": "two separators at start of phrase"},
    {"value": "a tabby cat  ", "description": "two separators at end of phrase"},
    {
        "value": "  a tabby cat  ",
        "description": "two separators at start and end of phrase",
    },
    {"value": "a tabby cat and another tabby cat", "description": "repeating phrase"},
]


results = [
    "stats",
    "formatted_stats",
    "bbcode",
    "table",
    "raw_table",
    "html",
    "html_inline",
    "html_page",
    "html_page_internal",
    "html_page_inline",
    "raw",
]


# Generate tests
print("\nGenerate permutation tests for Indifferent\n")

print(" * Values used in testing:")
for test_component in test_components:
    print(
        '   - "%s" - %s'
        % (test_component["value"], test_component["description"].capitalize())
    )

print("* Result formats")
for result in results:
    print("   - %s" % result)

for result in results:
    with open(
        os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            "permutations",
            "test_permutations_%s.py" % result,
        ),
        "w",
        encoding="utf-8",
    ) as testfile:
        testfile.write("from indifferent.indifferent import compare\nimport pytest\n")

        print(" * %s" % result)

        for base in test_components:
            print('   - base: "%s"' % base["value"])

            for revision in test_components:
                print('     + revision: "%s"' % revision["value"])

                testfile.write(
                    """

@pytest.mark.skipif("config.getoption('quick')")
def test_compare_%s_%s():  # noqa E501
    assert repr(
        compare(
            base="%s",
            revision="%s",
            results="%s")
    ), 'Base: \"%s\"; Revision: \"%s\"'  # noqa E501
"""
                    % (
                        base["description"].replace(" ", "_"),
                        revision["description"].replace(" ", "_"),
                        base["value"],
                        revision["value"],
                        result,
                        base["description"].capitalize(),
                        revision["description"].capitalize(),
                    )
                )
