"""Tests for shell command hooks."""

from __future__ import annotations

import argparse
import sys
from unittest.mock import Mock, patch

import mdformat
import pytest
from mdformat._cli import run

from mdformat_hooks.plugin import (
    POSTPROCESSORS,
    _create_post_processor,
    _dynamic_postprocessor,
    _run_shell_command,
    add_cli_argument_group,
)


def test_run_shell_command_success():
    """Test successful shell command execution."""
    text = "Hello, World!"
    # Use a simple echo command that should work on all platforms
    result = _run_shell_command(text, "cat", timeout=5)
    assert result == text


def test_run_shell_command_with_none():
    """Test that None command returns original text."""
    text = "Hello, World!"
    result = _run_shell_command(text, None, timeout=5)
    assert result == text


def test_run_shell_command_error():
    """Test that command error returns original text."""
    text = "Hello, World!"
    # Use a command that will fail
    result = _run_shell_command(text, "false", timeout=5)
    assert result == text


def test_run_shell_command_timeout():
    """Test that command timeout returns original text."""
    text = "Hello, World!"
    # Use a command that will timeout
    result = _run_shell_command(text, "sleep 10", timeout=0.1)
    assert result == text


def test_postprocessors_dict():
    """POSTPROCESSORS is keyed on the node type mdformat renders from."""
    assert isinstance(POSTPROCESSORS, dict)
    assert "root" in POSTPROCESSORS
    assert callable(POSTPROCESSORS["root"])


def test_dynamic_postprocessor_with_no_config():
    """Test dynamic postprocessor returns text unchanged with no config."""
    mock_context = Mock(options={"mdformat": {"plugin": {"hooks": {}}}})
    result = _dynamic_postprocessor("test text", Mock(type="root"), mock_context)
    assert result == "test text"


def test_dynamic_postprocessor_with_commands():
    """Test dynamic postprocessor applies commands."""
    mock_context = Mock(
        options={
            "mdformat": {
                "plugin": {
                    "hooks": {
                        "post_command": "cat",
                        "timeout": 10,
                    }
                }
            }
        }
    )
    result = _dynamic_postprocessor("test text", Mock(type="root"), mock_context)
    # The cat command should return the same text
    assert result == "test text"


@patch("subprocess.run")
def test_post_processor_runs_command(mock_run):
    """Test that post processor runs post command."""
    mock_run.return_value = Mock(
        returncode=0,
        stdout="processed text",
        stderr="",
    )

    options = {
        "mdformat": {
            "plugin": {
                "hooks": {
                    "post_command": "post-cmd",
                    "timeout": 10,
                }
            }
        }
    }

    processor = _create_post_processor(options)
    assert processor is not None

    mock_node = Mock()
    mock_context = Mock()
    result = processor("input text", mock_node, mock_context)  # ruff: ignore[unused-variable]

    # Should have been called once
    assert mock_run.call_count == 1


def test_mdformat_with_hooks():
    """Test mdformat integration with hooks."""
    text = "# Hello\n\nWorld!\n"

    # Test without any hooks (should just format normally)
    result = mdformat.text(text, extensions={"hooks"})
    assert result == "# Hello\n\nWorld!\n"


def test_mdformat_with_post_command():
    """Test mdformat with a simple post-command."""
    text = "# Hello\n\nWorld!\n"

    # Use cat command (should return the same text)
    options = {
        "plugin": {
            "hooks": {
                "post_command": "cat",
            }
        }
    }
    result = mdformat.text(text, extensions={"hooks"}, options=options)
    assert result == "# Hello\n\nWorld!\n"


def test_mdformat_post_command_rewrites_output():
    """A rewriting command reaches the real render path, not just a mocked node."""
    options = {"plugin": {"hooks": {"post_command": "sed s/World/Mars/"}}}

    result = mdformat.text("# Hello\n\nWorld!\n", extensions={"hooks"}, options=options)

    assert result == "# Hello\n\nMars!\n"


def test_mdformat_post_command_receives_trailing_newline(tmp_path):
    """The command reads a POSIX-style final newline and adds no blank line."""
    # A script file rather than `-c`: shlex.quote emits POSIX single quotes, which
    # cmd.exe passes through literally and then fails to parse.
    script = tmp_path / "check_newline.py"
    script.write_text(
        "import sys\n"
        "sys.stdout.write('ends-with-newline'"
        " if sys.stdin.read().endswith(chr(10)) else 'no-trailing-newline')\n"
    )
    command = f'"{sys.executable}" "{script}"'
    options = {"plugin": {"hooks": {"post_command": command}}}

    result = mdformat.text("Hello\n", extensions={"hooks"}, options=options)

    assert result == "ends-with-newline\n"


def test_cli_applies_post_command_from_toml(tmp_path):
    """The CLI honors a `.mdformat.toml` hook against a real file on disk."""
    (tmp_path / ".mdformat.toml").write_text(
        '[plugin.hooks]\npost_command = "sed s/World/Mars/"\n'
    )
    target = tmp_path / "doc.md"
    target.write_text("# Hello\n\nWorld!\n")

    exit_code = run([str(target), "--no-validate"])

    assert exit_code == 0
    assert target.read_text() == "# Hello\n\nMars!\n"


