# mdformat-mdsf

[![Build Status][ci-badge]][ci-link] [![PyPI version][pypi-badge]][pypi-link]

An [mdformat](https://github.com/executablebooks/mdformat) plugin for formatting code blocks using [mdsf](https://github.com/hougesen/mdsf).

## Description

This plugin integrates [mdsf](https://github.com/hougesen/mdsf) with mdformat to automatically format code blocks in Markdown files. mdsf supports 332+ different code formatters across many programming languages.

## Prerequisites

You must have `mdsf` installed and available in your PATH. Install it from [https://github.com/hougesen/mdsf](https://github.com/hougesen/mdsf).

## Supported Languages

This plugin provides code formatters for the following languages:

- Python, JavaScript, TypeScript
- Rust, Go, Java, C, C++, C#
- Ruby, PHP, Swift, Kotlin, Scala
- Shell, Bash, Zsh
- JSON, YAML, TOML
- HTML, CSS, SCSS
- SQL, GraphQL
- Markdown

## `mdformat` Usage

Add this package wherever you use `mdformat` and the plugin will automatically format code blocks in supported languages. See [additional information on `mdformat` plugins here](https://mdformat.readthedocs.io/en/stable/users/plugins.html)

### Basic Usage

**Command Line:**

```sh
# Format all code blocks in supported languages
mdformat your-file.md

# Use specific mdsf config file
mdformat --mdsf-config path/to/mdsf.json your-file.md

# Only format specific languages
mdformat --mdsf-languages python,rust,go your-file.md

# Set custom timeout (default: 30 seconds)
mdformat --mdsf-timeout 60 your-file.md

# Fail on formatting errors instead of falling back to unformatted code
mdformat --mdsf-fail-on-error your-file.md
```

**Python API:**

```python
import mdformat

# Enable specific languages
formatted = mdformat.text(text, codeformatters={"python", "javascript"})

# With configuration options
formatted = mdformat.text(
    text,
    codeformatters={"python", "javascript", "rust"},
    options={
        "mdsf_config": "path/to/mdsf.json",
        "mdsf_timeout": 60,
        "mdsf_languages": ["python", "rust"],
        "mdsf_fail_on_error": False,
    }
)
```

### pre-commit / prek

```yaml
repos:
  - repo: https://github.com/executablebooks/mdformat
    rev: 0.7.19
    hooks:
      - id: mdformat
        additional_dependencies:
          - mdformat-mdformat-mdsf
```

### uvx

```sh
uvx --from mdformat-mdformat-mdsf mdformat
```

Or with pipx:

```sh
pipx install mdformat
pipx inject mdformat mdformat-mdformat-mdsf
```

## Configuration

### mdsf Configuration

You can configure mdsf's formatters using an `mdsf.json` configuration file in your project. See the [mdsf documentation](https://github.com/hougesen/mdsf) for configuration options.

### Plugin Configuration

The plugin can be configured in three ways:

**1. CLI Arguments**

```sh
mdformat --mdsf-config path/to/mdsf.json \
         --mdsf-timeout 60 \
         --mdsf-languages python,rust,go \
         --mdsf-fail-on-error \
         your-file.md
```

**2. TOML Configuration File** (`.mdformat.toml`)

```toml
[tool.mdformat.plugin.mdsf]
config = "path/to/mdsf.json"  # Path to mdsf config file
timeout = 60                   # Timeout in seconds (default: 30)
languages = ["python", "rust", "go"]  # Specific languages to format
fail_on_error = false          # Fail on errors vs. fallback (default: false)
```

**3. Python API**

```python
import mdformat

formatted = mdformat.text(
    text,
    codeformatters={"python"},
    options={
        "mdsf_config": "path/to/mdsf.json",
        "mdsf_timeout": 60,
        "mdsf_languages": ["python", "rust"],
        "mdsf_fail_on_error": False,
    }
)
```

### Configuration Options

- **`config`** / **`--mdsf-config`**: Path to custom mdsf.json configuration file
- **`timeout`** / **`--mdsf-timeout`**: Maximum time (in seconds) to wait for mdsf (default: 30)
- **`languages`** / **`--mdsf-languages`**: Specific languages to format (default: all supported languages)
- **`fail_on_error`** / **`--mdsf-fail-on-error`**: Whether to fail on formatting errors or silently fall back to unformatted code (default: false)

## Contributing

See [CONTRIBUTING.md](https://github.com/kyleking/mdformat-mdformat-mdsf/blob/main/CONTRIBUTING.md)

[ci-badge]: https://github.com/kyleking/mdformat-mdformat-mdsf/workflows/CI/badge.svg?branch=main
[ci-link]: https://github.com/kyleking/mdformat-mdformat-mdsf/actions?query=workflow%3ACI+branch%3Amain+event%3Apush
[pypi-badge]: https://img.shields.io/pypi/v/mdformat-mdformat-mdsf.svg
[pypi-link]: https://pypi.org/project/mdformat-mdformat-mdsf
