---
title: "Changelog"
publishedAt: "2024-11-03"
updatedAt: "2024-11-23"
summary: "Updates, bug fixes and improvements."
kind: "detailed"
---

## v0.2.27 - [UNRELEASED]

### Changed
- Enhanced configuration management
  - Moved `.env` and `pynions.json` to project root
  - Removed nested config directory structure
  - Added proper typing support for configuration
  - Improved singleton pattern implementation
  - Added comprehensive test coverage
  - Standardized on gpt-4o-mini as default model
- Improved configuration API
  - Added `set()` method for runtime configuration
  - Added `clear()` method for resetting configuration
  - Added `load()` method for custom file paths
  - Enhanced environment variable handling
- Updated documentation
  - Added new configuration examples
  - Updated API documentation
  - Added comprehensive test coverage information
  - Updated all examples to use gpt-4o-mini
- Simplified example workflow code

### Added
- New configuration methods:
  - `set()` for runtime configuration
  - `clear()` for resetting state
  - `load()` for custom file paths
- Complete test suite for configuration
- Type hints for better IDE support

### Fixed
- Environment variable handling in tests
- Configuration inheritance issues
- Missing type hints
- Inconsistent model defaults across codebase

### Security
- Improved API key management
- Enhanced environment variable handling

### Performance
- Standardized on gpt-4o-mini for better cost-performance ratio

## v0.2.26 - Nov 22, 2024

### Changed
- Simplified configuration management system
- Moved configuration files to project root
- Removed nested config folder structure
- Improved direct litellm integration
- Updated advanced example with async support
- Enhanced error handling and output formatting

### Added
- Root-level `.env` for API keys
- Root-level `pynions.json` for settings
- Clearer setup instructions in installation
- Example file copying during installation

### Removed
- Complex nested configuration system
- ~/.pynions directory requirement
- Outdated example configurations

### Security
- Improved API key management
- Enhanced environment variable handling

### Dependencies
- Updated minimum Python version to 3.8+

## v0.2.25 - Nov 20, 2024

### Security

- Fixed security vulnerabilities in aiohttp dependency
  - Addressed CVE-2024-52303 (Moderate severity)
  - Addressed CVE-2024-52304 (Moderate severity)

### Changed

- Improved dependency management
  - Updated to more flexible version ranges in requirements.txt
  - Reduced potential for dependency conflicts
  - Updated key dependencies:
    - aiohttp to 3.10.11
    - pydantic to 2.10.0
    - litellm to 1.52.11
    - openai to 1.55.0
    - setuptools to 75.6.0

## v0.2.24 - Nov 14, 2024

### Changed

- Updated data organization documentation
- Consolidated installation documentation
  - Merged SETUP.md and ENV_SETUP.md into installation.md
  - Improved organization and readability
  - Added comprehensive troubleshooting section
  - Enhanced security best practices
  - Updated file creation commands
  - Added detailed Python environment setup
  - Improved IDE setup instructions

### Documentation

- Streamlined documentation structure
- Removed redundant installation guides
- Updated cross-references in documentation
- Enhanced configuration documentation
- Added clear next steps section

## v0.2.22 - Nov 10, 2024

### Added

- New Workers system for standalone data extraction tasks
  - Added base Worker class in core module
  - Added PricingResearchWorker for automated pricing analysis
  - Integrated with existing plugins (Serper, Jina, LiteLLM)
- Automated pricing data extraction capabilities
  - Accurate plan detection
  - Feature extraction
  - Price point analysis
  - Subscriber limit detection

### Changed

- Enhanced LiteLLM integration for structured data extraction
- Improved content extraction accuracy in Jina plugin
- Standardized worker output format

### Documentation

- Added workers documentation and examples
- Updated plugin integration guides
- Added pricing research examples

## v0.2.21 - Nov 10, 2024

### Changed

- Centralized configuration management
  - Moved all environment loading to core Plugin class
  - Simplified plugin initialization
  - Removed redundant config loading from individual plugins
  - Standardized configuration access patterns
- Simplified workflow system
  - Streamlined WorkflowStep implementation
  - Improved error handling and propagation
  - Maintained backward compatibility with existing workflows

### Fixed

- Standardized environment variable handling across all plugins
- Fixed configuration file paths in documentation
- Improved workflow execution reliability
- Removed duplicate configuration loading

### Documentation

- Updated plugin development guide with new configuration patterns
- Added clear instructions for environment setup
- Improved workflow examples and best practices
- Added content analysis workflow documentation

## v0.2.19 - Nov 9, 2024

### Changed

- Reorganized project configuration structure
  - Moved all config files to `/pynions/config/` directory
  - Consolidated settings into single `settings.json`
  - Moved `.env` to config directory
- Improved data directory organization
  - Separated raw and output data
  - Added structured workflow status types
  - Implemented project-based output organization
- Enhanced utils.py with new file management functions
  - Added project-aware save functions
  - Improved status type validation
  - Added configurable file extensions
- Reorganized core module structure
  - Split core.py into separate modules
  - Created dedicated core/ directory
  - Improved code organization
- Maintained backward compatibility

### Added

- New configuration management system
  - Added `settings.py` for centralized config loading
  - Added workflow status types configuration
  - Added file extension preferences per status
- New utility functions for content workflow
  - `save_result()` with project and status support
  - `save_raw_data()` for structured data storage
  - `slugify()` for consistent file naming

## v0.2.17 - Nov 9, 2024

### Changed

- Reorganized examples structure for better discoverability
- Moved example scripts from /examples to /docs/examples
- Added detailed documentation for each example
- Improved example organization by marketing function

### Added

- New Research Workflow combining Serper and Jina plugins
- New documentation for BOFU content generator
- Quick analysis example documentation
- Examples README with categorized listing

## v0.2.15 - Nov 8, 2024

### Added

- New Frase API integration for content analysis
- Batch URL processing support
- Detailed metrics aggregation
- Enhanced logging and debugging output

## v0.2.14 - Nov 7, 2024

### Added

- New LiteLLM plugin for unified LLM access
- Content analysis workflow combining Serper, Jina, and LiteLLM
- Markdown brief generator with research citations
- Enhanced logging for content extraction

### Changed

- Updated workflow to use gpt-4o-mini model
- Improved error handling in Jina content extraction
- Enhanced content brief output format

### Fixed

- Token usage tracking in LiteLLM plugin
- Content extraction validation
- URL processing in workflow

## v0.2.13 - Nov 5, 2024

- Updated homepage
- Updated quickstart example
- Updated requirements.txt
- Updated setup.py

## v0.1.0 - Oct 30, 2024

- Initial release
