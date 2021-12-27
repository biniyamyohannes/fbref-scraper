from player_info import get_age


def test_age_empty():
    expected = None
    assert get_age("") == expected


def test_age_none():
    expected = None
    assert get_age(None) == expected


def test_age_too_many_words():
    expected = None
    assert get_age('too many words in the string') == expected


def test_age_not_enough_words():
    expected = None
    assert get_age('not enough') == expected


def test_age_nondate_str():
    expected = None
    assert get_age('just enough words') == expected


def test_age_wrong_type():
    expected = None
    assert get_age(3) == expected