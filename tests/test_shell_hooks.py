"""Tests for shell command hooks."""

from __future__ import annotations

import subprocess
from unittest.mock import Mock, patch

import mdformat
import pytest

from mdformat_hooks.plugin import _run_shell_command, POSTPROCESSORS, _create_combined_processor


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
    """Test POSTPROCESSORS is a proper dict with document processor."""
    assert isinstance(POSTPROCESSORS, dict)
    assert "document" in POSTPROCESSORS
    assert callable(POSTPROCESSORS["document"])


def test_dynamic_postprocessor_with_no_config():
    """Test dynamic postprocessor returns text unchanged with no config."""
    from mdformat_hooks.plugin import _dynamic_postprocessor

    mock_context = Mock(options={"mdformat": {"plugin": {"hooks": {}}}})
    result = _dynamic_postprocessor("test text", Mock(), mock_context)
    assert result == "test text"


def test_dynamic_postprocessor_with_commands():
    """Test dynamic postprocessor applies commands."""
    from mdformat_hooks.plugin import _dynamic_postprocessor

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
    result = _dynamic_postprocessor("test text", Mock(), mock_context)
    # The cat command should return the same text
    assert result == "test text"


@patch("subprocess.run")
def test_combined_processor_runs_both_commands(mock_run):
    """Test that combined processor runs both pre and post commands."""
    mock_run.return_value = Mock(
        returncode=0,
        stdout="processed text",
        stderr="",
    )

    options = {
        "mdformat": {
            "plugin": {
                "hooks": {
                    "pre_command": "pre-cmd",
                    "post_command": "post-cmd",
                    "timeout": 10,
                }
            }
        }
    }

    processor = _create_combined_processor(options)
    assert processor is not None

    mock_node = Mock()
    mock_context = Mock()
    result = processor("input text", mock_node, mock_context)

    # Should have been called twice
    assert mock_run.call_count == 2


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