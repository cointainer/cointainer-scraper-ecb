# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [v0.1.3] - (2022-12-19)

### Changed
- Changed the location of the logging setup (a26a96e427aa970e358c268e4d39309e2eb29323)

### Fixed
- Fixed dataparser displays a warning while using not the latest version (63c7e625c71693283b981f81af1168ad6248af03)

### Security
- Security: bump pytest from 7.1.3 to 7.2.0 (9abbf82c25d6bdac4ea2d9b447dad0c736188cbe)

## [v0.1.2] - (2022-12-17)

### Security
- Security: bump certifi from 2022.6.15 to 2022.12.7 (#1)

## [v0.1.1] - (2022-12-17)

### Added
- Added a log message for responses with status code 404 when requesting the html page for a two euro (89d093c90dad8f3c11cabc338f2d96ea1de23363) 
### Fixed
- Fixed relative urls of images were not parsed correctly (especially occured in 2012) (011439f3449ec1ae3527c1ef2bf3c924a774ce4f)

## [v0.1.0] - (2022-09-11)

- Initial release