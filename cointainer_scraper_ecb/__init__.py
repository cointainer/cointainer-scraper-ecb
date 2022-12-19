import logging
import sys

from .coins import get_two_euro_commemorative_coins as get_two_euro_commemorative_coins

__version__ = "0.1.2"

# setup logging

LOG = logging.getLogger("cointainer_scraper_ecb")
LOG.setLevel(logging.INFO)

FORMATTER = logging.Formatter(
    "[{asctime}] [{levelname:<7}] [{name}] {message}",
    datefmt="%d.%m.%Y %H:%M:%S",
    style="{",
)

stream = logging.StreamHandler(sys.stdout)
stream.setFormatter(FORMATTER)
LOG.addHandler(stream)

LOG.info("[OK] application started.")
