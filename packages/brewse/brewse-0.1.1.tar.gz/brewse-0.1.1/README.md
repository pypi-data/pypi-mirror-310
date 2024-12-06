# Brewse

An interactive TUI (Terminal User Interface) browser for Homebrew packages. Brewse provides a fast, user-friendly way to search, view, and install or uninstall Homebrew packages.

## Features

- Interactive search interface for both Formulae and Casks
- Detailed package information including:
  - Version
  - Description
  - Homepage
  - Installation status
  - Installation analytics (30/90/365 days)
- Quick installation/uninstallation of packages
- Keyboard-driven navigation
- Local caching of package data for faster subsequent searches

## Installation

Install via pip:

```
pip install brewse
```

## Usage

Launch Brewse in one of two ways:

1. Interactive search mode:
```
brewse
```

2. Direct search mode:
```
brewse <search-term>
```

## Requirements

- Python 3.6+
- Homebrew
- Internet connection

## Cache

Brewse caches package data in `~/.cache/brewse/` to improve performance. Cache entries expire after 24 hours.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
