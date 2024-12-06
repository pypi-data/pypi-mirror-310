from indifferent.indifferent import compare
import pytest


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_empty_empty():  # noqa E501
    assert repr(
        compare(
            base="",
            revision="",
            results="html_page")
    ), 'Base: "Empty"; Revision: "Empty"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_empty_content():  # noqa E501
    assert repr(
        compare(
            base="",
            revision="cat",
            results="html_page")
    ), 'Base: "Empty"; Revision: "Content"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_empty_alternate_content():  # noqa E501
    assert repr(
        compare(
            base="",
            revision="tabby",
            results="html_page")
    ), 'Base: "Empty"; Revision: "Alternate content"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_empty_separator():  # noqa E501
    assert repr(
        compare(
            base="",
            revision=" ",
            results="html_page")
    ), 'Base: "Empty"; Revision: "Separator"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_empty_alternate_separator():  # noqa E501
    assert repr(
        compare(
            base="",
            revision="	",
            results="html_page")
    ), 'Base: "Empty"; Revision: "Alternate separator"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_empty_separator_then_content():  # noqa E501
    assert repr(
        compare(
            base="",
            revision=" cat",
            results="html_page")
    ), 'Base: "Empty"; Revision: "Separator then content"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_empty_content_then_separator():  # noqa E501
    assert repr(
        compare(
            base="",
            revision="cat ",
            results="html_page")
    ), 'Base: "Empty"; Revision: "Content then separator"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_empty_separator_then_content_then_separator():  # noqa E501
    assert repr(
        compare(
            base="",
            revision=" cat ",
            results="html_page")
    ), 'Base: "Empty"; Revision: "Separator then content then separator"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_empty_consecutive_separators():  # noqa E501
    assert repr(
        compare(
            base="",
            revision=" 	",
            results="html_page")
    ), 'Base: "Empty"; Revision: "Consecutive separators"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_empty_phrase():  # noqa E501
    assert repr(
        compare(
            base="",
            revision="a tabby cat",
            results="html_page")
    ), 'Base: "Empty"; Revision: "Phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_empty_separator_at_start_of_phrase():  # noqa E501
    assert repr(
        compare(
            base="",
            revision=" a tabby cat",
            results="html_page")
    ), 'Base: "Empty"; Revision: "Separator at start of phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_empty_separator_at_end_of_phrase():  # noqa E501
    assert repr(
        compare(
            base="",
            revision="a tabby cat ",
            results="html_page")
    ), 'Base: "Empty"; Revision: "Separator at end of phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_empty_separators_at_start_and_end_of_phrase():  # noqa E501
    assert repr(
        compare(
            base="",
            revision=" a tabby cat ",
            results="html_page")
    ), 'Base: "Empty"; Revision: "Separators at start and end of phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_empty_two_separators_at_start_of_phrase():  # noqa E501
    assert repr(
        compare(
            base="",
            revision="  a tabby cat",
            results="html_page")
    ), 'Base: "Empty"; Revision: "Two separators at start of phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_empty_two_separators_at_end_of_phrase():  # noqa E501
    assert repr(
        compare(
            base="",
            revision="a tabby cat  ",
            results="html_page")
    ), 'Base: "Empty"; Revision: "Two separators at end of phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_empty_two_separators_at_start_and_end_of_phrase():  # noqa E501
    assert repr(
        compare(
            base="",
            revision="  a tabby cat  ",
            results="html_page")
    ), 'Base: "Empty"; Revision: "Two separators at start and end of phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_empty_repeating_phrase():  # noqa E501
    assert repr(
        compare(
            base="",
            revision="a tabby cat and another tabby cat",
            results="html_page")
    ), 'Base: "Empty"; Revision: "Repeating phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_content_empty():  # noqa E501
    assert repr(
        compare(
            base="cat",
            revision="",
            results="html_page")
    ), 'Base: "Content"; Revision: "Empty"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_content_content():  # noqa E501
    assert repr(
        compare(
            base="cat",
            revision="cat",
            results="html_page")
    ), 'Base: "Content"; Revision: "Content"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_content_alternate_content():  # noqa E501
    assert repr(
        compare(
            base="cat",
            revision="tabby",
            results="html_page")
    ), 'Base: "Content"; Revision: "Alternate content"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_content_separator():  # noqa E501
    assert repr(
        compare(
            base="cat",
            revision=" ",
            results="html_page")
    ), 'Base: "Content"; Revision: "Separator"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_content_alternate_separator():  # noqa E501
    assert repr(
        compare(
            base="cat",
            revision="	",
            results="html_page")
    ), 'Base: "Content"; Revision: "Alternate separator"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_content_separator_then_content():  # noqa E501
    assert repr(
        compare(
            base="cat",
            revision=" cat",
            results="html_page")
    ), 'Base: "Content"; Revision: "Separator then content"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_content_content_then_separator():  # noqa E501
    assert repr(
        compare(
            base="cat",
            revision="cat ",
            results="html_page")
    ), 'Base: "Content"; Revision: "Content then separator"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_content_separator_then_content_then_separator():  # noqa E501
    assert repr(
        compare(
            base="cat",
            revision=" cat ",
            results="html_page")
    ), 'Base: "Content"; Revision: "Separator then content then separator"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_content_consecutive_separators():  # noqa E501
    assert repr(
        compare(
            base="cat",
            revision=" 	",
            results="html_page")
    ), 'Base: "Content"; Revision: "Consecutive separators"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_content_phrase():  # noqa E501
    assert repr(
        compare(
            base="cat",
            revision="a tabby cat",
            results="html_page")
    ), 'Base: "Content"; Revision: "Phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_content_separator_at_start_of_phrase():  # noqa E501
    assert repr(
        compare(
            base="cat",
            revision=" a tabby cat",
            results="html_page")
    ), 'Base: "Content"; Revision: "Separator at start of phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_content_separator_at_end_of_phrase():  # noqa E501
    assert repr(
        compare(
            base="cat",
            revision="a tabby cat ",
            results="html_page")
    ), 'Base: "Content"; Revision: "Separator at end of phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_content_separators_at_start_and_end_of_phrase():  # noqa E501
    assert repr(
        compare(
            base="cat",
            revision=" a tabby cat ",
            results="html_page")
    ), 'Base: "Content"; Revision: "Separators at start and end of phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_content_two_separators_at_start_of_phrase():  # noqa E501
    assert repr(
        compare(
            base="cat",
            revision="  a tabby cat",
            results="html_page")
    ), 'Base: "Content"; Revision: "Two separators at start of phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_content_two_separators_at_end_of_phrase():  # noqa E501
    assert repr(
        compare(
            base="cat",
            revision="a tabby cat  ",
            results="html_page")
    ), 'Base: "Content"; Revision: "Two separators at end of phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_content_two_separators_at_start_and_end_of_phrase():  # noqa E501
    assert repr(
        compare(
            base="cat",
            revision="  a tabby cat  ",
            results="html_page")
    ), 'Base: "Content"; Revision: "Two separators at start and end of phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_content_repeating_phrase():  # noqa E501
    assert repr(
        compare(
            base="cat",
            revision="a tabby cat and another tabby cat",
            results="html_page")
    ), 'Base: "Content"; Revision: "Repeating phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_alternate_content_empty():  # noqa E501
    assert repr(
        compare(
            base="tabby",
            revision="",
            results="html_page")
    ), 'Base: "Alternate content"; Revision: "Empty"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_alternate_content_content():  # noqa E501
    assert repr(
        compare(
            base="tabby",
            revision="cat",
            results="html_page")
    ), 'Base: "Alternate content"; Revision: "Content"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_alternate_content_alternate_content():  # noqa E501
    assert repr(
        compare(
            base="tabby",
            revision="tabby",
            results="html_page")
    ), 'Base: "Alternate content"; Revision: "Alternate content"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_alternate_content_separator():  # noqa E501
    assert repr(
        compare(
            base="tabby",
            revision=" ",
            results="html_page")
    ), 'Base: "Alternate content"; Revision: "Separator"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_alternate_content_alternate_separator():  # noqa E501
    assert repr(
        compare(
            base="tabby",
            revision="	",
            results="html_page")
    ), 'Base: "Alternate content"; Revision: "Alternate separator"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_alternate_content_separator_then_content():  # noqa E501
    assert repr(
        compare(
            base="tabby",
            revision=" cat",
            results="html_page")
    ), 'Base: "Alternate content"; Revision: "Separator then content"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_alternate_content_content_then_separator():  # noqa E501
    assert repr(
        compare(
            base="tabby",
            revision="cat ",
            results="html_page")
    ), 'Base: "Alternate content"; Revision: "Content then separator"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_alternate_content_separator_then_content_then_separator():  # noqa E501
    assert repr(
        compare(
            base="tabby",
            revision=" cat ",
            results="html_page")
    ), 'Base: "Alternate content"; Revision: "Separator then content then separator"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_alternate_content_consecutive_separators():  # noqa E501
    assert repr(
        compare(
            base="tabby",
            revision=" 	",
            results="html_page")
    ), 'Base: "Alternate content"; Revision: "Consecutive separators"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_alternate_content_phrase():  # noqa E501
    assert repr(
        compare(
            base="tabby",
            revision="a tabby cat",
            results="html_page")
    ), 'Base: "Alternate content"; Revision: "Phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_alternate_content_separator_at_start_of_phrase():  # noqa E501
    assert repr(
        compare(
            base="tabby",
            revision=" a tabby cat",
            results="html_page")
    ), 'Base: "Alternate content"; Revision: "Separator at start of phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_alternate_content_separator_at_end_of_phrase():  # noqa E501
    assert repr(
        compare(
            base="tabby",
            revision="a tabby cat ",
            results="html_page")
    ), 'Base: "Alternate content"; Revision: "Separator at end of phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_alternate_content_separators_at_start_and_end_of_phrase():  # noqa E501
    assert repr(
        compare(
            base="tabby",
            revision=" a tabby cat ",
            results="html_page")
    ), 'Base: "Alternate content"; Revision: "Separators at start and end of phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_alternate_content_two_separators_at_start_of_phrase():  # noqa E501
    assert repr(
        compare(
            base="tabby",
            revision="  a tabby cat",
            results="html_page")
    ), 'Base: "Alternate content"; Revision: "Two separators at start of phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_alternate_content_two_separators_at_end_of_phrase():  # noqa E501
    assert repr(
        compare(
            base="tabby",
            revision="a tabby cat  ",
            results="html_page")
    ), 'Base: "Alternate content"; Revision: "Two separators at end of phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_alternate_content_two_separators_at_start_and_end_of_phrase():  # noqa E501
    assert repr(
        compare(
            base="tabby",
            revision="  a tabby cat  ",
            results="html_page")
    ), 'Base: "Alternate content"; Revision: "Two separators at start and end of phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_alternate_content_repeating_phrase():  # noqa E501
    assert repr(
        compare(
            base="tabby",
            revision="a tabby cat and another tabby cat",
            results="html_page")
    ), 'Base: "Alternate content"; Revision: "Repeating phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_separator_empty():  # noqa E501
    assert repr(
        compare(
            base=" ",
            revision="",
            results="html_page")
    ), 'Base: "Separator"; Revision: "Empty"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_separator_content():  # noqa E501
    assert repr(
        compare(
            base=" ",
            revision="cat",
            results="html_page")
    ), 'Base: "Separator"; Revision: "Content"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_separator_alternate_content():  # noqa E501
    assert repr(
        compare(
            base=" ",
            revision="tabby",
            results="html_page")
    ), 'Base: "Separator"; Revision: "Alternate content"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_separator_separator():  # noqa E501
    assert repr(
        compare(
            base=" ",
            revision=" ",
            results="html_page")
    ), 'Base: "Separator"; Revision: "Separator"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_separator_alternate_separator():  # noqa E501
    assert repr(
        compare(
            base=" ",
            revision="	",
            results="html_page")
    ), 'Base: "Separator"; Revision: "Alternate separator"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_separator_separator_then_content():  # noqa E501
    assert repr(
        compare(
            base=" ",
            revision=" cat",
            results="html_page")
    ), 'Base: "Separator"; Revision: "Separator then content"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_separator_content_then_separator():  # noqa E501
    assert repr(
        compare(
            base=" ",
            revision="cat ",
            results="html_page")
    ), 'Base: "Separator"; Revision: "Content then separator"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_separator_separator_then_content_then_separator():  # noqa E501
    assert repr(
        compare(
            base=" ",
            revision=" cat ",
            results="html_page")
    ), 'Base: "Separator"; Revision: "Separator then content then separator"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_separator_consecutive_separators():  # noqa E501
    assert repr(
        compare(
            base=" ",
            revision=" 	",
            results="html_page")
    ), 'Base: "Separator"; Revision: "Consecutive separators"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_separator_phrase():  # noqa E501
    assert repr(
        compare(
            base=" ",
            revision="a tabby cat",
            results="html_page")
    ), 'Base: "Separator"; Revision: "Phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_separator_separator_at_start_of_phrase():  # noqa E501
    assert repr(
        compare(
            base=" ",
            revision=" a tabby cat",
            results="html_page")
    ), 'Base: "Separator"; Revision: "Separator at start of phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_separator_separator_at_end_of_phrase():  # noqa E501
    assert repr(
        compare(
            base=" ",
            revision="a tabby cat ",
            results="html_page")
    ), 'Base: "Separator"; Revision: "Separator at end of phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_separator_separators_at_start_and_end_of_phrase():  # noqa E501
    assert repr(
        compare(
            base=" ",
            revision=" a tabby cat ",
            results="html_page")
    ), 'Base: "Separator"; Revision: "Separators at start and end of phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_separator_two_separators_at_start_of_phrase():  # noqa E501
    assert repr(
        compare(
            base=" ",
            revision="  a tabby cat",
            results="html_page")
    ), 'Base: "Separator"; Revision: "Two separators at start of phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_separator_two_separators_at_end_of_phrase():  # noqa E501
    assert repr(
        compare(
            base=" ",
            revision="a tabby cat  ",
            results="html_page")
    ), 'Base: "Separator"; Revision: "Two separators at end of phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_separator_two_separators_at_start_and_end_of_phrase():  # noqa E501
    assert repr(
        compare(
            base=" ",
            revision="  a tabby cat  ",
            results="html_page")
    ), 'Base: "Separator"; Revision: "Two separators at start and end of phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_separator_repeating_phrase():  # noqa E501
    assert repr(
        compare(
            base=" ",
            revision="a tabby cat and another tabby cat",
            results="html_page")
    ), 'Base: "Separator"; Revision: "Repeating phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_alternate_separator_empty():  # noqa E501
    assert repr(
        compare(
            base="	",
            revision="",
            results="html_page")
    ), 'Base: "Alternate separator"; Revision: "Empty"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_alternate_separator_content():  # noqa E501
    assert repr(
        compare(
            base="	",
            revision="cat",
            results="html_page")
    ), 'Base: "Alternate separator"; Revision: "Content"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_alternate_separator_alternate_content():  # noqa E501
    assert repr(
        compare(
            base="	",
            revision="tabby",
            results="html_page")
    ), 'Base: "Alternate separator"; Revision: "Alternate content"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_alternate_separator_separator():  # noqa E501
    assert repr(
        compare(
            base="	",
            revision=" ",
            results="html_page")
    ), 'Base: "Alternate separator"; Revision: "Separator"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_alternate_separator_alternate_separator():  # noqa E501
    assert repr(
        compare(
            base="	",
            revision="	",
            results="html_page")
    ), 'Base: "Alternate separator"; Revision: "Alternate separator"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_alternate_separator_separator_then_content():  # noqa E501
    assert repr(
        compare(
            base="	",
            revision=" cat",
            results="html_page")
    ), 'Base: "Alternate separator"; Revision: "Separator then content"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_alternate_separator_content_then_separator():  # noqa E501
    assert repr(
        compare(
            base="	",
            revision="cat ",
            results="html_page")
    ), 'Base: "Alternate separator"; Revision: "Content then separator"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_alternate_separator_separator_then_content_then_separator():  # noqa E501
    assert repr(
        compare(
            base="	",
            revision=" cat ",
            results="html_page")
    ), 'Base: "Alternate separator"; Revision: "Separator then content then separator"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_alternate_separator_consecutive_separators():  # noqa E501
    assert repr(
        compare(
            base="	",
            revision=" 	",
            results="html_page")
    ), 'Base: "Alternate separator"; Revision: "Consecutive separators"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_alternate_separator_phrase():  # noqa E501
    assert repr(
        compare(
            base="	",
            revision="a tabby cat",
            results="html_page")
    ), 'Base: "Alternate separator"; Revision: "Phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_alternate_separator_separator_at_start_of_phrase():  # noqa E501
    assert repr(
        compare(
            base="	",
            revision=" a tabby cat",
            results="html_page")
    ), 'Base: "Alternate separator"; Revision: "Separator at start of phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_alternate_separator_separator_at_end_of_phrase():  # noqa E501
    assert repr(
        compare(
            base="	",
            revision="a tabby cat ",
            results="html_page")
    ), 'Base: "Alternate separator"; Revision: "Separator at end of phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_alternate_separator_separators_at_start_and_end_of_phrase():  # noqa E501
    assert repr(
        compare(
            base="	",
            revision=" a tabby cat ",
            results="html_page")
    ), 'Base: "Alternate separator"; Revision: "Separators at start and end of phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_alternate_separator_two_separators_at_start_of_phrase():  # noqa E501
    assert repr(
        compare(
            base="	",
            revision="  a tabby cat",
            results="html_page")
    ), 'Base: "Alternate separator"; Revision: "Two separators at start of phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_alternate_separator_two_separators_at_end_of_phrase():  # noqa E501
    assert repr(
        compare(
            base="	",
            revision="a tabby cat  ",
            results="html_page")
    ), 'Base: "Alternate separator"; Revision: "Two separators at end of phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_alternate_separator_two_separators_at_start_and_end_of_phrase():  # noqa E501
    assert repr(
        compare(
            base="	",
            revision="  a tabby cat  ",
            results="html_page")
    ), 'Base: "Alternate separator"; Revision: "Two separators at start and end of phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_alternate_separator_repeating_phrase():  # noqa E501
    assert repr(
        compare(
            base="	",
            revision="a tabby cat and another tabby cat",
            results="html_page")
    ), 'Base: "Alternate separator"; Revision: "Repeating phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_separator_then_content_empty():  # noqa E501
    assert repr(
        compare(
            base=" cat",
            revision="",
            results="html_page")
    ), 'Base: "Separator then content"; Revision: "Empty"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_separator_then_content_content():  # noqa E501
    assert repr(
        compare(
            base=" cat",
            revision="cat",
            results="html_page")
    ), 'Base: "Separator then content"; Revision: "Content"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_separator_then_content_alternate_content():  # noqa E501
    assert repr(
        compare(
            base=" cat",
            revision="tabby",
            results="html_page")
    ), 'Base: "Separator then content"; Revision: "Alternate content"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_separator_then_content_separator():  # noqa E501
    assert repr(
        compare(
            base=" cat",
            revision=" ",
            results="html_page")
    ), 'Base: "Separator then content"; Revision: "Separator"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_separator_then_content_alternate_separator():  # noqa E501
    assert repr(
        compare(
            base=" cat",
            revision="	",
            results="html_page")
    ), 'Base: "Separator then content"; Revision: "Alternate separator"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_separator_then_content_separator_then_content():  # noqa E501
    assert repr(
        compare(
            base=" cat",
            revision=" cat",
            results="html_page")
    ), 'Base: "Separator then content"; Revision: "Separator then content"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_separator_then_content_content_then_separator():  # noqa E501
    assert repr(
        compare(
            base=" cat",
            revision="cat ",
            results="html_page")
    ), 'Base: "Separator then content"; Revision: "Content then separator"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_separator_then_content_separator_then_content_then_separator():  # noqa E501
    assert repr(
        compare(
            base=" cat",
            revision=" cat ",
            results="html_page")
    ), 'Base: "Separator then content"; Revision: "Separator then content then separator"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_separator_then_content_consecutive_separators():  # noqa E501
    assert repr(
        compare(
            base=" cat",
            revision=" 	",
            results="html_page")
    ), 'Base: "Separator then content"; Revision: "Consecutive separators"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_separator_then_content_phrase():  # noqa E501
    assert repr(
        compare(
            base=" cat",
            revision="a tabby cat",
            results="html_page")
    ), 'Base: "Separator then content"; Revision: "Phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_separator_then_content_separator_at_start_of_phrase():  # noqa E501
    assert repr(
        compare(
            base=" cat",
            revision=" a tabby cat",
            results="html_page")
    ), 'Base: "Separator then content"; Revision: "Separator at start of phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_separator_then_content_separator_at_end_of_phrase():  # noqa E501
    assert repr(
        compare(
            base=" cat",
            revision="a tabby cat ",
            results="html_page")
    ), 'Base: "Separator then content"; Revision: "Separator at end of phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_separator_then_content_separators_at_start_and_end_of_phrase():  # noqa E501
    assert repr(
        compare(
            base=" cat",
            revision=" a tabby cat ",
            results="html_page")
    ), 'Base: "Separator then content"; Revision: "Separators at start and end of phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_separator_then_content_two_separators_at_start_of_phrase():  # noqa E501
    assert repr(
        compare(
            base=" cat",
            revision="  a tabby cat",
            results="html_page")
    ), 'Base: "Separator then content"; Revision: "Two separators at start of phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_separator_then_content_two_separators_at_end_of_phrase():  # noqa E501
    assert repr(
        compare(
            base=" cat",
            revision="a tabby cat  ",
            results="html_page")
    ), 'Base: "Separator then content"; Revision: "Two separators at end of phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_separator_then_content_two_separators_at_start_and_end_of_phrase():  # noqa E501
    assert repr(
        compare(
            base=" cat",
            revision="  a tabby cat  ",
            results="html_page")
    ), 'Base: "Separator then content"; Revision: "Two separators at start and end of phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_separator_then_content_repeating_phrase():  # noqa E501
    assert repr(
        compare(
            base=" cat",
            revision="a tabby cat and another tabby cat",
            results="html_page")
    ), 'Base: "Separator then content"; Revision: "Repeating phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_content_then_separator_empty():  # noqa E501
    assert repr(
        compare(
            base="cat ",
            revision="",
            results="html_page")
    ), 'Base: "Content then separator"; Revision: "Empty"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_content_then_separator_content():  # noqa E501
    assert repr(
        compare(
            base="cat ",
            revision="cat",
            results="html_page")
    ), 'Base: "Content then separator"; Revision: "Content"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_content_then_separator_alternate_content():  # noqa E501
    assert repr(
        compare(
            base="cat ",
            revision="tabby",
            results="html_page")
    ), 'Base: "Content then separator"; Revision: "Alternate content"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_content_then_separator_separator():  # noqa E501
    assert repr(
        compare(
            base="cat ",
            revision=" ",
            results="html_page")
    ), 'Base: "Content then separator"; Revision: "Separator"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_content_then_separator_alternate_separator():  # noqa E501
    assert repr(
        compare(
            base="cat ",
            revision="	",
            results="html_page")
    ), 'Base: "Content then separator"; Revision: "Alternate separator"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_content_then_separator_separator_then_content():  # noqa E501
    assert repr(
        compare(
            base="cat ",
            revision=" cat",
            results="html_page")
    ), 'Base: "Content then separator"; Revision: "Separator then content"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_content_then_separator_content_then_separator():  # noqa E501
    assert repr(
        compare(
            base="cat ",
            revision="cat ",
            results="html_page")
    ), 'Base: "Content then separator"; Revision: "Content then separator"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_content_then_separator_separator_then_content_then_separator():  # noqa E501
    assert repr(
        compare(
            base="cat ",
            revision=" cat ",
            results="html_page")
    ), 'Base: "Content then separator"; Revision: "Separator then content then separator"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_content_then_separator_consecutive_separators():  # noqa E501
    assert repr(
        compare(
            base="cat ",
            revision=" 	",
            results="html_page")
    ), 'Base: "Content then separator"; Revision: "Consecutive separators"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_content_then_separator_phrase():  # noqa E501
    assert repr(
        compare(
            base="cat ",
            revision="a tabby cat",
            results="html_page")
    ), 'Base: "Content then separator"; Revision: "Phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_content_then_separator_separator_at_start_of_phrase():  # noqa E501
    assert repr(
        compare(
            base="cat ",
            revision=" a tabby cat",
            results="html_page")
    ), 'Base: "Content then separator"; Revision: "Separator at start of phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_content_then_separator_separator_at_end_of_phrase():  # noqa E501
    assert repr(
        compare(
            base="cat ",
            revision="a tabby cat ",
            results="html_page")
    ), 'Base: "Content then separator"; Revision: "Separator at end of phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_content_then_separator_separators_at_start_and_end_of_phrase():  # noqa E501
    assert repr(
        compare(
            base="cat ",
            revision=" a tabby cat ",
            results="html_page")
    ), 'Base: "Content then separator"; Revision: "Separators at start and end of phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_content_then_separator_two_separators_at_start_of_phrase():  # noqa E501
    assert repr(
        compare(
            base="cat ",
            revision="  a tabby cat",
            results="html_page")
    ), 'Base: "Content then separator"; Revision: "Two separators at start of phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_content_then_separator_two_separators_at_end_of_phrase():  # noqa E501
    assert repr(
        compare(
            base="cat ",
            revision="a tabby cat  ",
            results="html_page")
    ), 'Base: "Content then separator"; Revision: "Two separators at end of phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_content_then_separator_two_separators_at_start_and_end_of_phrase():  # noqa E501
    assert repr(
        compare(
            base="cat ",
            revision="  a tabby cat  ",
            results="html_page")
    ), 'Base: "Content then separator"; Revision: "Two separators at start and end of phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_content_then_separator_repeating_phrase():  # noqa E501
    assert repr(
        compare(
            base="cat ",
            revision="a tabby cat and another tabby cat",
            results="html_page")
    ), 'Base: "Content then separator"; Revision: "Repeating phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_separator_then_content_then_separator_empty():  # noqa E501
    assert repr(
        compare(
            base=" cat ",
            revision="",
            results="html_page")
    ), 'Base: "Separator then content then separator"; Revision: "Empty"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_separator_then_content_then_separator_content():  # noqa E501
    assert repr(
        compare(
            base=" cat ",
            revision="cat",
            results="html_page")
    ), 'Base: "Separator then content then separator"; Revision: "Content"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_separator_then_content_then_separator_alternate_content():  # noqa E501
    assert repr(
        compare(
            base=" cat ",
            revision="tabby",
            results="html_page")
    ), 'Base: "Separator then content then separator"; Revision: "Alternate content"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_separator_then_content_then_separator_separator():  # noqa E501
    assert repr(
        compare(
            base=" cat ",
            revision=" ",
            results="html_page")
    ), 'Base: "Separator then content then separator"; Revision: "Separator"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_separator_then_content_then_separator_alternate_separator():  # noqa E501
    assert repr(
        compare(
            base=" cat ",
            revision="	",
            results="html_page")
    ), 'Base: "Separator then content then separator"; Revision: "Alternate separator"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_separator_then_content_then_separator_separator_then_content():  # noqa E501
    assert repr(
        compare(
            base=" cat ",
            revision=" cat",
            results="html_page")
    ), 'Base: "Separator then content then separator"; Revision: "Separator then content"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_separator_then_content_then_separator_content_then_separator():  # noqa E501
    assert repr(
        compare(
            base=" cat ",
            revision="cat ",
            results="html_page")
    ), 'Base: "Separator then content then separator"; Revision: "Content then separator"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_separator_then_content_then_separator_separator_then_content_then_separator():  # noqa E501
    assert repr(
        compare(
            base=" cat ",
            revision=" cat ",
            results="html_page")
    ), 'Base: "Separator then content then separator"; Revision: "Separator then content then separator"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_separator_then_content_then_separator_consecutive_separators():  # noqa E501
    assert repr(
        compare(
            base=" cat ",
            revision=" 	",
            results="html_page")
    ), 'Base: "Separator then content then separator"; Revision: "Consecutive separators"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_separator_then_content_then_separator_phrase():  # noqa E501
    assert repr(
        compare(
            base=" cat ",
            revision="a tabby cat",
            results="html_page")
    ), 'Base: "Separator then content then separator"; Revision: "Phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_separator_then_content_then_separator_separator_at_start_of_phrase():  # noqa E501
    assert repr(
        compare(
            base=" cat ",
            revision=" a tabby cat",
            results="html_page")
    ), 'Base: "Separator then content then separator"; Revision: "Separator at start of phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_separator_then_content_then_separator_separator_at_end_of_phrase():  # noqa E501
    assert repr(
        compare(
            base=" cat ",
            revision="a tabby cat ",
            results="html_page")
    ), 'Base: "Separator then content then separator"; Revision: "Separator at end of phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_separator_then_content_then_separator_separators_at_start_and_end_of_phrase():  # noqa E501
    assert repr(
        compare(
            base=" cat ",
            revision=" a tabby cat ",
            results="html_page")
    ), 'Base: "Separator then content then separator"; Revision: "Separators at start and end of phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_separator_then_content_then_separator_two_separators_at_start_of_phrase():  # noqa E501
    assert repr(
        compare(
            base=" cat ",
            revision="  a tabby cat",
            results="html_page")
    ), 'Base: "Separator then content then separator"; Revision: "Two separators at start of phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_separator_then_content_then_separator_two_separators_at_end_of_phrase():  # noqa E501
    assert repr(
        compare(
            base=" cat ",
            revision="a tabby cat  ",
            results="html_page")
    ), 'Base: "Separator then content then separator"; Revision: "Two separators at end of phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_separator_then_content_then_separator_two_separators_at_start_and_end_of_phrase():  # noqa E501
    assert repr(
        compare(
            base=" cat ",
            revision="  a tabby cat  ",
            results="html_page")
    ), 'Base: "Separator then content then separator"; Revision: "Two separators at start and end of phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_separator_then_content_then_separator_repeating_phrase():  # noqa E501
    assert repr(
        compare(
            base=" cat ",
            revision="a tabby cat and another tabby cat",
            results="html_page")
    ), 'Base: "Separator then content then separator"; Revision: "Repeating phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_consecutive_separators_empty():  # noqa E501
    assert repr(
        compare(
            base=" 	",
            revision="",
            results="html_page")
    ), 'Base: "Consecutive separators"; Revision: "Empty"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_consecutive_separators_content():  # noqa E501
    assert repr(
        compare(
            base=" 	",
            revision="cat",
            results="html_page")
    ), 'Base: "Consecutive separators"; Revision: "Content"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_consecutive_separators_alternate_content():  # noqa E501
    assert repr(
        compare(
            base=" 	",
            revision="tabby",
            results="html_page")
    ), 'Base: "Consecutive separators"; Revision: "Alternate content"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_consecutive_separators_separator():  # noqa E501
    assert repr(
        compare(
            base=" 	",
            revision=" ",
            results="html_page")
    ), 'Base: "Consecutive separators"; Revision: "Separator"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_consecutive_separators_alternate_separator():  # noqa E501
    assert repr(
        compare(
            base=" 	",
            revision="	",
            results="html_page")
    ), 'Base: "Consecutive separators"; Revision: "Alternate separator"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_consecutive_separators_separator_then_content():  # noqa E501
    assert repr(
        compare(
            base=" 	",
            revision=" cat",
            results="html_page")
    ), 'Base: "Consecutive separators"; Revision: "Separator then content"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_consecutive_separators_content_then_separator():  # noqa E501
    assert repr(
        compare(
            base=" 	",
            revision="cat ",
            results="html_page")
    ), 'Base: "Consecutive separators"; Revision: "Content then separator"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_consecutive_separators_separator_then_content_then_separator():  # noqa E501
    assert repr(
        compare(
            base=" 	",
            revision=" cat ",
            results="html_page")
    ), 'Base: "Consecutive separators"; Revision: "Separator then content then separator"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_consecutive_separators_consecutive_separators():  # noqa E501
    assert repr(
        compare(
            base=" 	",
            revision=" 	",
            results="html_page")
    ), 'Base: "Consecutive separators"; Revision: "Consecutive separators"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_consecutive_separators_phrase():  # noqa E501
    assert repr(
        compare(
            base=" 	",
            revision="a tabby cat",
            results="html_page")
    ), 'Base: "Consecutive separators"; Revision: "Phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_consecutive_separators_separator_at_start_of_phrase():  # noqa E501
    assert repr(
        compare(
            base=" 	",
            revision=" a tabby cat",
            results="html_page")
    ), 'Base: "Consecutive separators"; Revision: "Separator at start of phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_consecutive_separators_separator_at_end_of_phrase():  # noqa E501
    assert repr(
        compare(
            base=" 	",
            revision="a tabby cat ",
            results="html_page")
    ), 'Base: "Consecutive separators"; Revision: "Separator at end of phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_consecutive_separators_separators_at_start_and_end_of_phrase():  # noqa E501
    assert repr(
        compare(
            base=" 	",
            revision=" a tabby cat ",
            results="html_page")
    ), 'Base: "Consecutive separators"; Revision: "Separators at start and end of phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_consecutive_separators_two_separators_at_start_of_phrase():  # noqa E501
    assert repr(
        compare(
            base=" 	",
            revision="  a tabby cat",
            results="html_page")
    ), 'Base: "Consecutive separators"; Revision: "Two separators at start of phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_consecutive_separators_two_separators_at_end_of_phrase():  # noqa E501
    assert repr(
        compare(
            base=" 	",
            revision="a tabby cat  ",
            results="html_page")
    ), 'Base: "Consecutive separators"; Revision: "Two separators at end of phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_consecutive_separators_two_separators_at_start_and_end_of_phrase():  # noqa E501
    assert repr(
        compare(
            base=" 	",
            revision="  a tabby cat  ",
            results="html_page")
    ), 'Base: "Consecutive separators"; Revision: "Two separators at start and end of phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_consecutive_separators_repeating_phrase():  # noqa E501
    assert repr(
        compare(
            base=" 	",
            revision="a tabby cat and another tabby cat",
            results="html_page")
    ), 'Base: "Consecutive separators"; Revision: "Repeating phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_phrase_empty():  # noqa E501
    assert repr(
        compare(
            base="a tabby cat",
            revision="",
            results="html_page")
    ), 'Base: "Phrase"; Revision: "Empty"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_phrase_content():  # noqa E501
    assert repr(
        compare(
            base="a tabby cat",
            revision="cat",
            results="html_page")
    ), 'Base: "Phrase"; Revision: "Content"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_phrase_alternate_content():  # noqa E501
    assert repr(
        compare(
            base="a tabby cat",
            revision="tabby",
            results="html_page")
    ), 'Base: "Phrase"; Revision: "Alternate content"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_phrase_separator():  # noqa E501
    assert repr(
        compare(
            base="a tabby cat",
            revision=" ",
            results="html_page")
    ), 'Base: "Phrase"; Revision: "Separator"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_phrase_alternate_separator():  # noqa E501
    assert repr(
        compare(
            base="a tabby cat",
            revision="	",
            results="html_page")
    ), 'Base: "Phrase"; Revision: "Alternate separator"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_phrase_separator_then_content():  # noqa E501
    assert repr(
        compare(
            base="a tabby cat",
            revision=" cat",
            results="html_page")
    ), 'Base: "Phrase"; Revision: "Separator then content"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_phrase_content_then_separator():  # noqa E501
    assert repr(
        compare(
            base="a tabby cat",
            revision="cat ",
            results="html_page")
    ), 'Base: "Phrase"; Revision: "Content then separator"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_phrase_separator_then_content_then_separator():  # noqa E501
    assert repr(
        compare(
            base="a tabby cat",
            revision=" cat ",
            results="html_page")
    ), 'Base: "Phrase"; Revision: "Separator then content then separator"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_phrase_consecutive_separators():  # noqa E501
    assert repr(
        compare(
            base="a tabby cat",
            revision=" 	",
            results="html_page")
    ), 'Base: "Phrase"; Revision: "Consecutive separators"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_phrase_phrase():  # noqa E501
    assert repr(
        compare(
            base="a tabby cat",
            revision="a tabby cat",
            results="html_page")
    ), 'Base: "Phrase"; Revision: "Phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_phrase_separator_at_start_of_phrase():  # noqa E501
    assert repr(
        compare(
            base="a tabby cat",
            revision=" a tabby cat",
            results="html_page")
    ), 'Base: "Phrase"; Revision: "Separator at start of phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_phrase_separator_at_end_of_phrase():  # noqa E501
    assert repr(
        compare(
            base="a tabby cat",
            revision="a tabby cat ",
            results="html_page")
    ), 'Base: "Phrase"; Revision: "Separator at end of phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_phrase_separators_at_start_and_end_of_phrase():  # noqa E501
    assert repr(
        compare(
            base="a tabby cat",
            revision=" a tabby cat ",
            results="html_page")
    ), 'Base: "Phrase"; Revision: "Separators at start and end of phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_phrase_two_separators_at_start_of_phrase():  # noqa E501
    assert repr(
        compare(
            base="a tabby cat",
            revision="  a tabby cat",
            results="html_page")
    ), 'Base: "Phrase"; Revision: "Two separators at start of phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_phrase_two_separators_at_end_of_phrase():  # noqa E501
    assert repr(
        compare(
            base="a tabby cat",
            revision="a tabby cat  ",
            results="html_page")
    ), 'Base: "Phrase"; Revision: "Two separators at end of phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_phrase_two_separators_at_start_and_end_of_phrase():  # noqa E501
    assert repr(
        compare(
            base="a tabby cat",
            revision="  a tabby cat  ",
            results="html_page")
    ), 'Base: "Phrase"; Revision: "Two separators at start and end of phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_phrase_repeating_phrase():  # noqa E501
    assert repr(
        compare(
            base="a tabby cat",
            revision="a tabby cat and another tabby cat",
            results="html_page")
    ), 'Base: "Phrase"; Revision: "Repeating phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_separator_at_start_of_phrase_empty():  # noqa E501
    assert repr(
        compare(
            base=" a tabby cat",
            revision="",
            results="html_page")
    ), 'Base: "Separator at start of phrase"; Revision: "Empty"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_separator_at_start_of_phrase_content():  # noqa E501
    assert repr(
        compare(
            base=" a tabby cat",
            revision="cat",
            results="html_page")
    ), 'Base: "Separator at start of phrase"; Revision: "Content"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_separator_at_start_of_phrase_alternate_content():  # noqa E501
    assert repr(
        compare(
            base=" a tabby cat",
            revision="tabby",
            results="html_page")
    ), 'Base: "Separator at start of phrase"; Revision: "Alternate content"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_separator_at_start_of_phrase_separator():  # noqa E501
    assert repr(
        compare(
            base=" a tabby cat",
            revision=" ",
            results="html_page")
    ), 'Base: "Separator at start of phrase"; Revision: "Separator"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_separator_at_start_of_phrase_alternate_separator():  # noqa E501
    assert repr(
        compare(
            base=" a tabby cat",
            revision="	",
            results="html_page")
    ), 'Base: "Separator at start of phrase"; Revision: "Alternate separator"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_separator_at_start_of_phrase_separator_then_content():  # noqa E501
    assert repr(
        compare(
            base=" a tabby cat",
            revision=" cat",
            results="html_page")
    ), 'Base: "Separator at start of phrase"; Revision: "Separator then content"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_separator_at_start_of_phrase_content_then_separator():  # noqa E501
    assert repr(
        compare(
            base=" a tabby cat",
            revision="cat ",
            results="html_page")
    ), 'Base: "Separator at start of phrase"; Revision: "Content then separator"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_separator_at_start_of_phrase_separator_then_content_then_separator():  # noqa E501
    assert repr(
        compare(
            base=" a tabby cat",
            revision=" cat ",
            results="html_page")
    ), 'Base: "Separator at start of phrase"; Revision: "Separator then content then separator"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_separator_at_start_of_phrase_consecutive_separators():  # noqa E501
    assert repr(
        compare(
            base=" a tabby cat",
            revision=" 	",
            results="html_page")
    ), 'Base: "Separator at start of phrase"; Revision: "Consecutive separators"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_separator_at_start_of_phrase_phrase():  # noqa E501
    assert repr(
        compare(
            base=" a tabby cat",
            revision="a tabby cat",
            results="html_page")
    ), 'Base: "Separator at start of phrase"; Revision: "Phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_separator_at_start_of_phrase_separator_at_start_of_phrase():  # noqa E501
    assert repr(
        compare(
            base=" a tabby cat",
            revision=" a tabby cat",
            results="html_page")
    ), 'Base: "Separator at start of phrase"; Revision: "Separator at start of phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_separator_at_start_of_phrase_separator_at_end_of_phrase():  # noqa E501
    assert repr(
        compare(
            base=" a tabby cat",
            revision="a tabby cat ",
            results="html_page")
    ), 'Base: "Separator at start of phrase"; Revision: "Separator at end of phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_separator_at_start_of_phrase_separators_at_start_and_end_of_phrase():  # noqa E501
    assert repr(
        compare(
            base=" a tabby cat",
            revision=" a tabby cat ",
            results="html_page")
    ), 'Base: "Separator at start of phrase"; Revision: "Separators at start and end of phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_separator_at_start_of_phrase_two_separators_at_start_of_phrase():  # noqa E501
    assert repr(
        compare(
            base=" a tabby cat",
            revision="  a tabby cat",
            results="html_page")
    ), 'Base: "Separator at start of phrase"; Revision: "Two separators at start of phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_separator_at_start_of_phrase_two_separators_at_end_of_phrase():  # noqa E501
    assert repr(
        compare(
            base=" a tabby cat",
            revision="a tabby cat  ",
            results="html_page")
    ), 'Base: "Separator at start of phrase"; Revision: "Two separators at end of phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_separator_at_start_of_phrase_two_separators_at_start_and_end_of_phrase():  # noqa E501
    assert repr(
        compare(
            base=" a tabby cat",
            revision="  a tabby cat  ",
            results="html_page")
    ), 'Base: "Separator at start of phrase"; Revision: "Two separators at start and end of phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_separator_at_start_of_phrase_repeating_phrase():  # noqa E501
    assert repr(
        compare(
            base=" a tabby cat",
            revision="a tabby cat and another tabby cat",
            results="html_page")
    ), 'Base: "Separator at start of phrase"; Revision: "Repeating phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_separator_at_end_of_phrase_empty():  # noqa E501
    assert repr(
        compare(
            base="a tabby cat ",
            revision="",
            results="html_page")
    ), 'Base: "Separator at end of phrase"; Revision: "Empty"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_separator_at_end_of_phrase_content():  # noqa E501
    assert repr(
        compare(
            base="a tabby cat ",
            revision="cat",
            results="html_page")
    ), 'Base: "Separator at end of phrase"; Revision: "Content"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_separator_at_end_of_phrase_alternate_content():  # noqa E501
    assert repr(
        compare(
            base="a tabby cat ",
            revision="tabby",
            results="html_page")
    ), 'Base: "Separator at end of phrase"; Revision: "Alternate content"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_separator_at_end_of_phrase_separator():  # noqa E501
    assert repr(
        compare(
            base="a tabby cat ",
            revision=" ",
            results="html_page")
    ), 'Base: "Separator at end of phrase"; Revision: "Separator"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_separator_at_end_of_phrase_alternate_separator():  # noqa E501
    assert repr(
        compare(
            base="a tabby cat ",
            revision="	",
            results="html_page")
    ), 'Base: "Separator at end of phrase"; Revision: "Alternate separator"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_separator_at_end_of_phrase_separator_then_content():  # noqa E501
    assert repr(
        compare(
            base="a tabby cat ",
            revision=" cat",
            results="html_page")
    ), 'Base: "Separator at end of phrase"; Revision: "Separator then content"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_separator_at_end_of_phrase_content_then_separator():  # noqa E501
    assert repr(
        compare(
            base="a tabby cat ",
            revision="cat ",
            results="html_page")
    ), 'Base: "Separator at end of phrase"; Revision: "Content then separator"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_separator_at_end_of_phrase_separator_then_content_then_separator():  # noqa E501
    assert repr(
        compare(
            base="a tabby cat ",
            revision=" cat ",
            results="html_page")
    ), 'Base: "Separator at end of phrase"; Revision: "Separator then content then separator"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_separator_at_end_of_phrase_consecutive_separators():  # noqa E501
    assert repr(
        compare(
            base="a tabby cat ",
            revision=" 	",
            results="html_page")
    ), 'Base: "Separator at end of phrase"; Revision: "Consecutive separators"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_separator_at_end_of_phrase_phrase():  # noqa E501
    assert repr(
        compare(
            base="a tabby cat ",
            revision="a tabby cat",
            results="html_page")
    ), 'Base: "Separator at end of phrase"; Revision: "Phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_separator_at_end_of_phrase_separator_at_start_of_phrase():  # noqa E501
    assert repr(
        compare(
            base="a tabby cat ",
            revision=" a tabby cat",
            results="html_page")
    ), 'Base: "Separator at end of phrase"; Revision: "Separator at start of phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_separator_at_end_of_phrase_separator_at_end_of_phrase():  # noqa E501
    assert repr(
        compare(
            base="a tabby cat ",
            revision="a tabby cat ",
            results="html_page")
    ), 'Base: "Separator at end of phrase"; Revision: "Separator at end of phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_separator_at_end_of_phrase_separators_at_start_and_end_of_phrase():  # noqa E501
    assert repr(
        compare(
            base="a tabby cat ",
            revision=" a tabby cat ",
            results="html_page")
    ), 'Base: "Separator at end of phrase"; Revision: "Separators at start and end of phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_separator_at_end_of_phrase_two_separators_at_start_of_phrase():  # noqa E501
    assert repr(
        compare(
            base="a tabby cat ",
            revision="  a tabby cat",
            results="html_page")
    ), 'Base: "Separator at end of phrase"; Revision: "Two separators at start of phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_separator_at_end_of_phrase_two_separators_at_end_of_phrase():  # noqa E501
    assert repr(
        compare(
            base="a tabby cat ",
            revision="a tabby cat  ",
            results="html_page")
    ), 'Base: "Separator at end of phrase"; Revision: "Two separators at end of phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_separator_at_end_of_phrase_two_separators_at_start_and_end_of_phrase():  # noqa E501
    assert repr(
        compare(
            base="a tabby cat ",
            revision="  a tabby cat  ",
            results="html_page")
    ), 'Base: "Separator at end of phrase"; Revision: "Two separators at start and end of phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_separator_at_end_of_phrase_repeating_phrase():  # noqa E501
    assert repr(
        compare(
            base="a tabby cat ",
            revision="a tabby cat and another tabby cat",
            results="html_page")
    ), 'Base: "Separator at end of phrase"; Revision: "Repeating phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_separators_at_start_and_end_of_phrase_empty():  # noqa E501
    assert repr(
        compare(
            base=" a tabby cat ",
            revision="",
            results="html_page")
    ), 'Base: "Separators at start and end of phrase"; Revision: "Empty"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_separators_at_start_and_end_of_phrase_content():  # noqa E501
    assert repr(
        compare(
            base=" a tabby cat ",
            revision="cat",
            results="html_page")
    ), 'Base: "Separators at start and end of phrase"; Revision: "Content"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_separators_at_start_and_end_of_phrase_alternate_content():  # noqa E501
    assert repr(
        compare(
            base=" a tabby cat ",
            revision="tabby",
            results="html_page")
    ), 'Base: "Separators at start and end of phrase"; Revision: "Alternate content"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_separators_at_start_and_end_of_phrase_separator():  # noqa E501
    assert repr(
        compare(
            base=" a tabby cat ",
            revision=" ",
            results="html_page")
    ), 'Base: "Separators at start and end of phrase"; Revision: "Separator"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_separators_at_start_and_end_of_phrase_alternate_separator():  # noqa E501
    assert repr(
        compare(
            base=" a tabby cat ",
            revision="	",
            results="html_page")
    ), 'Base: "Separators at start and end of phrase"; Revision: "Alternate separator"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_separators_at_start_and_end_of_phrase_separator_then_content():  # noqa E501
    assert repr(
        compare(
            base=" a tabby cat ",
            revision=" cat",
            results="html_page")
    ), 'Base: "Separators at start and end of phrase"; Revision: "Separator then content"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_separators_at_start_and_end_of_phrase_content_then_separator():  # noqa E501
    assert repr(
        compare(
            base=" a tabby cat ",
            revision="cat ",
            results="html_page")
    ), 'Base: "Separators at start and end of phrase"; Revision: "Content then separator"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_separators_at_start_and_end_of_phrase_separator_then_content_then_separator():  # noqa E501
    assert repr(
        compare(
            base=" a tabby cat ",
            revision=" cat ",
            results="html_page")
    ), 'Base: "Separators at start and end of phrase"; Revision: "Separator then content then separator"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_separators_at_start_and_end_of_phrase_consecutive_separators():  # noqa E501
    assert repr(
        compare(
            base=" a tabby cat ",
            revision=" 	",
            results="html_page")
    ), 'Base: "Separators at start and end of phrase"; Revision: "Consecutive separators"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_separators_at_start_and_end_of_phrase_phrase():  # noqa E501
    assert repr(
        compare(
            base=" a tabby cat ",
            revision="a tabby cat",
            results="html_page")
    ), 'Base: "Separators at start and end of phrase"; Revision: "Phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_separators_at_start_and_end_of_phrase_separator_at_start_of_phrase():  # noqa E501
    assert repr(
        compare(
            base=" a tabby cat ",
            revision=" a tabby cat",
            results="html_page")
    ), 'Base: "Separators at start and end of phrase"; Revision: "Separator at start of phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_separators_at_start_and_end_of_phrase_separator_at_end_of_phrase():  # noqa E501
    assert repr(
        compare(
            base=" a tabby cat ",
            revision="a tabby cat ",
            results="html_page")
    ), 'Base: "Separators at start and end of phrase"; Revision: "Separator at end of phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_separators_at_start_and_end_of_phrase_separators_at_start_and_end_of_phrase():  # noqa E501
    assert repr(
        compare(
            base=" a tabby cat ",
            revision=" a tabby cat ",
            results="html_page")
    ), 'Base: "Separators at start and end of phrase"; Revision: "Separators at start and end of phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_separators_at_start_and_end_of_phrase_two_separators_at_start_of_phrase():  # noqa E501
    assert repr(
        compare(
            base=" a tabby cat ",
            revision="  a tabby cat",
            results="html_page")
    ), 'Base: "Separators at start and end of phrase"; Revision: "Two separators at start of phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_separators_at_start_and_end_of_phrase_two_separators_at_end_of_phrase():  # noqa E501
    assert repr(
        compare(
            base=" a tabby cat ",
            revision="a tabby cat  ",
            results="html_page")
    ), 'Base: "Separators at start and end of phrase"; Revision: "Two separators at end of phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_separators_at_start_and_end_of_phrase_two_separators_at_start_and_end_of_phrase():  # noqa E501
    assert repr(
        compare(
            base=" a tabby cat ",
            revision="  a tabby cat  ",
            results="html_page")
    ), 'Base: "Separators at start and end of phrase"; Revision: "Two separators at start and end of phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_separators_at_start_and_end_of_phrase_repeating_phrase():  # noqa E501
    assert repr(
        compare(
            base=" a tabby cat ",
            revision="a tabby cat and another tabby cat",
            results="html_page")
    ), 'Base: "Separators at start and end of phrase"; Revision: "Repeating phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_two_separators_at_start_of_phrase_empty():  # noqa E501
    assert repr(
        compare(
            base="  a tabby cat",
            revision="",
            results="html_page")
    ), 'Base: "Two separators at start of phrase"; Revision: "Empty"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_two_separators_at_start_of_phrase_content():  # noqa E501
    assert repr(
        compare(
            base="  a tabby cat",
            revision="cat",
            results="html_page")
    ), 'Base: "Two separators at start of phrase"; Revision: "Content"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_two_separators_at_start_of_phrase_alternate_content():  # noqa E501
    assert repr(
        compare(
            base="  a tabby cat",
            revision="tabby",
            results="html_page")
    ), 'Base: "Two separators at start of phrase"; Revision: "Alternate content"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_two_separators_at_start_of_phrase_separator():  # noqa E501
    assert repr(
        compare(
            base="  a tabby cat",
            revision=" ",
            results="html_page")
    ), 'Base: "Two separators at start of phrase"; Revision: "Separator"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_two_separators_at_start_of_phrase_alternate_separator():  # noqa E501
    assert repr(
        compare(
            base="  a tabby cat",
            revision="	",
            results="html_page")
    ), 'Base: "Two separators at start of phrase"; Revision: "Alternate separator"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_two_separators_at_start_of_phrase_separator_then_content():  # noqa E501
    assert repr(
        compare(
            base="  a tabby cat",
            revision=" cat",
            results="html_page")
    ), 'Base: "Two separators at start of phrase"; Revision: "Separator then content"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_two_separators_at_start_of_phrase_content_then_separator():  # noqa E501
    assert repr(
        compare(
            base="  a tabby cat",
            revision="cat ",
            results="html_page")
    ), 'Base: "Two separators at start of phrase"; Revision: "Content then separator"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_two_separators_at_start_of_phrase_separator_then_content_then_separator():  # noqa E501
    assert repr(
        compare(
            base="  a tabby cat",
            revision=" cat ",
            results="html_page")
    ), 'Base: "Two separators at start of phrase"; Revision: "Separator then content then separator"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_two_separators_at_start_of_phrase_consecutive_separators():  # noqa E501
    assert repr(
        compare(
            base="  a tabby cat",
            revision=" 	",
            results="html_page")
    ), 'Base: "Two separators at start of phrase"; Revision: "Consecutive separators"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_two_separators_at_start_of_phrase_phrase():  # noqa E501
    assert repr(
        compare(
            base="  a tabby cat",
            revision="a tabby cat",
            results="html_page")
    ), 'Base: "Two separators at start of phrase"; Revision: "Phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_two_separators_at_start_of_phrase_separator_at_start_of_phrase():  # noqa E501
    assert repr(
        compare(
            base="  a tabby cat",
            revision=" a tabby cat",
            results="html_page")
    ), 'Base: "Two separators at start of phrase"; Revision: "Separator at start of phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_two_separators_at_start_of_phrase_separator_at_end_of_phrase():  # noqa E501
    assert repr(
        compare(
            base="  a tabby cat",
            revision="a tabby cat ",
            results="html_page")
    ), 'Base: "Two separators at start of phrase"; Revision: "Separator at end of phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_two_separators_at_start_of_phrase_separators_at_start_and_end_of_phrase():  # noqa E501
    assert repr(
        compare(
            base="  a tabby cat",
            revision=" a tabby cat ",
            results="html_page")
    ), 'Base: "Two separators at start of phrase"; Revision: "Separators at start and end of phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_two_separators_at_start_of_phrase_two_separators_at_start_of_phrase():  # noqa E501
    assert repr(
        compare(
            base="  a tabby cat",
            revision="  a tabby cat",
            results="html_page")
    ), 'Base: "Two separators at start of phrase"; Revision: "Two separators at start of phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_two_separators_at_start_of_phrase_two_separators_at_end_of_phrase():  # noqa E501
    assert repr(
        compare(
            base="  a tabby cat",
            revision="a tabby cat  ",
            results="html_page")
    ), 'Base: "Two separators at start of phrase"; Revision: "Two separators at end of phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_two_separators_at_start_of_phrase_two_separators_at_start_and_end_of_phrase():  # noqa E501
    assert repr(
        compare(
            base="  a tabby cat",
            revision="  a tabby cat  ",
            results="html_page")
    ), 'Base: "Two separators at start of phrase"; Revision: "Two separators at start and end of phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_two_separators_at_start_of_phrase_repeating_phrase():  # noqa E501
    assert repr(
        compare(
            base="  a tabby cat",
            revision="a tabby cat and another tabby cat",
            results="html_page")
    ), 'Base: "Two separators at start of phrase"; Revision: "Repeating phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_two_separators_at_end_of_phrase_empty():  # noqa E501
    assert repr(
        compare(
            base="a tabby cat  ",
            revision="",
            results="html_page")
    ), 'Base: "Two separators at end of phrase"; Revision: "Empty"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_two_separators_at_end_of_phrase_content():  # noqa E501
    assert repr(
        compare(
            base="a tabby cat  ",
            revision="cat",
            results="html_page")
    ), 'Base: "Two separators at end of phrase"; Revision: "Content"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_two_separators_at_end_of_phrase_alternate_content():  # noqa E501
    assert repr(
        compare(
            base="a tabby cat  ",
            revision="tabby",
            results="html_page")
    ), 'Base: "Two separators at end of phrase"; Revision: "Alternate content"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_two_separators_at_end_of_phrase_separator():  # noqa E501
    assert repr(
        compare(
            base="a tabby cat  ",
            revision=" ",
            results="html_page")
    ), 'Base: "Two separators at end of phrase"; Revision: "Separator"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_two_separators_at_end_of_phrase_alternate_separator():  # noqa E501
    assert repr(
        compare(
            base="a tabby cat  ",
            revision="	",
            results="html_page")
    ), 'Base: "Two separators at end of phrase"; Revision: "Alternate separator"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_two_separators_at_end_of_phrase_separator_then_content():  # noqa E501
    assert repr(
        compare(
            base="a tabby cat  ",
            revision=" cat",
            results="html_page")
    ), 'Base: "Two separators at end of phrase"; Revision: "Separator then content"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_two_separators_at_end_of_phrase_content_then_separator():  # noqa E501
    assert repr(
        compare(
            base="a tabby cat  ",
            revision="cat ",
            results="html_page")
    ), 'Base: "Two separators at end of phrase"; Revision: "Content then separator"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_two_separators_at_end_of_phrase_separator_then_content_then_separator():  # noqa E501
    assert repr(
        compare(
            base="a tabby cat  ",
            revision=" cat ",
            results="html_page")
    ), 'Base: "Two separators at end of phrase"; Revision: "Separator then content then separator"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_two_separators_at_end_of_phrase_consecutive_separators():  # noqa E501
    assert repr(
        compare(
            base="a tabby cat  ",
            revision=" 	",
            results="html_page")
    ), 'Base: "Two separators at end of phrase"; Revision: "Consecutive separators"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_two_separators_at_end_of_phrase_phrase():  # noqa E501
    assert repr(
        compare(
            base="a tabby cat  ",
            revision="a tabby cat",
            results="html_page")
    ), 'Base: "Two separators at end of phrase"; Revision: "Phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_two_separators_at_end_of_phrase_separator_at_start_of_phrase():  # noqa E501
    assert repr(
        compare(
            base="a tabby cat  ",
            revision=" a tabby cat",
            results="html_page")
    ), 'Base: "Two separators at end of phrase"; Revision: "Separator at start of phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_two_separators_at_end_of_phrase_separator_at_end_of_phrase():  # noqa E501
    assert repr(
        compare(
            base="a tabby cat  ",
            revision="a tabby cat ",
            results="html_page")
    ), 'Base: "Two separators at end of phrase"; Revision: "Separator at end of phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_two_separators_at_end_of_phrase_separators_at_start_and_end_of_phrase():  # noqa E501
    assert repr(
        compare(
            base="a tabby cat  ",
            revision=" a tabby cat ",
            results="html_page")
    ), 'Base: "Two separators at end of phrase"; Revision: "Separators at start and end of phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_two_separators_at_end_of_phrase_two_separators_at_start_of_phrase():  # noqa E501
    assert repr(
        compare(
            base="a tabby cat  ",
            revision="  a tabby cat",
            results="html_page")
    ), 'Base: "Two separators at end of phrase"; Revision: "Two separators at start of phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_two_separators_at_end_of_phrase_two_separators_at_end_of_phrase():  # noqa E501
    assert repr(
        compare(
            base="a tabby cat  ",
            revision="a tabby cat  ",
            results="html_page")
    ), 'Base: "Two separators at end of phrase"; Revision: "Two separators at end of phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_two_separators_at_end_of_phrase_two_separators_at_start_and_end_of_phrase():  # noqa E501
    assert repr(
        compare(
            base="a tabby cat  ",
            revision="  a tabby cat  ",
            results="html_page")
    ), 'Base: "Two separators at end of phrase"; Revision: "Two separators at start and end of phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_two_separators_at_end_of_phrase_repeating_phrase():  # noqa E501
    assert repr(
        compare(
            base="a tabby cat  ",
            revision="a tabby cat and another tabby cat",
            results="html_page")
    ), 'Base: "Two separators at end of phrase"; Revision: "Repeating phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_two_separators_at_start_and_end_of_phrase_empty():  # noqa E501
    assert repr(
        compare(
            base="  a tabby cat  ",
            revision="",
            results="html_page")
    ), 'Base: "Two separators at start and end of phrase"; Revision: "Empty"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_two_separators_at_start_and_end_of_phrase_content():  # noqa E501
    assert repr(
        compare(
            base="  a tabby cat  ",
            revision="cat",
            results="html_page")
    ), 'Base: "Two separators at start and end of phrase"; Revision: "Content"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_two_separators_at_start_and_end_of_phrase_alternate_content():  # noqa E501
    assert repr(
        compare(
            base="  a tabby cat  ",
            revision="tabby",
            results="html_page")
    ), 'Base: "Two separators at start and end of phrase"; Revision: "Alternate content"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_two_separators_at_start_and_end_of_phrase_separator():  # noqa E501
    assert repr(
        compare(
            base="  a tabby cat  ",
            revision=" ",
            results="html_page")
    ), 'Base: "Two separators at start and end of phrase"; Revision: "Separator"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_two_separators_at_start_and_end_of_phrase_alternate_separator():  # noqa E501
    assert repr(
        compare(
            base="  a tabby cat  ",
            revision="	",
            results="html_page")
    ), 'Base: "Two separators at start and end of phrase"; Revision: "Alternate separator"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_two_separators_at_start_and_end_of_phrase_separator_then_content():  # noqa E501
    assert repr(
        compare(
            base="  a tabby cat  ",
            revision=" cat",
            results="html_page")
    ), 'Base: "Two separators at start and end of phrase"; Revision: "Separator then content"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_two_separators_at_start_and_end_of_phrase_content_then_separator():  # noqa E501
    assert repr(
        compare(
            base="  a tabby cat  ",
            revision="cat ",
            results="html_page")
    ), 'Base: "Two separators at start and end of phrase"; Revision: "Content then separator"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_two_separators_at_start_and_end_of_phrase_separator_then_content_then_separator():  # noqa E501
    assert repr(
        compare(
            base="  a tabby cat  ",
            revision=" cat ",
            results="html_page")
    ), 'Base: "Two separators at start and end of phrase"; Revision: "Separator then content then separator"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_two_separators_at_start_and_end_of_phrase_consecutive_separators():  # noqa E501
    assert repr(
        compare(
            base="  a tabby cat  ",
            revision=" 	",
            results="html_page")
    ), 'Base: "Two separators at start and end of phrase"; Revision: "Consecutive separators"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_two_separators_at_start_and_end_of_phrase_phrase():  # noqa E501
    assert repr(
        compare(
            base="  a tabby cat  ",
            revision="a tabby cat",
            results="html_page")
    ), 'Base: "Two separators at start and end of phrase"; Revision: "Phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_two_separators_at_start_and_end_of_phrase_separator_at_start_of_phrase():  # noqa E501
    assert repr(
        compare(
            base="  a tabby cat  ",
            revision=" a tabby cat",
            results="html_page")
    ), 'Base: "Two separators at start and end of phrase"; Revision: "Separator at start of phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_two_separators_at_start_and_end_of_phrase_separator_at_end_of_phrase():  # noqa E501
    assert repr(
        compare(
            base="  a tabby cat  ",
            revision="a tabby cat ",
            results="html_page")
    ), 'Base: "Two separators at start and end of phrase"; Revision: "Separator at end of phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_two_separators_at_start_and_end_of_phrase_separators_at_start_and_end_of_phrase():  # noqa E501
    assert repr(
        compare(
            base="  a tabby cat  ",
            revision=" a tabby cat ",
            results="html_page")
    ), 'Base: "Two separators at start and end of phrase"; Revision: "Separators at start and end of phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_two_separators_at_start_and_end_of_phrase_two_separators_at_start_of_phrase():  # noqa E501
    assert repr(
        compare(
            base="  a tabby cat  ",
            revision="  a tabby cat",
            results="html_page")
    ), 'Base: "Two separators at start and end of phrase"; Revision: "Two separators at start of phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_two_separators_at_start_and_end_of_phrase_two_separators_at_end_of_phrase():  # noqa E501
    assert repr(
        compare(
            base="  a tabby cat  ",
            revision="a tabby cat  ",
            results="html_page")
    ), 'Base: "Two separators at start and end of phrase"; Revision: "Two separators at end of phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_two_separators_at_start_and_end_of_phrase_two_separators_at_start_and_end_of_phrase():  # noqa E501
    assert repr(
        compare(
            base="  a tabby cat  ",
            revision="  a tabby cat  ",
            results="html_page")
    ), 'Base: "Two separators at start and end of phrase"; Revision: "Two separators at start and end of phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_two_separators_at_start_and_end_of_phrase_repeating_phrase():  # noqa E501
    assert repr(
        compare(
            base="  a tabby cat  ",
            revision="a tabby cat and another tabby cat",
            results="html_page")
    ), 'Base: "Two separators at start and end of phrase"; Revision: "Repeating phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_repeating_phrase_empty():  # noqa E501
    assert repr(
        compare(
            base="a tabby cat and another tabby cat",
            revision="",
            results="html_page")
    ), 'Base: "Repeating phrase"; Revision: "Empty"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_repeating_phrase_content():  # noqa E501
    assert repr(
        compare(
            base="a tabby cat and another tabby cat",
            revision="cat",
            results="html_page")
    ), 'Base: "Repeating phrase"; Revision: "Content"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_repeating_phrase_alternate_content():  # noqa E501
    assert repr(
        compare(
            base="a tabby cat and another tabby cat",
            revision="tabby",
            results="html_page")
    ), 'Base: "Repeating phrase"; Revision: "Alternate content"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_repeating_phrase_separator():  # noqa E501
    assert repr(
        compare(
            base="a tabby cat and another tabby cat",
            revision=" ",
            results="html_page")
    ), 'Base: "Repeating phrase"; Revision: "Separator"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_repeating_phrase_alternate_separator():  # noqa E501
    assert repr(
        compare(
            base="a tabby cat and another tabby cat",
            revision="	",
            results="html_page")
    ), 'Base: "Repeating phrase"; Revision: "Alternate separator"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_repeating_phrase_separator_then_content():  # noqa E501
    assert repr(
        compare(
            base="a tabby cat and another tabby cat",
            revision=" cat",
            results="html_page")
    ), 'Base: "Repeating phrase"; Revision: "Separator then content"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_repeating_phrase_content_then_separator():  # noqa E501
    assert repr(
        compare(
            base="a tabby cat and another tabby cat",
            revision="cat ",
            results="html_page")
    ), 'Base: "Repeating phrase"; Revision: "Content then separator"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_repeating_phrase_separator_then_content_then_separator():  # noqa E501
    assert repr(
        compare(
            base="a tabby cat and another tabby cat",
            revision=" cat ",
            results="html_page")
    ), 'Base: "Repeating phrase"; Revision: "Separator then content then separator"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_repeating_phrase_consecutive_separators():  # noqa E501
    assert repr(
        compare(
            base="a tabby cat and another tabby cat",
            revision=" 	",
            results="html_page")
    ), 'Base: "Repeating phrase"; Revision: "Consecutive separators"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_repeating_phrase_phrase():  # noqa E501
    assert repr(
        compare(
            base="a tabby cat and another tabby cat",
            revision="a tabby cat",
            results="html_page")
    ), 'Base: "Repeating phrase"; Revision: "Phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_repeating_phrase_separator_at_start_of_phrase():  # noqa E501
    assert repr(
        compare(
            base="a tabby cat and another tabby cat",
            revision=" a tabby cat",
            results="html_page")
    ), 'Base: "Repeating phrase"; Revision: "Separator at start of phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_repeating_phrase_separator_at_end_of_phrase():  # noqa E501
    assert repr(
        compare(
            base="a tabby cat and another tabby cat",
            revision="a tabby cat ",
            results="html_page")
    ), 'Base: "Repeating phrase"; Revision: "Separator at end of phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_repeating_phrase_separators_at_start_and_end_of_phrase():  # noqa E501
    assert repr(
        compare(
            base="a tabby cat and another tabby cat",
            revision=" a tabby cat ",
            results="html_page")
    ), 'Base: "Repeating phrase"; Revision: "Separators at start and end of phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_repeating_phrase_two_separators_at_start_of_phrase():  # noqa E501
    assert repr(
        compare(
            base="a tabby cat and another tabby cat",
            revision="  a tabby cat",
            results="html_page")
    ), 'Base: "Repeating phrase"; Revision: "Two separators at start of phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_repeating_phrase_two_separators_at_end_of_phrase():  # noqa E501
    assert repr(
        compare(
            base="a tabby cat and another tabby cat",
            revision="a tabby cat  ",
            results="html_page")
    ), 'Base: "Repeating phrase"; Revision: "Two separators at end of phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_repeating_phrase_two_separators_at_start_and_end_of_phrase():  # noqa E501
    assert repr(
        compare(
            base="a tabby cat and another tabby cat",
            revision="  a tabby cat  ",
            results="html_page")
    ), 'Base: "Repeating phrase"; Revision: "Two separators at start and end of phrase"'  # noqa E501


@pytest.mark.skipif("config.getoption('quick')")
def test_compare_repeating_phrase_repeating_phrase():  # noqa E501
    assert repr(
        compare(
            base="a tabby cat and another tabby cat",
            revision="a tabby cat and another tabby cat",
            results="html_page")
    ), 'Base: "Repeating phrase"; Revision: "Repeating phrase"'  # noqa E501
