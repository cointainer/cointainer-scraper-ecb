from coin_collector_scraper_ecb.coins import _get_commemorative_coins


def test_coins_2004():
    with open("tests/data/comm_2004.en.html", "rb") as f:
        coins = _get_commemorative_coins(f.read(), "en", 2004)

        assert len(coins) == 6


def test_coins_2007():
    with open("tests/data/comm_2007.en.html", "rb") as f:
        coins = _get_commemorative_coins(f.read(), "en", 2007)

        assert len(coins) == 8
        assert len(coins[5].coinages) == 13


def test_coins_2015():
    with open("tests/data/comm_2015.en.html", "rb") as f:
        coins = _get_commemorative_coins(f.read(), "en", 2015)

        assert len(coins) == 29


def test_coins_2021():
    with open("tests/data/comm_2021.en.html", "rb") as f:
        coins = _get_commemorative_coins(f.read(), "en", 2021)

        assert len(coins) == 30
