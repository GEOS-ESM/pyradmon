# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [Unreleased]

## [3.1.0] - 2026-08-06

### Added
* **Driver Script**: Added `instruments` variable extraction directly from `rcfile` in `pyradmon_img_driver.csh`.

### Changed 

#### index.php:
* **PHP 8+ Compatibility**: Added null coalescing/fallback to empty arrays (`?: []`) for `glob()` calls to prevent fatal errors if no directories are found.
* **Error Prevention**: Implemented `isset()` checks and null coalescing (`??`) for all `$_POST` variable accesses (exp, date, inst, chan, imgtype) to eliminate undefined index warnings. Added default initializations for `$nchan` and `$dosubset`.
* **HTML/CSS Modernization**: Replaced deprecated HTML tags and attributes (e.g., `<center>`, `cols`, `border`, `cellpadding`) with modern inline CSS (`text-align: center`, `border: 2px solid`, etc.).
* **UI/Layout Updates**: Increased the main table width to `1342px` and added responsive CSS (`max-width: 100%; height: auto;`) to the primary display image.
* **Markup Corrections**: Fixed broken HTML structure by adding the missing closing `</form>` and `</tr>` tags at the end of the document.

#### Timeseries / Pyradmon Offline:
* **Image Dimensions**: Increased target width from 595 to 1000 in all plot configuration YAML files.
* **File Deduplication**: Replaced redundant `ssmis_f16` and `ssmis_f18` configuration files with symlinks to the `ssmis_f17` templates.
* **Plot Styling (`plot.py`)**: Moved legends to the right side of plots, increased text/title sizes, set line widths to 2.0, adjusted X-axis date format to `%Y-%m-%d %Hz`, and shifted assimilation status labels leftward for better alignment.
* **Config Templates**: Updated inline instructions to use spaces instead of commas for multiple instruments, updated the polar host example to `gs6101-polar`, and removed hardcoded fallback parameters (`base_directory`, `experiment_id`, etc.).

### Fixed

### Removed

### Deprecated


## [3.0.0] - 2026-07-01

### Added
* **Environment Setup**: Unified one-step loader scripts (`load_radmon_config.sh` / `.csh`) with repo-root verification and helper instructions for aliases.
* **Auto-Configuration**: Environment loader now auto-generates user-specific timeseries YAMLs (`user_geosit...`, `user_m21c...`), dynamically injecting `$USER` and path variables.

### Changed
* **Path Resolution**: Replaced hardcoded `/discover/...` paths in configuration templates with dynamic `{PYRADMON_TIMESERIES}` variables to ensure portability.
* **Documentation**: Overhauled README installation and usage instructions to reflect the streamlined setup workflow.

### Removed
* **Redundant Loaders**: Deleted `.tcsh` and `.zsh` configuration loader scripts, consolidating functionality into `.csh` and `.sh` respectively.


## [2.1.0] - 2026-06-25

### Changed
* **Self-Contained Architecture**: Pyradmon no longer acts as a pointer to `/home/dao_ops/pyradmon/`; it now runs directly from the local repository.
* **Publication-Quality Plots**: Increased image DPI (150 -> 300) and canvas size (1200x1500 -> 3200x3000) for high-resolution output.
* **Typography**: Applied bold formatting to key plot elements (instrument names, channel numbers, assimilation status, subplot titles, and legends).
* **Layout Adjustments**: Modified title spacing and assimilation status positioning to prevent text overlap at larger resolutions.
* **Configuration**: Updated all YAML configuration files to utilize the new resolution settings.

### Fixed
* **Plot Rendering**: Escaped underscores in instrument names to prevent Matplotlib from incorrectly rendering them as LaTeX subscripts (e.g., `ATMS_NPP` instead of `ATMS` subscript `NPP`).


## [2.0.0] - 2026-06-16

### Added
* **Python Frontend**: Introduced new Python wrapper scripts to handle both spatial and timeseries pyradmon operations.

### Changed
* **OS Transition Fixes**: Overhauled the codebase to resolve compatibility issues caused by the SLES12 to SLES15 operating system transition.
* **Dependency Updates**: Updated backend Python scripts to account for newer package versions (e.g., matplotlib).
* **Pointer Architecture**: Pyradmon acts strictly as a pointer, executing backend scripts located in `/home/dao_ops/pyradmon/` rather than local source directories.
* **Output Destinations**: Changed the default directory locations for output images and `.tar` files (though the internal structure of the `.tar` files remains identical). Terminal output is also updated to reflect the new Python wrappers.
