# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.1] - 2025-01-12

### Fixed

- Fixed "Could not find rules directory" error when package is installed (non-editable mode)
- Moved rules directory from project root to package directory (`cursor_dev_rules/rules/`) for proper package data inclusion
- Improved `get_rules_path()` function with better fallback logic for both installed and development modes
- Updated package configuration to properly include rules as package data instead of shared-data

### Changed

- Rules directory structure: moved from `rules/` to `cursor_dev_rules/rules/` for better package distribution
- Updated documentation to reflect new rules directory location

## [0.1.0] - 2025-01-12

### Added

- Initial release of cursor-dev-rules CLI tool
- Support for fetching and installing Cursor IDE dev rules
- Framework support for:
  - Django (backend)
  - FastAPI (backend)
  - Next.js (frontend)
- General backend and frontend rules
- Automatic directory structure creation in `.cursor/rules/`
- CLI command `cursor-dev-rules fetch <category>/<framework>`
- Comprehensive test suite with pytest
- GitHub Actions workflows for:
  - Automated testing on push and pull requests
  - Automated PyPI publishing on tag pushes
- MIT License
- Comprehensive documentation in README
- PyPI package configuration and publishing setup

### Changed

- N/A (initial release)

### Fixed

- N/A (initial release)

### Security

- N/A (initial release)

[0.1.1]: https://github.com/Ohuru-Tech/cursor-dev-rules/releases/tag/v0.1.1
[0.1.0]: https://github.com/Ohuru-Tech/cursor-dev-rules/releases/tag/v0.1.0
