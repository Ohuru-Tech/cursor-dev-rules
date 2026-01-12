"""Tests for CLI commands in cursor_dev_rules.cli."""

from pathlib import Path
from unittest.mock import patch

import pytest
from click.testing import CliRunner

from cursor_dev_rules.cli import main


class TestFetchCommand:
    """Tests for the fetch CLI command."""

    @pytest.fixture
    def runner(self):
        """Create a CLI runner for testing."""
        return CliRunner()

    @pytest.fixture
    def mock_rules_path(self, mock_rules_dir):
        """Mock get_rules_path to return our test rules directory."""
        return mock_rules_dir

    def test_fetch_backend_django_success(self, runner, mock_rules_path, temp_dir):
        """Test successful fetch of backend/django rules."""
        with patch("cursor_dev_rules.cli.get_rules_path", return_value=mock_rules_path):
            with runner.isolated_filesystem(temp_dir):
                result = runner.invoke(main, ["fetch", "backend/django"])

                assert result.exit_code == 0
                assert "Successfully installed rules" in result.output
                assert "backend/django" in result.output

                # Check that files were copied
                general_rule = Path(".cursor/rules/general/RULE.md")
                specific_rule = Path(".cursor/rules/code-patterns/RULE.md")

                assert general_rule.exists()
                assert specific_rule.exists()
                assert general_rule.read_text() == "# Backend General Rule"
                assert specific_rule.read_text() == "# Django Rule"

    def test_fetch_backend_fastapi_success(self, runner, mock_rules_path, temp_dir):
        """Test successful fetch of backend/fastapi rules."""
        with patch("cursor_dev_rules.cli.get_rules_path", return_value=mock_rules_path):
            with runner.isolated_filesystem(temp_dir):
                result = runner.invoke(main, ["fetch", "backend/fastapi"])

                assert result.exit_code == 0
                assert "Successfully installed rules" in result.output

                # Check that files were copied
                general_rule = Path(".cursor/rules/general/RULE.md")
                specific_rule = Path(".cursor/rules/code-patterns/RULE.md")

                assert general_rule.exists()
                assert specific_rule.exists()
                assert specific_rule.read_text() == "# FastAPI Rule"

    def test_fetch_frontend_nextjs_success(self, runner, mock_rules_path, temp_dir):
        """Test successful fetch of frontend/nextjs rules."""
        with patch("cursor_dev_rules.cli.get_rules_path", return_value=mock_rules_path):
            with runner.isolated_filesystem(temp_dir):
                result = runner.invoke(main, ["fetch", "frontend/nextjs"])

                assert result.exit_code == 0
                assert "Successfully installed rules" in result.output

                # Check that files were copied
                general_rule = Path(".cursor/rules/general/RULE.md")
                specific_rule = Path(".cursor/rules/code-patterns/RULE.md")

                assert general_rule.exists()
                assert specific_rule.exists()
                assert general_rule.read_text() == "# Frontend General Rule"
                assert specific_rule.read_text() == "# Next.js Rule"

    def test_fetch_invalid_path_format_single_part(self, runner):
        """Test fetch with invalid path format (single part)."""
        result = runner.invoke(main, ["fetch", "django"])

        assert result.exit_code != 0
        assert "Invalid rule path format" in result.output
        assert "category/framework" in result.output

    def test_fetch_invalid_path_format_three_parts(self, runner):
        """Test fetch with invalid path format (three parts)."""
        result = runner.invoke(main, ["fetch", "backend/django/extra"])

        assert result.exit_code != 0
        assert "Invalid rule path format" in result.output

    def test_fetch_invalid_path_format_empty(self, runner):
        """Test fetch with empty path."""
        result = runner.invoke(main, ["fetch", ""])

        assert result.exit_code != 0
        assert "Invalid rule path format" in result.output

    def test_fetch_nonexistent_category(self, runner, mock_rules_path, temp_dir):
        """Test fetch with non-existent category."""
        with patch("cursor_dev_rules.cli.get_rules_path", return_value=mock_rules_path):
            with runner.isolated_filesystem(temp_dir):
                result = runner.invoke(main, ["fetch", "nonexistent/framework"])

                assert result.exit_code != 0
                assert "General rule not found" in result.output

    def test_fetch_nonexistent_framework(self, runner, mock_rules_path, temp_dir):
        """Test fetch with non-existent framework."""
        with patch("cursor_dev_rules.cli.get_rules_path", return_value=mock_rules_path):
            with runner.isolated_filesystem(temp_dir):
                result = runner.invoke(main, ["fetch", "backend/nonexistent"])

                assert result.exit_code != 0
                assert "Framework rule not found" in result.output

    def test_fetch_missing_general_rule(self, runner, temp_dir):
        """Test fetch when general rule is missing."""
        # Create a rules directory without general rule
        rules_dir = temp_dir / "rules" / "backend"
        rules_dir.mkdir(parents=True)
        (rules_dir / "django").mkdir(parents=True)
        (rules_dir / "django" / "RULE.md").write_text("# Django Rule")

        with patch(
            "cursor_dev_rules.cli.get_rules_path", return_value=temp_dir / "rules"
        ):
            with runner.isolated_filesystem(temp_dir):
                result = runner.invoke(main, ["fetch", "backend/django"])

                assert result.exit_code != 0
                assert "General rule not found" in result.output

    def test_fetch_missing_specific_rule(self, runner, temp_dir):
        """Test fetch when specific rule is missing."""
        # Create a rules directory without specific rule
        rules_dir = temp_dir / "rules" / "backend"
        rules_dir.mkdir(parents=True)
        (rules_dir / "general").mkdir(parents=True)
        (rules_dir / "general" / "RULE.md").write_text("# General Rule")

        with patch(
            "cursor_dev_rules.cli.get_rules_path", return_value=temp_dir / "rules"
        ):
            with runner.isolated_filesystem(temp_dir):
                result = runner.invoke(main, ["fetch", "backend/django"])

                assert result.exit_code != 0
                assert "Framework rule not found" in result.output

    def test_fetch_with_existing_cursor_directory(
        self, runner, mock_rules_path, temp_dir
    ):
        """Test fetch when .cursor directory already exists."""
        with patch("cursor_dev_rules.cli.get_rules_path", return_value=mock_rules_path):
            with runner.isolated_filesystem(temp_dir):
                # Create existing .cursor directory
                cursor_dir = Path(".cursor")
                cursor_dir.mkdir()

                result = runner.invoke(main, ["fetch", "backend/django"])

                assert result.exit_code == 0
                assert "Successfully installed rules" in result.output

                # Check that files were copied
                general_rule = Path(".cursor/rules/general/RULE.md")
                assert general_rule.exists()

    def test_fetch_with_existing_rules_directory(
        self, runner, mock_rules_path, temp_dir
    ):
        """Test fetch when .cursor/rules directory already exists."""
        with patch("cursor_dev_rules.cli.get_rules_path", return_value=mock_rules_path):
            with runner.isolated_filesystem(temp_dir):
                # Create existing rules directory
                rules_dir = Path(".cursor/rules")
                rules_dir.mkdir(parents=True)

                result = runner.invoke(main, ["fetch", "backend/django"])

                assert result.exit_code == 0
                assert "Successfully installed rules" in result.output

                # Check that files were copied
                general_rule = Path(".cursor/rules/general/RULE.md")
                assert general_rule.exists()

    def test_fetch_overwrites_existing_rules(self, runner, mock_rules_path, temp_dir):
        """Test fetch overwrites existing rule files."""
        with patch("cursor_dev_rules.cli.get_rules_path", return_value=mock_rules_path):
            with runner.isolated_filesystem(temp_dir):
                # Create existing rule files
                general_rule = Path(".cursor/rules/general/RULE.md")
                general_rule.parent.mkdir(parents=True)
                general_rule.write_text("# Old General Rule")

                result = runner.invoke(main, ["fetch", "backend/django"])

                assert result.exit_code == 0
                assert general_rule.exists()
                assert general_rule.read_text() == "# Backend General Rule"

    def test_fetch_file_not_found_error(self, runner, temp_dir):
        """Test fetch when rules directory cannot be found."""
        with patch(
            "cursor_dev_rules.cli.get_rules_path",
            side_effect=FileNotFoundError("Could not find rules directory"),
        ):
            with runner.isolated_filesystem(temp_dir):
                result = runner.invoke(main, ["fetch", "backend/django"])

                assert result.exit_code != 0
                assert "Could not find rules directory" in result.output
                assert "Make sure the package is properly installed" in result.output

    def test_fetch_with_traversable_source(self, runner, mock_traversable, temp_dir):
        """Test fetch with Traversable source from importlib.resources."""
        # This test verifies that the fetch command works with Path objects
        # (which is what get_rules_path returns in dev mode).
        # Testing with actual Traversable objects would require installing
        # the package, which is tested in integration tests.
        # For unit tests, we verify the Path-based flow works correctly.
        mock_rules_path = temp_dir / "rules"
        (mock_rules_path / "backend" / "general").mkdir(parents=True)
        (mock_rules_path / "backend" / "django").mkdir(parents=True)
        (mock_rules_path / "backend" / "general" / "RULE.md").write_text(
            "# Backend General Rule"
        )
        (mock_rules_path / "backend" / "django" / "RULE.md").write_text("# Django Rule")

        with patch("cursor_dev_rules.cli.get_rules_path", return_value=mock_rules_path):
            with runner.isolated_filesystem(temp_dir):
                result = runner.invoke(main, ["fetch", "backend/django"])

                assert result.exit_code == 0
                assert "Successfully installed rules" in result.output

                # Verify files were copied
                general_rule = Path(".cursor/rules/general/RULE.md")
                specific_rule = Path(".cursor/rules/code-patterns/RULE.md")
                assert general_rule.exists()
                assert specific_rule.exists()

    def test_fetch_special_characters_in_path(self, runner, mock_rules_path, temp_dir):
        """Test fetch handles special characters in paths correctly."""
        with patch("cursor_dev_rules.cli.get_rules_path", return_value=mock_rules_path):
            with runner.isolated_filesystem(temp_dir):
                # Create a directory with special characters
                special_dir = Path("project with spaces")
                special_dir.mkdir()

                with patch("cursor_dev_rules.cli.Path.cwd", return_value=special_dir):
                    result = runner.invoke(main, ["fetch", "backend/django"])

                    assert result.exit_code == 0

    def test_fetch_version_command(self, runner):
        """Test the version command."""
        result = runner.invoke(main, ["--version"])

        assert result.exit_code == 0
        assert "0.1.0" in result.output

    def test_fetch_help_command(self, runner):
        """Test the help command."""
        result = runner.invoke(main, ["--help"])

        assert result.exit_code == 0
        assert "Cursor Dev Rules" in result.output
        assert "fetch" in result.output

    def test_fetch_copy_file_failure(self, runner, mock_rules_path, temp_dir):
        """Test fetch when copy_rule_file fails."""
        with patch("cursor_dev_rules.cli.get_rules_path", return_value=mock_rules_path):
            with patch("cursor_dev_rules.cli.copy_rule_file", return_value=False):
                with runner.isolated_filesystem(temp_dir):
                    result = runner.invoke(main, ["fetch", "backend/django"])

                    assert result.exit_code != 0

    def test_fetch_unexpected_exception(self, runner, temp_dir):
        """Test fetch handles unexpected exceptions."""
        with patch(
            "cursor_dev_rules.cli.get_rules_path",
            side_effect=ValueError("Unexpected error"),
        ):
            with runner.isolated_filesystem(temp_dir):
                result = runner.invoke(main, ["fetch", "backend/django"])

                assert result.exit_code != 0
                assert "Unexpected error" in result.output
