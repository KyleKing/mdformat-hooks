# mdformat-hooks

[![Build Status][ci-badge]][ci-link] [![PyPI version][pypi-badge]][pypi-link]

An [mdformat](https://github.com/executablebooks/mdformat) plugin for running shell commands as post-processing hooks. This allows you to integrate external tools like [mdsf](https://github.com/hougesen/mdsf).

## Installation

Add this package wherever you use `mdformat` and the plugin will be auto-recognized. The only configuration required is specifying a 'post command'. See [additional information on `mdformat` plugins here](https://mdformat.readthedocs.io/en/stable/users/plugins.html)

### pre-commit / prek

```yaml
repos:
  - repo: https://github.com/executablebooks/mdformat
    rev: 1.0.0
    hooks:
      - id: mdformat
        additional_dependencies:
          - mdformat-hooks
```

### uvx

```sh
uvx --with mdformat-hooks mdformat
```

Or with pipx:

```sh
pipx install mdformat
pipx inject mdformat mdformat-hooks
```

## Usage

### Command Line

You can use mdformat-hooks via the command line with the following options:

```bash
# Run a post-processing command (e.g., mdsf for additional formatting)
mdformat --post-command "mdsf format --stdin" document.md

# Run a post command with custom timeout
mdformat --post-command "mdsf format --stdin" --timeout 60 document.md
```

### Configuration File

You can configure hooks in your `.mdformat.toml` file:

```toml
[plugin.hooks]
post_command = "mdsf format --stdin"
timeout = 30
strict_hooks = true                          # Optional: fail on command errors (useful for CI)
```

### Python API

```python
import mdformat

# Format with post-processing hook
formatted = mdformat.text(
    markdown_text,
    extensions={"hooks"},
    options={
        "plugin": {
            "hooks": {
                "post_command": "mdsf format --stdin",
                "timeout": 30,
                "strict_hooks": True,  # Optional: fail on command errors
            }
        }
    },
)
```

## How It Works

1. **mdformat**: The text is formatted by mdformat as usual
1. **Post-command**: If configured, the formatted text is passed to the post-command via stdin for additional processing

### Error Handling

By default, mdformat-hooks uses graceful error handling:

- If a command fails (non-zero exit code), the original text is returned and an error is printed to stderr
- If a command times out, the original text is returned and a timeout message is printed to stderr
- All errors are non-fatal to ensure your formatting workflow continues

**Strict Mode**: Enable strict mode to make command failures halt formatting (useful in CI/CD):

```bash
mdformat --post-command "mdsf format --stdin" --strict-hooks document.md
```

In strict mode, any non-zero exit code, timeout, or exception will raise an error and stop formatting.

## Configuration Options

- `post_command`: Shell command to run after mdformat processing
- `timeout`: Maximum time in seconds for the command to execute (default: 30)
- `strict_hooks`: Fail formatting if command returns non-zero exit code (default: false)

## Examples

### Using with mdsf

[mdsf](https://github.com/hougesen/mdsf) is a fast markdown code block formatter that supports hundreds of formatting tools:

```toml
[plugin.hooks]
post_command = "mdsf format --stdin"
```

### Chaining Multiple Tools

Since commands run in shell, you can chain multiple operations:

```toml
[plugin.hooks]
post_command = "prettier --parser markdown --stdin-filepath doc.md | mdsf format --stdin"
```

## Contributing

See [CONTRIBUTING.md](https://github.com/kyleking/mdformat-hooks/blob/main/CONTRIBUTING.md)

[ci-badge]: https://github.com/kyleking/mdformat-hooks/actions/workflows/tests.yml/badge.svg?branch=main
[ci-link]: https://github.com/kyleking/mdformat-hooks/actions?query=workflow%3ACI+branch%3Amain+event%3Apush
[pypi-badge]: https://img.shields.io/pypi/v/mdformat-hooks.svg
[pypi-link]: https://pypi.org/project/mdformat-hooks
