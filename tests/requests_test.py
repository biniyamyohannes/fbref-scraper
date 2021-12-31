from src.scraper.requests import get_soup, get_squads


def test_soup_empty():
    expected = None
    assert get_soup("") == expected


def test_soup_none():
    expected = None
    assert get_soup(None) == expected


def test_soup_nonexistent():
    expected = None
    assert get_soup("not a player") == expected


def test_squads_empty():
    expected = None
    assert get_squads("") == expected