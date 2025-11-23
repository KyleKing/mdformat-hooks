"""Code formatter using mdsf."""

from __future__ import annotations

import shutil
import subprocess  # noqa: S404


def _find_mdsf_bin() -> str:
    """Find the mdsf binary path.

    Raises:
        RuntimeError: If mdsf binary is not found in PATH
    """
    mdsf_bin = shutil.which("mdsf")
    if mdsf_bin is None:
        msg = "mdsf is not installed. Install it from https://github.com/hougesen/mdsf"
        raise RuntimeError(msg)
    return mdsf_bin


def _format_code_with_mdsf(unformatted: str, language: str) -> str:
    """Format code using mdsf.

    Args:
        unformatted: The unformatted code block content
        language: The language identifier (info string)

    Returns:
        The formatted code as a string
    """
    if not unformatted:
        return unformatted

    # Create a markdown code block
    markdown_input = f"```{language}\n{unformatted}\n```\n"

    # Find mdsf binary
    mdsf_bin = _find_mdsf_bin()

    # Call mdsf with stdin
    try:
        result = subprocess.run(  # noqa: S603
            [mdsf_bin, "format", "--stdin"],
            input=markdown_input,
            capture_output=True,
            text=True,
            check=True,
            timeout=30,
        )
    except subprocess.CalledProcessError:
        # If mdsf fails, return unformatted code
        return unformatted
    except subprocess.TimeoutExpired:
        # If mdsf times out, return unformatted code
        return unformatted
    else:
        formatted_output = result.stdout

        # Extract the code from the formatted markdown
        # Remove the opening fence
        lines = formatted_output.strip().split("\n")
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        # Remove the closing fence
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]

        formatted_code = "\n".join(lines)

        # Ensure trailing newline if original had one
        if unformatted.endswith("\n") and not formatted_code.endswith("\n"):
            formatted_code += "\n"

        return formatted_code


# Formatter functions for each supported language


def format_python(unformatted: str, _info_str: str) -> str:
    """Format Python code using mdsf."""
    return _format_code_with_mdsf(unformatted, "python")


def format_javascript(unformatted: str, _info_str: str) -> str:
    """Format JavaScript code using mdsf."""
    return _format_code_with_mdsf(unformatted, "javascript")


def format_typescript(unformatted: str, _info_str: str) -> str:
    """Format TypeScript code using mdsf."""
    return _format_code_with_mdsf(unformatted, "typescript")


def format_rust(unformatted: str, _info_str: str) -> str:
    """Format Rust code using mdsf."""
    return _format_code_with_mdsf(unformatted, "rust")


def format_go(unformatted: str, _info_str: str) -> str:
    """Format Go code using mdsf."""
    return _format_code_with_mdsf(unformatted, "go")


def format_java(unformatted: str, _info_str: str) -> str:
    """Format Java code using mdsf."""
    return _format_code_with_mdsf(unformatted, "java")


def format_c(unformatted: str, _info_str: str) -> str:
    """Format C code using mdsf."""
    return _format_code_with_mdsf(unformatted, "c")


def format_cpp(unformatted: str, _info_str: str) -> str:
    """Format C++ code using mdsf."""
    return _format_code_with_mdsf(unformatted, "cpp")


def format_csharp(unformatted: str, _info_str: str) -> str:
    """Format C# code using mdsf."""
    return _format_code_with_mdsf(unformatted, "csharp")


def format_ruby(unformatted: str, _info_str: str) -> str:
    """Format Ruby code using mdsf."""
    return _format_code_with_mdsf(unformatted, "ruby")


def format_php(unformatted: str, _info_str: str) -> str:
    """Format PHP code using mdsf."""
    return _format_code_with_mdsf(unformatted, "php")


def format_swift(unformatted: str, _info_str: str) -> str:
    """Format Swift code using mdsf."""
    return _format_code_with_mdsf(unformatted, "swift")


def format_kotlin(unformatted: str, _info_str: str) -> str:
    """Format Kotlin code using mdsf."""
    return _format_code_with_mdsf(unformatted, "kotlin")


def format_scala(unformatted: str, _info_str: str) -> str:
    """Format Scala code using mdsf."""
    return _format_code_with_mdsf(unformatted, "scala")


def format_shell(unformatted: str, _info_str: str) -> str:
    """Format Shell code using mdsf."""
    return _format_code_with_mdsf(unformatted, "shell")


def format_bash(unformatted: str, _info_str: str) -> str:
    """Format Bash code using mdsf."""
    return _format_code_with_mdsf(unformatted, "bash")


def format_sh(unformatted: str, _info_str: str) -> str:
    """Format sh code using mdsf."""
    return _format_code_with_mdsf(unformatted, "sh")


def format_zsh(unformatted: str, _info_str: str) -> str:
    """Format Zsh code using mdsf."""
    return _format_code_with_mdsf(unformatted, "zsh")


def format_json(unformatted: str, _info_str: str) -> str:
    """Format JSON code using mdsf."""
    return _format_code_with_mdsf(unformatted, "json")


def format_yaml(unformatted: str, _info_str: str) -> str:
    """Format YAML code using mdsf."""
    return _format_code_with_mdsf(unformatted, "yaml")


def format_toml(unformatted: str, _info_str: str) -> str:
    """Format TOML code using mdsf."""
    return _format_code_with_mdsf(unformatted, "toml")


def format_html(unformatted: str, _info_str: str) -> str:
    """Format HTML code using mdsf."""
    return _format_code_with_mdsf(unformatted, "html")


def format_css(unformatted: str, _info_str: str) -> str:
    """Format CSS code using mdsf."""
    return _format_code_with_mdsf(unformatted, "css")


def format_scss(unformatted: str, _info_str: str) -> str:
    """Format SCSS code using mdsf."""
    return _format_code_with_mdsf(unformatted, "scss")


def format_sql(unformatted: str, _info_str: str) -> str:
    """Format SQL code using mdsf."""
    return _format_code_with_mdsf(unformatted, "sql")


def format_graphql(unformatted: str, _info_str: str) -> str:
    """Format GraphQL code using mdsf."""
    return _format_code_with_mdsf(unformatted, "graphql")


def format_markdown(unformatted: str, _info_str: str) -> str:
    """Format Markdown code using mdsf."""
    return _format_code_with_mdsf(unformatted, "markdown")


def format_md(unformatted: str, _info_str: str) -> str:
    """Format Markdown code using mdsf."""
    return _format_code_with_mdsf(unformatted, "md")
