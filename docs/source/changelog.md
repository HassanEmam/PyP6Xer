# Changelog

All notable changes to PyP6Xer will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0] - 2026-10-30

### Changed
- Version bumped to 2.0 — the 1.016.00 feature set (programmatic relationship
  editing, generic table store, RSRCCURV support, expanded field coverage,
  hardened DCMA 14-point analysis, and the comprehensive test suite) is now
  the stable 2.0 baseline

## [1.016.00] - 2026-10-28

### Added
- Programmatic relationship editing: `add_relationship`, `remove_relationship`,
  `replace_relationship` on the relations collection, plus `get_predecessors` /
  `get_successors` passthroughs on Tasks (issue #7)
- Generic table store: every XER table is available losslessly via
  `xer.tables["TABLE_NAME"]`, even those without a dedicated model class
- RSRCCURV (resource curve definitions) and RSRCCURVDATA support
- 37 previously unsupported XER schema fields now parsed and written back
- Comprehensive test suite: 280+ tests covering all 39 model-backed tables
  (parse, lookups, TSV alignment, write round-trips), every DCMA check, Tasks
  queries, resource hierarchy, calendar data parsing, and reader/writer edge
  cases — fixtures are built from scratch, no sample files needed

### Improved
- Roughly 2x faster parsing and ~30% less memory on large files
- DCMA 14-point analysis hardened: calendar-aware day/hour conversions,
  multi-project data dates, per-activity slippage counting, robust
  longest-critical-chain, and checks #12-#14 (critical path test, CPLI, BEI)
- Consistent `__len__` / iteration across all collections
- Reader tolerates blank lines, schema drift, and ROLES/ROLE table names

### Fixed
- Seven wrong-column bugs in field mappings (TASK, TASKRSRC, TASKPRED, PROJWBS,
  PROJECT, ROLES and others)
- Character encoding corruption on non-ASCII XER content
- Crashes on blank lines and schema drift in XER files
- `Calendar.obj_list` leaking between Reader instances
- Writer previously dropped tables not present in the model and faked the
  ERMHDR on round-trips; it now writes every table and preserves the header
- `find_by_id` lookups in 12 collections used the wrong key and always
  returned empty results
- `get_num_lines` crash on empty files; `get_work_pattern` missing day blocks
  after the VIEW marker in calendar data

## [1.015.00] - 2025-01-09

### Added
- Comprehensive documentation with Sphinx
- Getting started guide and examples
- API reference documentation
- Contributing guidelines
- Support for writing XER files back to disk
- Enhanced error handling and validation
- Object-oriented access to project data

### Improved
- Code organization and structure
- Class relationships and data access
- Documentation coverage
- Test coverage improvements

### Fixed
- Various parsing edge cases
- Memory optimization for large files
- Unicode handling improvements

## [1.014.00] - 2024-12-15

### Added
- Support for additional XER elements
- Enhanced calendar parsing
- Resource assignment tracking
- UDF (User Defined Fields) support

### Fixed
- Date parsing improvements
- Memory leaks in large file processing

## [1.013.00] - 2024-11-20

### Added
- DCMA 14-point analysis module
- Enhanced relationship parsing
- Activity code support
- Financial template parsing

### Changed
- Improved parsing performance
- Better error messages

## [1.012.00] - 2024-10-15

### Added
- Resource category support
- Role and role rate parsing
- Schedule options parsing
- Non-work time support

### Fixed
- Critical path calculation issues
- Float calculation improvements

## [1.011.00] - 2024-09-10

### Added
- Complete WBS hierarchy support
- Calendar exception handling
- Project category support
- Enhanced activity relationships

### Changed
- Refactored class structure for better inheritance
- Improved data validation

## [1.010.00] - 2024-08-05

### Added
- Multi-project support
- Resource assignments
- Cost account structure
- Currency support

### Fixed
- Various parsing edge cases
- Performance improvements for large files

## [1.009.00] - 2024-07-01

### Added
- Activity resource assignments
- Task procedure support
- Enhanced calendar data parsing
- OBS (Organizational Breakdown Structure) support

### Changed
- Improved object relationships
- Better memory management

## [1.008.00] - 2024-06-01

### Added
- Resource rates and categories
- Enhanced activity codes
- Project-level settings
- Financial templates

### Fixed
- Date handling improvements
- Encoding issues with international characters

## [1.007.00] - 2024-05-01

### Added
- Schedule options parsing
- Enhanced WBS support
- Resource calendars
- Activity types

### Changed
- Improved error handling
- Better validation of XER file format

## [1.006.00] - 2024-04-01

### Added
- User defined field types and values
- Enhanced project properties
- Calendar working patterns
- Resource hierarchies

### Fixed
- Performance improvements
- Memory usage optimization

## [1.005.00] - 2024-03-01

### Added
- Complete calendar support with exceptions
- Resource assignments to activities
- Activity code values
- Enhanced relationship types

### Changed
- Refactored data model for better performance
- Improved class inheritance structure

## [1.004.00] - 2024-02-01

### Added
- Account structure support
- Role definitions
- Currency types
- Enhanced activity properties

### Fixed
- Various parsing edge cases
- Improved error messages

## [1.003.00] - 2024-01-15

### Added
- WBS (Work Breakdown Structure) support
- Resource definitions
- Basic calendar parsing
- Activity relationships (predecessors)

### Changed
- Improved object-oriented design
- Better separation of concerns

## [1.002.00] - 2023-12-01

### Added
- Enhanced activity parsing
- Project-level properties
- Basic resource support
- OBS structure parsing

### Fixed
- File encoding issues
- Performance improvements

## [1.001.00] - 2023-11-01

### Added
- Basic activity code support
- Enhanced project metadata
- Improved error handling
- Better validation

### Changed
- Code structure improvements
- Documentation updates

## [1.000.00] - 2023-10-01

### Added
- Initial release
- Basic XER file parsing
- Project and activity extraction
- Simple data model
- Basic relationship parsing

### Features
- Read XER files exported from Primavera P6
- Extract project, activity, and basic relationship data
- Python object model for easy data access
- Basic error handling and validation

---

## Legend

- **Added** for new features
- **Changed** for changes in existing functionality
- **Deprecated** for soon-to-be removed features
- **Removed** for now removed features
- **Fixed** for any bug fixes
- **Security** for vulnerability fixes
