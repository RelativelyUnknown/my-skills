import pytest
from textkit import wrap


def test_message_is_fixed():
    with pytest.raises(ValueError) as e:
        wrap("aa", 0)
    assert "positive" in str(e.value) and "postive" not in str(e.value)


def test_behaviour_unchanged():
    assert wrap("aa bb cc", 5) == ["aa bb", "cc"]
