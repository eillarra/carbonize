Changelog
=========

All notable changes to this project will be documented in this file.

## [Unreleased]

## [0.1.0] - 2025-03-25

### Added
- General API, introducing the `Footprint` class and steps.
- New calculator for car rides: `Ride`.
- New calculator for trains: `Train`.
- New calculator for webinars: `Webinar`.
- Initial documentation.

### Changed
- Underlying data is stored as Pickle files instead of CSV files.
- Save typed data to reduce processing when catalogs are loaded.
- `AviationCalculator` is now `Flight`.
- Minimal Python version is now 3.9.

## [0.0.1] - 2018-04-13

### Added
- First calculator: `AviationCalculator`.
- Initial data.

[unreleased]: https://github.com/eillarra/carbonize/compare/0.1.0...HEAD
[0.1.0]: https://github.com/eillarra/carbonize/releases/tag/0.1.0
[0.0.1]: https://github.com/eillarra/carbonize/releases/tag/0.0.1
