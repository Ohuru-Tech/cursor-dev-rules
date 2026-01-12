"""Pytest configuration and fixtures."""

import tempfile
from pathlib import Path
from unittest.mock import MagicMock

import pytest


@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def mock_rules_dir(temp_dir):
    """Create a mock rules directory structure."""
    rules_dir = temp_dir / "rules"
    rules_dir.mkdir(parents=True)

    # Create backend rules
    (rules_dir / "backend" / "general").mkdir(parents=True)
    (rules_dir / "backend" / "django").mkdir(parents=True)
    (rules_dir / "backend" / "fastapi").mkdir(parents=True)

    # Create frontend rules
    (rules_dir / "frontend" / "general").mkdir(parents=True)
    (rules_dir / "frontend" / "nextjs").mkdir(parents=True)

    # Create RULE.md files
    (rules_dir / "backend" / "general" / "RULE.md").write_text("# Backend General Rule")
    (rules_dir / "backend" / "django" / "RULE.md").write_text("# Django Rule")
    (rules_dir / "backend" / "fastapi" / "RULE.md").write_text("# FastAPI Rule")
    (rules_dir / "frontend" / "general" / "RULE.md").write_text(
        "# Frontend General Rule"
    )
    (rules_dir / "frontend" / "nextjs" / "RULE.md").write_text("# Next.js Rule")

    return rules_dir


@pytest.fixture
def mock_traversable():
    """Create a mock Traversable object from importlib.resources."""
    mock = MagicMock()
    mock.is_dir.return_value = True
    mock.is_file.return_value = True
    mock.read_bytes.return_value = b"# Mock Rule Content"
    return mock


@pytest.fixture
def mock_package_resources(mock_rules_dir, mock_traversable):
    """Mock importlib.resources to return our test rules directory."""

    def mock_files(package_name):
        if package_name == "cursor_dev_rules":
            mock_package = MagicMock()
            mock_rules = MagicMock()
            mock_rules.is_dir.return_value = True

            # Mock the general rule
            mock_general = MagicMock()
            mock_general.is_file.return_value = True
            mock_general.read_bytes.return_value = b"# Backend General Rule"

            # Mock the specific rule
            mock_specific = MagicMock()
            mock_specific.is_file.return_value = True
            mock_specific.read_bytes.return_value = b"# Django Rule"

            # Set up the path structure
            def mock_div(name):
                if name == "rules":
                    return mock_rules
                elif name == "backend":
                    mock_backend = MagicMock()
                    mock_backend.__truediv__ = (
                        lambda x: mock_general
                        if x == "general/RULE.md"
                        else mock_specific
                    )
                    return mock_backend
                return MagicMock()

            mock_rules.__truediv__ = mock_div
            mock_package.__truediv__ = (
                lambda x: mock_rules if x == "rules" else MagicMock()
            )
            return mock_package
        return MagicMock()

    return mock_files
