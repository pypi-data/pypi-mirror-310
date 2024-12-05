import pytest
from click.testing import CliRunner
from localaws.cli import main
import os
import tempfile

def test_script_execution():
    runner = CliRunner()
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py') as f:
        f.write('print("Hello, World!")')
        f.flush()
        result = runner.invoke(main, [f.name])
        assert result.exit_code == 0
        assert "Hello, World!" in result.output

def test_invalid_profile():
    runner = CliRunner()
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py') as f:
        f.write('print("test")')
        f.flush()
        result = runner.invoke(main, [f.name, '--profile', 'invalid_profile_name'])
        assert result.exit_code == 1
        assert "not found in credentials" in result.output