# Strict mode tests
def test_strict_mode_success():
    """Strict mode passes when command succeeds."""
    text = "Hello, World!"
    result = _run_shell_command(text, "cat", timeout=5, strict=True)
    assert result == text


def test_strict_mode_failure_nonzero_exit():
    """Strict mode raises exception on non-zero exit."""
    text = "Hello, World!"
    with pytest.raises(RuntimeError, match="Command failed with exit code"):
        _run_shell_command(text, "false", timeout=5, strict=True)


def test_strict_mode_timeout():
    """Strict mode raises exception on timeout."""
    text = "Hello, World!"
    with pytest.raises(RuntimeError, match="Command timed out"):
        _run_shell_command(text, "sleep 10", timeout=0.1, strict=True)


def test_strict_mode_disabled_by_default():
    """Non-strict mode (default) returns original text on error."""
    text = "Hello, World!"
    # Command fails but strict is False (default), so should return original text
    result = _run_shell_command(text, "false", timeout=5, strict=False)
    assert result == text


def test_strict_mode_with_post_command_failure():
    """Strict mode raises exception on post_command failure."""
    mock_node = Mock()
    mock_node.type = "root"

    mock_context = Mock()
    mock_context.options = {
        "mdformat": {
            "plugin": {
                "hooks": {
                    "post_command": "false",  # Command that fails
                    "strict_hooks": True,
                    "timeout": 10,
                }
            }
        }
    }

    # Should raise because post_command fails and strict=True
    with pytest.raises(RuntimeError, match="Command failed with exit code"):
        _dynamic_postprocessor("test text", mock_node, mock_context)


def test_strict_mode_with_post_command_success():
    """Strict mode allows successful post_command to pass."""
    mock_node = Mock()
    mock_node.type = "root"

    mock_context = Mock()
    mock_context.options = {
        "mdformat": {
            "plugin": {
                "hooks": {
                    "post_command": "cat",  # Command that succeeds
                    "strict_hooks": True,
                    "timeout": 10,
                }
            }
        }
    }

    # Should work fine because command succeeds
    result = _dynamic_postprocessor("test text", mock_node, mock_context)
    assert result == "test text"


@patch("subprocess.run")
def test_strict_mode_post_processor(mock_run):
    """Test that strict mode is passed to post processor."""
    mock_run.return_value = Mock(
        returncode=1,  # Failure
        stdout="",
        stderr="error output",
    )

    options = {
        "mdformat": {
            "plugin": {
                "hooks": {
                    "post_command": "some-cmd",
                    "strict_hooks": True,
                    "timeout": 10,
                }
            }
        }
    }

    processor = _create_post_processor(options)
    assert processor is not None

    mock_node = Mock()
    mock_context = Mock()

    # Should raise because command fails and strict=True
    with pytest.raises(RuntimeError, match="Command failed with exit code"):
        processor("input text", mock_node, mock_context)


# CLI argument group tests
def test_add_cli_argument_group():
    """Test that CLI argument group adds correct arguments."""
    parser = argparse.ArgumentParser()
    group = parser.add_argument_group("hooks")

    # Add the arguments
    add_cli_argument_group(group)

    # Parse some test arguments
    test_timeout = 60
    args = parser.parse_args(
        ["--post-command", "cat", "--timeout", str(test_timeout), "--strict-hooks"]
    )

    # Verify arguments were added correctly
    assert args.post_command == "cat"
    assert args.timeout == test_timeout
    assert args.strict_hooks is True


def test_add_cli_argument_group_defaults():
    """Test CLI argument defaults."""
    parser = argparse.ArgumentParser()
    group = parser.add_argument_group("hooks")

    add_cli_argument_group(group)

    # Parse with no arguments to check defaults
    args = parser.parse_args([])

    # Every default must be None so an absent flag defers to `.mdformat.toml`
    assert args.post_command is None
    assert args.timeout is None
    assert args.strict_hooks is None


def test_absent_cli_flags_defer_to_toml():
    """Absent flags parse to `None`, which mdformat drops so TOML settings win."""
    parser = argparse.ArgumentParser()
    add_cli_argument_group(parser.add_argument_group("hooks"))

    supplied = {k: v for k, v in vars(parser.parse_args([])).items() if v is not None}

    assert supplied == {}


def test_add_cli_argument_group_argument_properties():
    """Test that CLI arguments have correct properties."""
    parser = argparse.ArgumentParser()
    group = parser.add_argument_group("hooks")

    add_cli_argument_group(group)

    # Find the added actions in the parser
    actions = {action.dest: action for action in parser._actions}  # ruff: ignore[private-member-access]

    # Check post_command argument
    assert "post_command" in actions
    post_cmd_action = actions["post_command"]
    assert post_cmd_action.type is str
    assert "Shell command" in post_cmd_action.help

    # Check timeout argument
    assert "timeout" in actions
    timeout_action = actions["timeout"]
    assert timeout_action.type is int
    assert timeout_action.default is None
    assert "Timeout" in timeout_action.help

    # Check strict_hooks argument
    assert "strict_hooks" in actions
    strict_action = actions["strict_hooks"]
    assert isinstance(strict_action, argparse._StoreConstAction)  # ruff: ignore[private-member-access]
    assert strict_action.const is True
    assert strict_action.default is None
    assert "Fail formatting" in strict_action.help
