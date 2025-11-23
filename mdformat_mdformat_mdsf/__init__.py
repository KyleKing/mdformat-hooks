"""An mdformat plugin for formatting code blocks with mdsf.

This plugin integrates mdsf (https://github.com/hougesen/mdsf) with mdformat
to automatically format code blocks in Markdown files using various formatters.

Configuration options:
- --mdsf-config PATH: Path to mdsf.json configuration file
- --mdsf-timeout SECONDS: Timeout for mdsf operations (default: 30)
- --mdsf-languages LANG1,LANG2: Comma-separated list of languages to format
- --mdsf-fail-on-error: Fail if mdsf formatting errors occur

TOML configuration (.mdformat.toml):
    [tool.mdformat.plugin.mdsf]
    config = "path/to/mdsf.json"
    timeout = 30
    languages = ["python", "javascript", "rust"]
    fail_on_error = false
"""

__version__ = "0.0.1"

# Export plugin interface for mdformat parser extension
from .plugin import RENDERERS, add_cli_argument_group, update_mdit

__all__ = ("RENDERERS", "__version__", "add_cli_argument_group", "update_mdit")
