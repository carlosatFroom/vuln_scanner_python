# Python Package Vulnerability Scanner

A comprehensive tool to scan Python packages for vulnerabilities by parsing requirements.txt files, resolving transitive dependencies, and checking for CVEs and security issues from multiple sources.

## Features

- **Requirements.txt Parser**: Supports various version specification formats (==, >=, >, <=, <)
- **Dependency Resolution**: Automatically resolves transitive dependencies
- **Multi-source Vulnerability Checking**:
  - Safety Database (via `safety` tool)
  - OSV Database (Google's Open Source Vulnerabilities database)
  - pip-audit (PyPI's vulnerability scanner)
- **Detailed Reporting**: Generates comprehensive reports with vulnerability details
- **Multiple Output Formats**: Console output and file export
- **CVE Integration**: Links vulnerabilities to CVE identifiers when available

## Installation

1. Clone or download the vulnerability scanner
2. Run the setup script to install dependencies:

```bash
python3 setup.py
```

Or install dependencies manually:

```bash
pip install requests safety pip-audit
```

## Usage

### Basic Usage

```bash
python3 vulnerability_scanner.py
```

This will scan the default `requirements.txt` file in the current directory.

### Advanced Usage

```bash
# Scan a specific requirements file
python3 vulnerability_scanner.py --requirements /path/to/requirements.txt

# Save report to file
python3 vulnerability_scanner.py --requirements requirements.txt --output vulnerability_report.txt

# Quiet mode (no console output)
python3 vulnerability_scanner.py --requirements requirements.txt --output report.txt --quiet
```

### Command Line Options

- `--requirements, -r`: Path to requirements.txt file (default: requirements.txt)
- `--output, -o`: Output file for report (optional)
- `--quiet, -q`: Suppress output to stdout

## Sample Report

```
================================================================================
PYTHON PACKAGE VULNERABILITY SCAN REPORT
================================================================================
Generated: 2025-07-15 09:43:34
Requirements file: requirements.txt
Total packages scanned: 20
Direct packages: 7
Transitive dependencies: 13
Total vulnerabilities found: 143

VULNERABILITY SUMMARY BY SEVERITY:
  CVSS_V3: 83
  CVSS_V4: 3
  UNKNOWN: 57

DETAILED VULNERABILITY LIST:
----------------------------------------
Package: Django (3.2.5)
Vulnerability ID: GHSA-2gwj-7jmv-h26r
CVE ID: CVE-2022-28346
Severity: CVSS_V3
Source: osv
Description: SQL Injection in Django

[... more vulnerabilities ...]

SCANNED PACKAGES:
--------------------
Direct packages:
  django (3.2.5)
  flask (1.1.4)
  jinja2 (2.11.3)
  [... more packages ...]

Transitive dependencies:
  Django (3.2.5)
  Flask (1.1.4)
  [... more dependencies ...]
```

## Exit Codes

- `0`: Success (no vulnerabilities found)
- `1`: Vulnerabilities found

## Vulnerability Sources

### Safety Database
- Community-maintained database of known security vulnerabilities
- Requires `safety` package to be installed
- Provides detailed vulnerability information with fix versions

### OSV Database
- Google's Open Source Vulnerabilities database
- Real-time API access to comprehensive vulnerability data
- Includes CVE mappings and detailed descriptions

### pip-audit
- PyPI's official vulnerability scanner
- Integrates with PyPI Advisory Database
- Provides structured vulnerability reports

## Supported Requirements Formats

The scanner supports various pip requirements formats:

```
# Exact version
django==3.2.5

# Version ranges
requests>=2.25.0
flask>1.0.0
pillow<=8.3.0
numpy<1.21.0

# No version specified (latest)
pytest
```

## Dependencies

- Python 3.6+
- requests (for OSV API calls)
- safety (for Safety DB scanning)
- pip-audit (for PyPI Advisory Database)

## Architecture

The scanner follows a modular architecture:

1. **Requirements Parser**: Parses requirements.txt files
2. **Dependency Resolver**: Creates virtual environments to resolve transitive dependencies
3. **Vulnerability Checkers**: Multiple sources for comprehensive coverage
4. **Report Generator**: Structured output with detailed vulnerability information

## Limitations

- Some packages may fail to install during dependency resolution (warnings will be shown)
- Network connectivity required for OSV database queries
- Virtual environment creation requires sufficient disk space

## Contributing

The scanner is designed to be easily extensible. To add new vulnerability sources:

1. Create a new method following the pattern `check_[source]_database()`
2. Return a list of `Vulnerability` objects
3. Add the method call to the `scan()` method

## Security Considerations

This tool is designed for **defensive security purposes only**:
- Vulnerability detection and reporting
- Security assessment of dependencies
- Compliance and audit support

Do not use this tool for malicious purposes.