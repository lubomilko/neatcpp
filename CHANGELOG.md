# Changelog

[![Common Changelog](https://common-changelog.org/badge.svg)](https://common-changelog.org)

---

This file documents all notable changes in the [pycpp](https://github.com/lubomilko/pycpp) -
a C preprocessor in Python preserving the formatting of the original C source code.

---


## [1.1.3] - 2024-10-19

> **_Note:_** The version is set to 1.1.3 for consistency with other repo, where the fixes were
> applied separately through a longer period of time.

### Fixed

- Fix nested parentheses of the same type in methods `get_code_sample` and `expand_args` causing
  errors with certain Python versions.
- Do not require ellipsis (`...`) argument in a variadic macro to be filled with at least one
  argument in a macro reference. This fixes an invalid detection of insufficient amount of
  arguments in a macro reference where no arguments are provided for the ellipsis.
- Treat an empty argument in a function-like macro reference as a valid argument. This fixes an
  invalid detection of insufficient amount of arguments in a macro reference, where some arguments
  are empty.


## [1.1.0] - 2024-03-20

### Added

- `exclude_macros_files` attribute to the preprocessor class `PyCpp`.
- `-x, -- exclude` command line option.
- Docstrings for all public attributes and methods of the preprocessor class `PyCpp`.


## [1.0.0] - 2024-03-15

*First release*


[unreleased]: https://github.com/lubomilko/pycpp
[1.1.3]: https://github.com/lubomilko/pycpp/releases/tag/1.1.3
[1.1.0]: https://github.com/lubomilko/pycpp/releases/tag/1.1.0
[1.0.0]: https://github.com/lubomilko/pycpp/releases/tag/1.0.0
