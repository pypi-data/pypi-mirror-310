import pytest
from indian_name_maker import NameGenerator

@pytest.fixture
def generator():
    return NameGenerator()

def test_get_first_name(generator):
    name = generator.get_first_name()
    assert isinstance(name, str)
    assert len(name) > 0

def test_get_last_name(generator):
    name = generator.get_last_name()
    assert isinstance(name, str)
    assert len(name) > 0

def test_get_full_name(generator):
    name = generator.get_full_name()
    assert isinstance(name, str)
    assert " " in name
    first_name, last_name = name.split(" ")
    assert len(first_name) > 0
    assert len(last_name) > 0

def test_get_full_name_custom_separator(generator):
    name = generator.get_full_name(separator="-")
    assert "-" in name

def test_get_multiple_names(generator):
    names = generator.get_multiple_names(count=5)
    assert len(names) == 5
    assert all(isinstance(name, str) for name in names)
    assert all(" " in name for name in names)

def test_get_multiple_first_names(generator):
    names = generator.get_multiple_names(count=5, full_name=False)
    assert len(names) == 5
    assert all(isinstance(name, str) for name in names)
    assert all(" " not in name for name in names)

def test_invalid_count(generator):
    with pytest.raises(ValueError):
        generator.get_multiple_names(count=0)
