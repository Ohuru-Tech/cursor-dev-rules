# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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

[0.1.0]: https://github.com/Ohuru-Tech/cursor-dev-rules/releases/tag/v0.1.0
