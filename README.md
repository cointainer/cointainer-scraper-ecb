<img src="https://github.com/B4rtware/coin-collector-scraper-ecb/raw/main/docs/images/Cointainer-Scraper.png" width="100%" alt="Cointainer-Scraper Banner">

> Cointainer component for scraping coins from the ECB Website.

<div align="center">
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg">
</a>
<a href="https://github.com/B4rtware/coin-collector-scraper-ecb/blob/main/LICENSE">
    <img alt="License" src="https://img.shields.io/github/license/b4rtware/
coin-collector-scraper-ecb.svg?color=blue">
</a>
<a href="https://github.com/B4rtware/coin-collector-scraper-ecb"><img src="https://img.shields.io/pypi/pyversions/coin-collector-scraper-ecb.svg"></a><br>
<a href="">
  <img src="https://img.shields.io/pypi/v/coin-collector-scraper-ecb?color=dar-green" />
</a>
</div>

## 👋 Introduction

Cointainer Scraper (ECB) is one of the components of the Cointainer. This component offers the functionality of scraping euro coin data from the ECB website.

At the current time, these are the following dates:
- €2 commemorative coins
  - Country
  - Feature
  - Description
  - Issuing Volume
  - Issuing Date
  - Image URLs

## 💡 Installation

`pip install cointainer-scraper-ecb`

### via git

1. make sure to use at least **python 3.8**
2. clone the repo `git clone https://github.com/B4rtware/coin-collector-scraper-ecb.git`
3. `cd coin-collector-scraper-ecb` and install dependencies via
    - `poetry install` ([Poetry](https://github.com/python-poetry/poetry))
    or
    - use the provided `requirements.txt`

## ⚙️ Example
```python
from cointainer_scraper_ecb import get_two_euro_commemorative_coins

get_two_euro_commemorative_coins(
    language="en",
    year=2004
)
```

> Tested with Python 3.10.4 and cointainer_scraper_ecb v0.1.0 ✔️

## 👩🏽‍💻 Development

### Creating a new release

1. Run the following command `poetry version <version>`
<br>*Morpho* uses the following schema: `^\d+\.\d+\.\d+((b|a)\d+)?$`

2. Bump the version within the file: `morpho/__version__.py`
<br>Make sure it's the same version used when bumping with poetry

3. Open `Changelog.md` and write the new changelog:
    - Use the following `#` header: `v<version> - (dd.mm.yyyy)`
    <br>Used `##` headers:
    - 💌 Added
    - 🔨 Fixed
    - ♻️ Changed

4. Stage the modified files and push them with the following commit message:
    > chore: bump to version `<version>`

5. Run the following command `poetry build` to create a tarball and a wheel based on the new version

6. Create a new github release and:
    1. Copy and paste the changelog content **without** the `#` header into the *description of the release* textbox
    2. Use the `#` header style to fill in the *Release title* (copy it from the `Changelog.md`)
    3. Copy the version with the `v`-prefix into the *Tag version*

7. Attach the produced tarball and wheel (`dist/`) to the release

8. Check *This is a pre-release* if it's either an alpha or beta release *(a|b)* - ***optional*** 

9. **Publish release**

### Testing

To run the tests, the `download-test-files.ps1` script must be executed.

This is not the best method because the test data can change. However, I don't know if it is allowed to upload the data to the repository because of the copyright.

## 📝 License
MIT