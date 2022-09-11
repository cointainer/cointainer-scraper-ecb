<img src="https://github.com/cointainer/scraper-ecb/raw/main/docs/images/Cointainer-Scraper.png" width="100%" alt="Cointainer-Scraper Banner">

> Cointainer component for scraping coins from the ECB Website.

<div align="center">
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg">
</a>
<a href="https://github.com/cointainer/cointainer-scraper-ecb/blob/main/LICENSE">
    <img alt="License" src="https://img.shields.io/github/license/b4rtware/
cointainer-scraper-ecb.svg?color=blue">
</a>
<a href="https://github.com/cointainer/scraper-ecb"><img src="https://img.shields.io/pypi/pyversions/cointainer-scraper-ecb.svg"></a><br>
<a href="">
  <img src="https://img.shields.io/pypi/v/cointainer-scraper-ecb?color=dar-green" />
</a>
</div>

## Introduction

Cointainer Scraper (ECB) is one of the components of the Cointainer. This component offers the functionality of scraping euro coin data from the ECB website.

Currently supported coins:
- €2 commemorative coins
  - Country
  - Feature
  - Description
  - Issuing Volume
  - Issuing Date
  - Image URLs

## Installation

```bash
pip install cointainer-scraper-ecb
```

## Example
```python
from cointainer_scraper_ecb import get_two_euro_commemorative_coins

get_two_euro_commemorative_coins(
    language="en",
    year=2004
)
```
> Tested with Python 3.9.13 and cointainer_scraper_ecb v0.1.0 ✔️

Two data classes are relevant which are beeing returned by the function:
```python
def get_two_euro_commemorative_coins(
    lang: str = "en",
    year: int = START_YEAR
) -> List[TwoEuro]: ...
```

```python
@dataclass
class Coinage:
    """Represents a coin of a country to be collected."""

    country: Optional[str]
    image_default_url: Optional[str]
    volume: Optional[int]
    image_default_url_info: Optional[str] = None
    country_info: Optional[str] = None
    circulation_date: Optional[datetime.date] = None
    image_attribution: Optional[str] = None
    circulation_date_info: Optional[str] = None
    volume_info: Optional[str] = None


@dataclass
class TwoEuro:
    """A two euro coin to collect."""

    feature: str = ""
    description: str = ""
    coinages: List[Coinage] = field(default_factory=list)
```

## Roadmap

- [ ] Implement national side scraping (2€, 1€, 50 cent, 20 cent, 10 cent, 5 cent, 2 cent and 1 cent)
- [ ] CLI implementation with click

## Development

### Creating a new release

#### A. Create annotated release tag

1. New tag
```
git tag -a v<major>.<minor>.<patch>(a|b) -m release v<major>.<minor>.<patch>(a|b)
```
2. Push created tag

```
git push --tags
```
#### B. Create GitHub release

1. Run the following command `poetry version <version>`
<br>*cointainer-scraper-ecb* uses the following schema: `^\d+\.\d+\.\d+((b|a)\d+)?$`

2. Bump the version within the file: `cointainer_scraper_ecb/__init__.py`
<br>Make sure it's the same version used when bumping with poetry

3. Open `CHANGELOG.md` and write the new changelog:
    - Use the following `#` header: `v<version> - (yyyy-mm-dd)`
    <br>Used `##` headers:
    - 💌 Added
    - 🔨 Fixed
    - ♻️ Changed

4. Stage the modified files and push them with the following commit message:
> chore: bump to version `v<version>`

1. Create annotated release tag
   1.  New tag
    ```
    git tag -s -m "release v<version>" v<version>
    ```
   2. Push created tag

    ```
    git push --tags
    ```

2. Run the following command `poetry build` to create a tarball and a wheel based on the new version

3. Create a new github release and:
    1. Copy and paste the changelog content **without** the `#` header into the *description of the release* textbox
    2. Use the `#` header style to fill in the *Release title* (copy it from the `CHANGELOG.md`)
    3. Copy the version with the `v`-prefix into the *Tag version*

4. Attach the produced tarball and wheel (`dist/`) to the release

5. Check *This is a pre-release* if it's either an alpha or beta release *(a|b)* - ***optional*** 

6.  **Publish release**

### Testing

Use the following command to execute the tests:

```bash
poetry run pytest
```

To run the tests, the: `download-test-files.(ps1|sh)` script must be executed.

This is not the best method because the test data can change. However, I don't know if it is allowed to upload the data to the repository because of the copyright.

## License
This cointainer-scraper-ecb module is distributed under Apache-2.0. For ODbL-1.0 exception, see [LICENSING.md](https://github.com/cointainer/cointainer-scraper-ecb/blob/main/LICENSING.md)