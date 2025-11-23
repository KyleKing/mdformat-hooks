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

**Command Line:**

```sh
mdformat your-file.md
```

**Python API:**

```python
import mdformat

# Enable specific languages
formatted = mdformat.text(text, codeformatters={"python", "javascript"})

# Or enable all supported languages
formatted = mdformat.text(
    text,
    codeformatters={
        "python", "javascript", "typescript", "rust", "go",
        "java", "c", "cpp", "csharp", "ruby", "php",
        "swift", "kotlin", "scala", "shell", "bash",
        "sh", "zsh", "json", "yaml", "toml", "html",
        "css", "scss", "sql", "graphql", "markdown", "md"
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

You can configure mdsf behavior using an `mdsf.json` configuration file in your project. See the [mdsf documentation](https://github.com/hougesen/mdsf) for configuration options.

## Contributing

See [CONTRIBUTING.md](https://github.com/kyleking/mdformat-mdformat-mdsf/blob/main/CONTRIBUTING.md)

[ci-badge]: https://github.com/kyleking/mdformat-mdformat-mdsf/workflows/CI/badge.svg?branch=main
[ci-link]: https://github.com/kyleking/mdformat-mdformat-mdsf/actions?query=workflow%3ACI+branch%3Amain+event%3Apush
[pypi-badge]: https://img.shields.io/pypi/v/mdformat-mdformat-mdsf.svg
[pypi-link]: https://pypi.org/project/mdformat-mdformat-mdsf
