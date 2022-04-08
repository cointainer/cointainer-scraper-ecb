from coin_collector_parser_ecb.coins import _get_commemorative_coins

import pprint


def test_coins_2004():
    with open("tests/data/comm_2004.en.html", "rb") as f:
        coins = _get_commemorative_coins(f.read(), "en", 2004)

        assert len(coins) == 6

def test_coins_2007():
    with open("tests/data/comm_2007.en.html", "rb") as f:
        coins = _get_commemorative_coins(f.read(), "en", 2004)

        assert len(coins) == 8
        assert len(coins[5].coinages) == 13