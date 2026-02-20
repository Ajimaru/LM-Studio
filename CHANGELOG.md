# Changelog

All notable changes to this project are documented in this file.

## [v0.1.0] - 2026-02-20

### Added

- `setup.sh`: Added `--dry-run` (`-n`) to preview setup actions without applying system changes.
- `setup.sh`: Added `--help` (`-h`) option.
- `lmstudio_tray.py`: Added an **About** menu entry in the tray menu.
- `lmstudio_tray.py`: About dialog now shows branding metadata and model context.
- Added central `VERSION` file and wired tray version display to read from it.
- Documentation updates for setup flow and dry-run usage across docs.
- Renamed setup documentation from `docs/VENV_SETUP.md` to `docs/SETUP.md`.
- Initial centralized version metadata (`VERSION`).
- Tray About dialog with application and repository information
- Added comprehensive unit tests for `lmstudio_tray.py` in `tests/test_lmstudio_tray.py`.
- Added pytest coverage gate in `pytest.ini` with `--cov-fail-under=90`.
- Added documentation section in `docs/python_docstrings.html` for docstrings from `tests/test_lmstudio_tray.py`.
- Added a direct docs landing-page link to the test docstrings section (`docs/index.html` → `python_docstrings.html#test-docstrings`).
- Added `VERSION` file for centralized version metadata.

### Changed

- Documentation wording aligned from venv-centric labels to setup/environment-centric terminology.
- Internal docs links and workflow checks updated to `docs/SETUP.md`.
- Expanded branch coverage-focused tests to reach and keep at least 90% coverage for `lmstudio_tray.py`.
- Updated test fixture declaration to avoid Pylint `W0621` (`redefined-outer-name`) while preserving fixture usage (`@pytest.fixture(name="tray_module")`).
- Refactored protected member calls in tests via helper indirection to satisfy Pylint `W0212` (`protected-access`).
- Updated model selection behavior so `--list-models` in TTY mode loads the selected model into daemon mode.

### Fixed

- Consistency fixes for setup documentation links and references.
- Fixed Flake8 `E501` line-length issues in `tests/test_lmstudio_tray.py`.
- Fixed missing function docstrings (`Pylint C0116`) in `lmstudio_tray.py` and `tests/test_lmstudio_tray.py`.
- Fixed Pylint `W0621` warnings in test suite.
- Fixed Pylint `W0212` warnings in test suite.
- Fixed missing version display in tray About dialog by reading from `VERSION` file.
- Fixed local model discovery for LM Studio Hub by scanning `~/.lmstudio/hub/models` and listing `manifest.json`-based model entries.

---

For release tags and history, see the repository tags and pull requests.
