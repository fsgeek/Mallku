"""Minimal CI test to establish baseline functionality."""


def test_basic_arithmetic():
    """Most basic test possible."""
    assert 2 + 2 == 4


def test_string_operations():
    """Test basic string operations."""
    assert "hello" + " " + "world" == "hello world"


def test_list_operations():
    """Test basic list operations."""
    items = [1, 2, 3]
    items.append(4)
    assert len(items) == 4
    assert items[-1] == 4


def test_dict_operations():
    """Test basic dict operations."""
    data = {"key": "value"}
    data["new_key"] = "new_value"
    assert len(data) == 2
    assert data.get("key") == "value"


def test_boolean_logic():
    """Test basic boolean operations."""
    assert True and True
    assert not (True and False)
    assert True or False
    assert not (False or False)
