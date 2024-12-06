import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--quick",
        action="store_true",
        dest="quick",
        default=False,
        help="Don't run the permutation tests",
    )


@pytest.fixture
def a():
    return {
        "value": "a",
        "content": True,
    }


@pytest.fixture
def the():
    return {
        "value": "the",
        "content": True,
    }


@pytest.fixture
def tabby():
    return {
        "value": "tabby",
        "content": True,
    }


@pytest.fixture
def cat():
    return {
        "value": "cat",
        "content": True,
    }


@pytest.fixture
def big():
    return {
        "value": "big",
        "content": True,
    }


@pytest.fixture
def space():
    return {
        "value": " ",
        "content": False,
    }


@pytest.fixture
def tab():
    return {
        "value": "\t",
        "content": False,
    }
