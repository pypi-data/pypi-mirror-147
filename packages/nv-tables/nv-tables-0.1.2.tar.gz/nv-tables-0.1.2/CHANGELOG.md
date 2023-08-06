# Change Log

## Unreleased


## 0.1.2
### Added
### Changed
- Removed dependency from nv.utils for normalization (now done via normalization.py)
### Fixed
- Removed a `__init__.py` package that was breaking the namespace package 
  when installed with nv.utils
- Fixed a bug that was preventing `from nv.utils import csv` from working
  in a way similar to other serialization packages such as json, pickle or PyYaml.

## 0.1.1
### Fixed
- Added guards that prevent empty data to be passed to the underlying parsers (which breaks with cryptic messages)
- Fixed a package namespace bug that was preventing nv-utils and nv-tables to be installed properly in projects that use both
- Changed the way that the default serializers were implemented, aiming however to keep the way the names to avoid breaking changes
